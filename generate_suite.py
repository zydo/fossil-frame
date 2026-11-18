#!/usr/bin/env python3
import argparse
import csv
import os
from pathlib import Path
import subprocess
import sys


COLOR_PATCHES = [
    ("white", 0.03, 0.55, 0.06, 0.10),
    ("black", 0.10, 0.55, 0.06, 0.10),
    ("red", 0.17, 0.55, 0.06, 0.10),
    ("green", 0.24, 0.55, 0.06, 0.10),
    ("blue", 0.31, 0.55, 0.06, 0.10),
    ("yellow", 0.03, 0.67, 0.06, 0.10),
    ("cyan", 0.10, 0.67, 0.06, 0.10),
    ("magenta", 0.17, 0.67, 0.06, 0.10),
]


def find_font():
    configured = os.getenv("SUITE_FONT")
    if configured and Path(configured).exists():
        return configured
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/local/share/fonts/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    try:
        result = subprocess.run(
            ["fc-match", "-f", "%{file}", "sans"], check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        candidate = result.stdout.strip()
        if candidate and Path(candidate).exists():
            return candidate
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    return None


FONT = find_font()


def fr(value):
    if float(value).is_integer():
        return str(int(value))
    return f"{float(value):g}"


def audio_encoder(codec):
    presets = {
        "mp2": ["-c:a", "mp2", "-b:a", "128k", "-ar", "44100", "-ac", "2"],
        "mp3": ["-c:a", "libmp3lame", "-b:a", "112k", "-ar", "44100", "-ac", "2"],
        "aac": ["-c:a", "aac", "-b:a", "72k", "-ar", "44100", "-ac", "2"],
        "ac3": ["-c:a", "ac3", "-b:a", "96k", "-ar", "48000", "-ac", "2"],
        "wmav1": ["-c:a", "wmav1", "-b:a", "64k", "-ar", "44100", "-ac", "2"],
        "wmav2": ["-c:a", "wmav2", "-b:a", "64k", "-ar", "44100", "-ac", "2"],
        "vorbis": ["-c:a", "libvorbis", "-q:a", "2", "-ar", "44100", "-ac", "2"],
        "flac": ["-c:a", "flac", "-ar", "44100", "-ac", "2"],
        "pcm_s16le": ["-c:a", "pcm_s16le", "-ar", "44100", "-ac", "2"],
        "adpcm_ima_wav": ["-c:a", "adpcm_ima_wav", "-ar", "44100", "-ac", "2"],
        "adpcm_ms": ["-c:a", "adpcm_ms", "-ar", "44100", "-ac", "2"],
        "amr_nb": ["-c:a", "libopencore_amrnb", "-b:a", "12.2k", "-ar", "8000", "-ac", "1"],
        "real_144": ["-c:a", "real_144", "-ar", "8000", "-ac", "1"],
        "nellymoser": ["-c:a", "nellymoser", "-ar", "44100", "-ac", "1"],
    }
    return presets[codec]


def video_encoder(codec):
    presets = {
        "msmpeg4v2": ["-c:v", "msmpeg4v2", "-b:v", "360k", "-qmin", "3", "-qmax", "12"],
        "msmpeg4v3": ["-c:v", "msmpeg4v3", "-b:v", "380k", "-qmin", "3", "-qmax", "12"],
        "mpeg1video": ["-c:v", "mpeg1video", "-b:v", "600k", "-qmin", "3", "-qmax", "12"],
        "mpeg2video": ["-c:v", "mpeg2video", "-b:v", "900k", "-qmin", "3", "-qmax", "12"],
        "mpeg4": ["-c:v", "mpeg4", "-q:v", "7"],
        "libxvid": ["-c:v", "libxvid", "-q:v", "7"],
        "h263": ["-c:v", "h263", "-b:v", "140k"],
        "rv10": ["-c:v", "rv10", "-b:v", "300k", "-qmin", "3", "-qmax", "12"],
        "rv20": ["-c:v", "rv20", "-b:v", "340k", "-qmin", "3", "-qmax", "12"],
        "wmv1": ["-c:v", "wmv1", "-b:v", "340k", "-qmin", "3", "-qmax", "12"],
        "wmv2": ["-c:v", "wmv2", "-b:v", "360k", "-qmin", "3", "-qmax", "12"],
        "mjpeg": ["-c:v", "mjpeg", "-q:v", "7"],
        "theora": ["-c:v", "libtheora", "-q:v", "4"],
        "flv1": ["-c:v", "flv", "-q:v", "8"],
        "h264": ["-c:v", "libx264", "-profile:v", "baseline", "-preset", "veryfast", "-crf", "31"],
        "vp8": ["-c:v", "libvpx", "-b:v", "420k", "-deadline", "realtime", "-cpu-used", "8"],
        "ffv1": ["-c:v", "ffv1", "-level", "3"],
        "ffv1_rgb": ["-c:v", "ffv1", "-level", "3", "-pix_fmt", "bgr0"],
        "rawvideo": ["-c:v", "rawvideo", "-pix_fmt", "bgr24"],
    }
    return presets[codec]


JOBS = [
    dict(name="avi_msmpeg4v2_mp3_320x240_7fps.avi", format="avi", width=320, height=240,
         sar="1:1", fps=7, video="msmpeg4v2", audio="mp3"),
    dict(name="avi_msmpeg4v3_mp3_320x240.avi", format="avi", width=320, height=240,
         sar="1:1", fps=15, video="msmpeg4v3", audio="mp3"),
    dict(name="avi_mpeg1video_mp2_320x240_25fps.avi", format="avi", width=320, height=240,
         sar="1:1", fps=25, video="mpeg1video", audio="mp2"),
    dict(name="avi_mpeg4asp_mp3_352x288_sar12-11.avi", format="avi", width=352, height=288,
         sar="12:11", fps=25, video="libxvid", audio="mp3"),
    dict(name="avi_h263_adpcm_176x144.avi", format="avi", width=176, height=144,
         sar="1:1", fps=15, video="h263", audio="adpcm_ima_wav"),
    dict(name="avi_msmpeg4v2_adpcm_320x180_8fps.avi", format="avi", width=320, height=180,
         sar="1:1", fps=8, video="msmpeg4v2", audio="adpcm_ms"),
    dict(name="avi_rawvideo_bgr24_136x76_10fps.avi", format="avi", width=136, height=76,
         sar="1:1", fps=10, video="rawvideo", audio="pcm_s16le", pixel_format="bgr24"),
    dict(name="mkv_mpeg2video_ac3_720x480_sar32-27.mkv", format="matroska", width=720,
         height=480, sar="32:27", fps="29.97", video="mpeg2video", audio="ac3"),
    dict(name="mkv_mpeg4asp_mp3_352x288_sar64-45.mkv", format="matroska", width=352,
         height=288, sar="64:45", fps=25, video="mpeg4", audio="mp3"),
    dict(name="mkv_mjpeg_pcm_320x240.mkv", format="matroska", width=320, height=240,
         sar="1:1", fps=15, video="mjpeg", audio="pcm_s16le"),
    dict(name="mkv_h263_mp3_176x144.mkv", format="matroska", width=176, height=144,
         sar="1:1", fps=15, video="h263", audio="mp3"),
    dict(name="mkv_ffv1_rgb_flac_227x127_12-5fps.mkv", format="matroska", width=227,
         height=127, sar="1:1", fps="12.5", video="ffv1_rgb", audio="flac",
         pixel_format="bgr0", source="color"),
    dict(name="mkv_vp8_vorbis_320x240.mkv", format="matroska", width=320, height=240,
         sar="1:1", fps=15, video="vp8", audio="vorbis"),
    dict(name="mp4_mpeg4asp_mp3_640x360.mp4", format="mp4", width=640, height=360,
         sar="1:1", fps=25, video="mpeg4", audio="mp3"),
    dict(name="mp4_mpeg4asp_mp3_160x106.mp4", format="mp4", width=160, height=106,
         sar="1:1", fps=10, video="mpeg4", audio="mp3"),
    dict(name="mov_mjpeg_pcm_320x240.mov", format="mov", width=320, height=240,
         sar="1:1", fps=15, video="mjpeg", audio="pcm_s16le"),
    dict(name="mov_mpeg4asp_mp2_256x144_sar16-15.mov", format="mov", width=256, height=144,
         sar="16:15", fps=12, video="mpeg4", audio="mp2"),
    dict(name="3gp_h263_amrnb_176x144.3gp", format="3gp", width=176, height=144,
         sar="1:1", fps=15, video="h263", audio="amr_nb"),
    dict(name="3gp_mpeg4_amrnb_128x96.3gp", format="3gp", width=128, height=96,
         sar="1:1", fps=10, video="mpeg4", audio="amr_nb"),
    dict(name="asf_wmv1_wmav1_320x240.wmv", format="asf", width=320, height=240,
         sar="1:1", fps=15, video="wmv1", audio="wmav1"),
    dict(name="asf_wmv2_wmav2_320x240.wmv", format="asf", width=320, height=240,
         sar="1:1", fps=15, video="wmv2", audio="wmav2"),
    dict(name="asf_msmpeg4v3_wmav2_256x144_sar32-27.asf", format="asf", width=256,
         height=144, sar="32:27", fps=15, video="msmpeg4v3", audio="wmav2"),
    dict(name="rm_rv10_ac3_320x240.rm", format="rm", width=320, height=240,
         sar="1:1", fps=15, video="rv10", audio="ac3"),
    dict(name="rm_rv10_real144_176x144_sar12-11.rm", format="rm", width=176, height=144,
         sar="12:11", fps=12, video="rv10", audio="real_144"),
    dict(name="rm_rv20_ac3_320x240.rmvb", format="rm", width=320, height=240,
         sar="1:1", fps=15, video="rv20", audio="ac3"),
    dict(name="mpeg1_mpeg1video_mp2_352x240.mpg", format="mpeg", width=352, height=240,
         sar="1:1", fps="23.976", video="mpeg1video", audio="mp2"),
    dict(name="mpeg2_mpeg2video_mp2_720x576_sar64-45.mpg", format="mpeg", width=720,
         height=576, sar="64:45", fps=25, video="mpeg2video", audio="mp2"),
    dict(name="mpegts_mpeg2video_ac3_480x480_29-97.mpegts", format="mpegts", width=480,
         height=480, sar="1:1", fps="29.97", video="mpeg2video", audio="ac3"),
    dict(name="vcd_mpeg1video_mp2_352x240.mpg", format="vcd", width=352, height=240,
         sar="1:1", fps="23.976", video="mpeg1video", audio="mp2"),
    dict(name="svcd_mpeg2video_mp2_480x480.mpg", format="svcd", width=480, height=480,
         sar="1:1", fps="23.976", video="mpeg2video", audio="mp2"),
    dict(name="dvd_mpeg2video_ac3_720x480_sar32-27.vob", format="dvd", width=720,
         height=480, sar="32:27", fps="29.97", video="mpeg2video", audio="ac3"),
    dict(name="ogv_theora_vorbis_320x240.ogv", format="ogv", width=320, height=240,
         sar="1:1", fps=15, video="theora", audio="vorbis"),
    dict(name="flv_flv1_mp3_320x240.flv", format="flv", width=320, height=240,
         sar="1:1", fps=15, video="flv1", audio="mp3"),
    dict(name="flv_h264_nellymoser_320x240.flv", format="flv", width=320, height=240,
         sar="1:1", fps=15, video="h264", audio="nellymoser"),
    dict(name="nut_ffv1_rgb_pcm_161x107_12-5fps.nut", format="nut", width=161,
         height=107, sar="1:1", fps="12.5", video="ffv1_rgb", audio="pcm_s16le",
         pixel_format="bgr0", source="color"),
]


DAMAGE_SUFFIXES = [
    ("avi_msmpeg4v3_mp3_320x240.avi", "corrupt"),
    ("mp4_mpeg4asp_mp3_640x360.mp4", "trunc"),
    ("mkv_mpeg2video_ac3_720x480_sar32-27.mkv", "corrupt"),
    ("mkv_mpeg4asp_mp3_352x288_sar64-45.mkv", "trunc"),
    ("3gp_h263_amrnb_176x144.3gp", "corrupt"),
    ("3gp_mpeg4_amrnb_128x96.3gp", "trunc"),
    ("asf_wmv1_wmav1_320x240.wmv", "corrupt"),
    ("rm_rv10_ac3_320x240.rm", "corrupt"),
    ("rm_rv20_ac3_320x240.rmvb", "trunc"),
    ("mpegts_mpeg2video_ac3_480x480_29-97.mpegts", "corrupt"),
]


def visual_filters(job):
    width = job["width"]
    height = job["height"]
    sar_x, sar_y = map(int, job["sar"].split(":"))
    sar_value = sar_x / sar_y
    display_width = width * sar_value
    dar = display_width / height
    font = min(max(9, round(height / 14)), 34)
    small_font = max(8, round(font * 0.78))
    font_option = f"fontfile={FONT}" if FONT else "font=Sans"

    # Compensate the reference box for non-square storage pixels. With correct
    # SAR/DAR handling, it should be rendered as a square on screen.
    box_height = height * 0.22
    box_width = box_height / sar_value
    box_x = width * 0.08
    box_y = height * 0.13

    filters = [
        f"format={job.get('pixel_format', 'yuv420p')}",
        f"setsar={sar_x}/{sar_y}",
        f"drawgrid=x=iw/12:y=ih/8:w=iw/12:h=ih/8:color=white@0.30:t=1",
        f"drawbox=x={box_x:.3f}:y={box_y:.3f}:w={box_width:.3f}:h={box_height:.3f}:"
        "color=white@0.85:t=4",
    ]
    for color, x, y, w, h in COLOR_PATCHES:
        filters.append(
            f"drawbox=x=iw*{x}:y=ih*{y}:w=iw*{w}:h=ih*{h}:color={color}:t=fill"
        )
    filters.extend([
        f"drawbox=0:y=ih*0.79:w=iw:h=ih*0.21:color=black@0.72:t=fill",
        f"drawbox=0:y=0:w=iw:h=ih*0.10:color=black@0.78:t=fill",
        f"drawbox=0:y=0:w=iw:h=ih*0.055:color=white:t=fill:enable='lt(mod(t,1),0.08)'",
        f"drawbox=x='mod(t*(iw-0.12*iw)/5,iw-0.12*iw)':y='ih*0.47':"
        f"w=iw*0.12:h=ih*0.045:color=white@0.85:t=fill",
        f"drawtext={font_option}:text='SYNC {width}x{height} SAR {sar_x}x{sar_y} "
        f"DAR {dar:.3f}':fontcolor=white:fontsize={font}:x=8:y=10",
        f"drawtext={font_option}:text='sec %{{eif\\:trunc(t)\\:d}} "
        f"%{{eif\\:mod(trunc(t),2)\\:d}}':fontcolor=white:fontsize={small_font}:"
        "x=8:y='h*0.82'",
    ])
    return ",".join(filters)


def input_audio(duration):
    return (
        "aevalsrc='if(lt(mod(t,1),0.08),0.65*sin(2*PI*1000*t),0):"
        f"s=48000:c=mono:d={duration}'"
    )


def make_normal(ffmpeg, outdir, job, duration, verbose):
    path = outdir / "normal" / job["name"]
    cmd = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", (
            f"color=c=0x202020:s={job['width']}x{job['height']}:rate={fr(job['fps'])}"
            if job.get("source") == "color"
            else f"testsrc2=size={job['width']}x{job['height']}:rate={fr(job['fps'])}"
        ),
        "-f", "lavfi", "-i", input_audio(duration),
        "-vf", visual_filters(job),
        "-map", "0:v:0", "-map", "1:a:0",
        *video_encoder(job["video"]),
        *audio_encoder(job["audio"]),
        "-t", str(duration),
        "-f", job["format"],
        str(path),
    ]
    return run(cmd, path, verbose)


def make_damage(outdir, name, kind):
    source = outdir / "normal" / name
    target = outdir / "damage" / f"damage_{kind}_{name}"
    if not source.exists():
        return False
    target.write_bytes(source.read_bytes())
    size = target.stat().st_size
    if kind == "trunc":
        with target.open("r+b") as handle:
            handle.truncate(max(1024, int(size * 0.97)))
    else:
        with target.open("r+b") as handle:
            offset = min(max(8192, size // 2), max(8192, size - 16384))
            handle.seek(offset)
            length = min(8192, size - offset)
            handle.write(bytes((index * 37 + 0xA3) & 0xFF for index in range(length)))
    return True


def run(cmd, path, verbose):
    if verbose:
        print(" ".join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode:
        print(f"FAILED {path.name} (exit {result.returncode})", file=sys.stderr)
        print(result.stderr.strip(), file=sys.stderr)
        if path.exists():
            path.unlink()
        return False
    print(f"OK {path.name} {path.stat().st_size / 1024:.0f} KiB")
    return True


def write_manifest(outdir, rows):
    """Write this generator's rows, keeping rows owned by the other generators."""
    path = outdir / "manifest.csv"
    owned = {f"normal/{job['name']}" for job in JOBS}
    owned |= {f"damage/damage_{kind}_{name}" for name, kind in DAMAGE_SUFFIXES}
    kept = []
    if path.exists():
        with path.open(newline="", encoding="utf-8") as handle:
            kept = [row for row in csv.DictReader(handle) if row["file"] not in owned]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "file", "container", "video_codec", "audio_codec", "pixels",
            "sample_aspect_ratio", "fps", "bytes"
        ])
        writer.writeheader()
        writer.writerows(rows + kept)


def write_readme(outdir):
    text = """# Legacy video playback test suite

Every normal clip is a 12-second synthetic reference signal. There is no
third-party video or audio source.

## Pass/fail cues

- A white bar flashes at the top during every integer second. The same interval
  contains a 1 kHz beep. The visible `sec N` label must change at that instant.
- The white center box is compensated for non-square sample aspect ratios. It
  should look square, and the full image should match the DAR printed on it.
- The grid is intended to stay straight and evenly spaced.
- The color patches are fixed white, black, red, green, blue, yellow, cyan, and
  magenta. Wrong color conversion, range, or matrix is immediately visible.
- A white marker crosses the frame every five seconds. Repeated or frozen
  frames show timing/decode problems.

`normal/` contains valid files. `damage/` contains deliberately corrupted or
truncated copies; decoder errors are expected there. A player should conceal
or recover locally where possible, rather than freeze permanently or crash.

The `.rmvb` item uses the FFmpeg-supported RealVideo 2 codec with variable-ish
rate settings. FFmpeg has no encoders for canonical RV30/RV40 RMVB, WMV3/VC-1,
WMA Pro, Indeo, QDesign, Cook, or SIPR; see docs/PROPRIETARY_GAPS.md.
"""
    text = "This generated note is secondary; see README.md in the repository root.\n\n" + text
    (outdir / "GENERATED_README.md").write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "dataset")
    parser.add_argument("--duration", type=float, default=12)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    (args.outdir / "normal").mkdir(parents=True, exist_ok=True)
    (args.outdir / "damage").mkdir(parents=True, exist_ok=True)
    rows = []
    failures = []

    for job in JOBS:
        ok = make_normal(args.ffmpeg, args.outdir, job, args.duration, args.verbose)
        if ok:
            path = args.outdir / "normal" / job["name"]
            rows.append({
                "file": f"normal/{job['name']}",
                "container": job["format"],
                "video_codec": job["video"],
                "audio_codec": job["audio"],
                "pixels": f"{job['width']}x{job['height']}",
                "sample_aspect_ratio": job["sar"],
                "fps": job["fps"],
                "bytes": path.stat().st_size,
            })
        else:
            failures.append(job["name"])

    for name, kind in DAMAGE_SUFFIXES:
        if make_damage(args.outdir, name, kind):
            rows.append({
                "file": f"damage/damage_{kind}_{name}",
                "container": Path(name).suffix,
                "video_codec": "corrupt_copy",
                "audio_codec": "corrupt_copy",
                "pixels": "", "sample_aspect_ratio": "", "fps": "",
                "bytes": (args.outdir / "damage" / f"damage_{kind}_{name}").stat().st_size,
            })

    write_manifest(args.outdir, rows)
    write_readme(args.outdir)
    print(f"\nGenerated {len(rows)} items; {len(failures)} encoder/container jobs failed.")
    if failures:
        print("Failures recorded for follow-up:")
        for name in failures:
            print(f"  {name}")


if __name__ == "__main__":
    main()
