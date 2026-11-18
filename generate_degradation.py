#!/usr/bin/env python3
import csv
import json
import math
from pathlib import Path
import subprocess
import tempfile

import generate_suite as base


DURATION = 12


def add_effects(filters, effects):
    filters.extend(effects)
    filters.append("format=yuv420p")
    return ",".join(filters)


def base_filters(job, title):
    title_font = max(10, round(job["height"] / 17))
    title_y = max(2, round(job["height"] * 0.025))
    return base.visual_filters(job).removesuffix(",format=yuv420p").split(",") + [
        f"drawbox=0:y=ih*0.02:w=iw:h=ih*0.07:color=black@0.75:t=fill",
        f"drawtext=fontfile={base.FONT}:text='{title}':fontcolor=yellow:"
        f"fontsize={title_font}:x=8:y={title_y}",
    ]


def dropout_boxes():
    return [
        "drawbox=x='mod(floor(t*23)*137\\,iw-140)':y='mod(floor(t*17)*91\\,"
        "ih*0.75)+ih*0.12':w='90+mod(floor(t*31)\\,110)':h=3:color=white@0.75:"
        "t=fill:enable='lt(mod(t\\,1.7)\\,0.06)'",
        "drawbox=x='mod(floor(t*41)*211\\,iw-170)':y='mod(floor(t*29)*157\\,"
        "ih*0.75)+ih*0.12':w='70+mod(floor(t*37)\\,100)':h=2:color=black@0.85:"
        "t=fill:enable='lt(mod(t\\,2.3)\\,0.05)'",
        "drawbox=0:y='mod(t*ih*0.11\\,ih*0.72)+ih*0.12':w=iw:h=ih*0.028:"
        "color=white@0.15:t=fill",
    ]


DEGRADED_JOBS = [
    dict(name="vhs_composite_wear_mpeg2_ac3_720x480.mkv", output_format="matroska",
         width=720, height=480, sar="32:27", fps="29.97", video="mpeg2video",
         audio="ac3", title="VHS WEAR / COMPOSITE CAPTURE",
         effects=[
             "rgbashift=rh=3:bh=-3:rv=1:bv=-1",
             "chromashift=cbh=5:crh=-5",
             "gblur=sigma=0.8",
             "noise=alls=16:allf=t+u",
             "lagfun=decay=0.42",
             "tmix=frames=3:weights='1 1 1'",
             *dropout_boxes(),
         ], test="analog wear, chroma bleed, ghosting, dropouts"),
    dict(name="chroma_under_bleed_mpeg2_ac3_720x480.mkv", output_format="matroska",
         width=720, height=480, sar="32:27", fps="29.97", video="mpeg2video",
         audio="ac3", title="COLOR-UNDER CHROMA BLEED",
         effects=[
             "chromashift=cbh=12:crh=-12:cbv=2",
             "rgbashift=rh=6:bh=-6",
             "hue=s=1.35",
             "gblur=sigma=1.2",
             "noise=alls=7:allf=t",
         ], test="VHS color-under chroma delay/bleed"),
    dict(name="motion_ghost_trails_mpeg4_mp3_480x360.mp4", output_format="mp4",
         width=480, height=360, sar="1:1", fps=25, video="mpeg4", audio="mp3",
         title="MOTION GHOST / LAG",
         effects=[
             "lagfun=decay=0.82",
             "tmix=frames=5:weights='1 2 3 2 1'",
         ], test="old decoder/capture ghosting, repeated-reference smearing"),
    dict(name="generation_loss_x3_mpeg4_mp3_352x240.avi", output_format="avi",
         width=352, height=240, sar="1:1", fps=25, video="mpeg4", audio="mp3",
         title="GENERATION LOSS X3", generations=3,
         test="repeated VHS/CD/DVD/P2P-era lossy transcoding"),
    dict(name="long_gop_bitstream_errors_mpeg4_mp3_480x360.avi", output_format="avi",
         width=480, height=360, sar="1:1", fps=25, video="mpeg4", audio="mp3",
         title="LONG GOP + BITSTREAM ERRORS", extra_video=[
             "-g", "300", "-bf", "1", "-error_rate", "3", "-qmin", "8", "-qmax", "31"
         ], expected_decode_errors=True,
         test="I/P/B prediction error propagation across a long GOP"),
    dict(name="damaged_i_frame_mpeg4_mp3_480x360.avi", output_format="avi",
         width=480, height=360, sar="1:1", fps=25, video="mpeg4", audio="mp3",
         title="DAMAGED I-FRAME", damage_i_frame=True, expected_decode_errors=True,
         test="corrupt keyframe propagating into dependent P/B frames"),
    dict(name="interlaced_wrong_handling_mpeg2_ac3_720x480.mkv", output_format="matroska",
         width=720, height=480, sar="32:27", fps="29.97", video="mpeg2video",
         audio="ac3", title="INTERLACED SOURCE / WRONG HANDLING", interlaced=True,
         source_fps="59.94",
         extra_video=["-flags", "+ilme+ildct"],
         test="field order, combing, wrong progressive deinterlace"),
    dict(name="telecine_judder_mpeg2_mp3_720x480.mpg", output_format="mpeg",
         width=720, height=480, sar="32:27", fps="29.97", video="mpeg2video",
         audio="mp3", title="TELECINE / 3-2 CADENCE", source_fps="23.976",
         extra_video=["-flags", "+ilme+ildct"],
         test="film-to-NTSC pulldown and wrong inverse-telecine judder"),
    dict(name="vbr_mp3_audio_offset_mpeg4_352x240.avi", output_format="avi",
         width=352, height=240, sar="1:1", fps=25, video="mpeg4", audio="mp3",
         title="VBR MP3 + AUDIO OFFSET", audio_offset=0.35,
         extra_audio=["-c:a", "libmp3lame", "-q:a", "7", "-ar", "44100", "-ac", "2"],
         test="AVI VBR MP3 timebase issues and constant A/V offset"),
    dict(name="dropped_duplicated_frames_mpeg4_mp3_480x360.mkv", output_format="matroska",
         width=480, height=360, sar="1:1", fps=25, video="mpeg4", audio="mp3",
         title="DROPPED / DUPLICATED FRAMES",
         effects=["select='not(eq(n\\,95)+eq(n\\,190)+eq(n\\,285))'",
                  "setpts=N/(FRAME_RATE*TB)"], test="capture drops, frame repeats, stutter"),
]


def build_command(ffmpeg, outdir, job):
    output_path = outdir / "degraded" / job["name"]
    source_fps = job.get("source_fps", job["fps"])
    filters = base_filters(job, job["title"])
    filters.extend(job.get("effects", []))
    if job.get("interlaced"):
        filters.extend(["tinterlace=mode=interleave_top", "setfield=tff"])
    filters.append("format=yuv420p")

    cmd = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", (
            f"testsrc2=size={job['width']}x{job['height']}:rate={base.fr(source_fps)}"
        ),
        "-f", "lavfi", "-i", base.input_audio(DURATION),
    ]
    if job.get("audio_offset"):
        cmd += ["-itsoffset", str(job["audio_offset"])]
        cmd += ["-f", "lavfi", "-i", base.input_audio(DURATION)]
    cmd += [
        "-vf", ",".join(filters),
        "-map", "0:v:0",
        "-map", f"{2 if job.get('audio_offset') else 1}:a:0",
    ]
    cmd += base.video_encoder(job["video"])
    if job.get("extra_video"):
        cmd += job["extra_video"]
    cmd += job.get("extra_audio", base.audio_encoder(job["audio"]))
    cmd += ["-t", str(DURATION), "-f", job["output_format"], str(output_path)]
    return cmd


def make_generation_loss(ffmpeg, outdir, job):
    output_path = outdir / "degraded" / job["name"]
    with tempfile.TemporaryDirectory(prefix=".generation-", dir=outdir / "degraded") as directory:
        current = Path(directory) / "generation-0.mkv"
        filters = base_filters(job, job["title"])
        cmd = [
            ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i",
            f"testsrc2=size={job['width']}x{job['height']}:rate={base.fr(job['fps'])}",
            "-f", "lavfi", "-i", base.input_audio(DURATION),
            "-vf", "format=yuv420p",
            "-map", "0:v:0", "-map", "1:a:0",
            *base.video_encoder("mpeg2video"),
            "-b:v", "420k", "-qmin", "10", "-qmax", "31", "-g", "45",
            *base.audio_encoder("mp2"), "-t", str(DURATION), str(current)
        ]
        base.run(cmd, current, False)
        for generation in range(1, job["generations"] + 1):
            previous = current
            current = Path(directory) / f"generation-{generation}.{Path(output_path).suffix[1:]}"
            encoder_args = base.video_encoder(job["video"])
            quality_args = [
                "-q:v", str(12 + generation * 4),
                "-g", str(30 + generation * 10),
            ]
            filters = "scale=352:240:flags=lanczos,format=yuv420p"
            cmd = [
                ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(previous), "-vf", filters,
                "-map", "0:v:0", "-map", "0:a:0?", *encoder_args, *quality_args,
                *base.audio_encoder("mp3"), "-t", str(DURATION), str(current)
            ]
            base.run(cmd, current, False)
        current.replace(output_path)
    return True


def make_i_frame_damage(outdir, job):
    path = outdir / "degraded" / job["name"]
    result = subprocess.run([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_packets",
        "-print_format", "json", str(path)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode:
        return False
    packets = json.loads(result.stdout)["packets"]
    keyframes = [packet for packet in packets if "K" in packet.get("flags", "")]
    if not keyframes:
        return False
    target = keyframes[min(1, len(keyframes) - 1)]
    start = int(target["pos"]) + 160
    with path.open("r+b") as handle:
        handle.seek(start)
        handle.write(bytes((index * 53 + 0x71) & 0xFF for index in range(96)))
    return True


def update_manifest(outdir, rows):
    path = outdir / "manifest.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        old_rows = list(csv.DictReader(handle))
    fields = list(old_rows[0].keys()) if old_rows else [
        "file", "container", "video_codec", "audio_codec", "pixels",
        "sample_aspect_ratio", "fps", "bytes"
    ]
    kept = [row for row in old_rows if not row["file"].startswith("degraded/")]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(kept + rows)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "dataset")
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    (args.outdir / "degraded").mkdir(parents=True, exist_ok=True)

    rows = []
    failures = []
    for job in DEGRADED_JOBS:
        path = args.outdir / "degraded" / job["name"]
        if path.exists() and not args.force:
            print(f"SKIP {path.name}")
            rows.append({
                "file": f"degraded/{job['name']}",
                "container": job["output_format"],
                "video_codec": job["video"],
                "audio_codec": job["audio"],
                "pixels": f"{job['width']}x{job['height']}",
                "sample_aspect_ratio": job["sar"],
                "fps": job.get("fps", ""),
                "bytes": path.stat().st_size,
            })
            continue
        if job.get("generations"):
            ok = make_generation_loss(args.ffmpeg, args.outdir, job)
            if ok and not args.verbose:
                print(f"OK {path.name} {path.stat().st_size / 1024:.0f} KiB")
        else:
            ok = base.run(build_command(args.ffmpeg, args.outdir, job), path,
                          args.verbose)
        if ok and job.get("damage_i_frame"):
            ok = make_i_frame_damage(args.outdir, job)
            print(f"{'OK' if ok else 'FAILED'} damage-i-frame {path.name}")
        if ok:
            rows.append({
                "file": f"degraded/{job['name']}",
                "container": job["output_format"],
                "video_codec": job["video"],
                "audio_codec": job["audio"],
                "pixels": f"{job['width']}x{job['height']}",
                "sample_aspect_ratio": job["sar"],
                "fps": job.get("fps", ""),
                "bytes": path.stat().st_size,
            })
        else:
            failures.append(job["name"])
    update_manifest(args.outdir, rows)
    print(f"\nGenerated {len(rows)} degraded items; {len(failures)} jobs failed.")
    for name in failures:
        print(f"  {name}")


if __name__ == "__main__":
    main()
