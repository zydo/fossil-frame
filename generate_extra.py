#!/usr/bin/env python3
"""Extra legacy-playback samples: more old codecs, audio tracks, subtitles,
container/timing structure edge cases, mislabeled extensions and
download-style damage.

Run after generate_suite.py and generate_degradation.py:

    python3 generate_extra.py --outdir dataset

Every video sample reuses the 12-second reference signal from
generate_suite.py (sync bar + 1 kHz beep on every integer second) unless
the title line burned into the picture says otherwise.
"""
import argparse
import csv
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile

import generate_suite as base
import generate_degradation as deg

DURATION = 12
ROOT = Path(__file__).resolve().parent
FONT_ATTACHMENT = ROOT / "assets" / "fonts" / "PressStart2P-Regular.ttf"
ROWS = []
FAILURES = []
VERBOSE = False
FFMPEG = "ffmpeg"


# ---------------------------------------------------------------- helpers

def ff(args, out):
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", *map(str, args), str(out)]
    if VERBOSE:
        print(" ".join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode:
        raise RuntimeError(f"ffmpeg failed for {Path(out).name}:\n{result.stderr.strip()}")
    return out


def probe(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return json.loads(result.stdout or "{}")


def video_src(width, height, fps, duration=DURATION):
    return ["-f", "lavfi", "-i",
            f"testsrc2=size={width}x{height}:rate={base.fr(fps)}:duration={duration}"]


def beep_src(duration=DURATION, rate=48000):
    return ["-f", "lavfi", "-i",
            "aevalsrc='if(lt(mod(t,1),0.08),0.65*sin(2*PI*1000*t),0)':"
            f"s={rate}:c=mono:d={duration}"]


def tone_beep(freq, length=0.08, gain=0.65):
    return f"if(lt(mod(t,1),{length}),{gain}*sin(2*PI*{freq}*t),0)"


def aeval(exprs, layout, duration=DURATION, rate=48000):
    joined = "|".join(exprs)
    return ["-f", "lavfi", "-i", f"aevalsrc='{joined}':s={rate}:c={layout}:d={duration}"]


def channel_id_51(duration=DURATION):
    # Exactly one channel beeps per second: sec%6 -> FL FR FC LFE BL BR.
    exprs = []
    for index in range(6):
        freq = 80 if index == 3 else 1000
        exprs.append(
            f"if(eq(mod(floor(t),6),{index})*lt(mod(t,1),0.30),0.6*sin(2*PI*{freq}*t),0)")
    return aeval(exprs, "5.1", duration)


def vf(width, height, sar="1:1", title=None, tail=None, fps=25):
    job = dict(width=width, height=height, sar=sar, fps=fps)
    if title:
        # ':' and '%' are filtergraph / drawtext expansion syntax.
        title = title.replace(":", "/").replace("%", " MOD ")
        filters = deg.base_filters(job, title)
    else:
        filters = base.visual_filters(job).split(",")
    if tail:
        filters.extend(tail if isinstance(tail, list) else [tail])
    return ",".join(filters)


def row(rel, container, video, audio, pixels="", sar="", fps=""):
    ROWS.append(dict(file=rel, container=container, video_codec=video, audio_codec=audio,
                     pixels=pixels, sample_aspect_ratio=sar, fps=fps, bytes=0))


def job(fn):
    """Decorator: run a generator function, record failure instead of aborting."""
    def wrapper(outdir):
        before = len(ROWS)
        try:
            fn(outdir)
        except Exception as error:  # noqa: BLE001 - report and continue
            del ROWS[before:]
            FAILURES.append(f"{fn.__name__}: {error}")
            print(f"FAILED {fn.__name__}: {error}", file=sys.stderr)
            return
        for item in ROWS[before:]:
            path = outdir / item["file"]
            item["bytes"] = path.stat().st_size
            print(f"OK {item['file']} {item['bytes'] / 1024:.0f} KiB")
    wrapper.__name__ = fn.__name__
    return wrapper


# ------------------------------------------------------------ AVI rewriting

def avi_read(path):
    data = Path(path).read_bytes()
    assert data[:4] == b"RIFF" and data[8:12] == b"AVI "
    chunks = []
    offset = 12
    while offset + 8 <= len(data):
        fid = data[offset:offset + 4]
        size = struct.unpack("<I", data[offset + 4:offset + 8])[0]
        chunks.append([fid, data[offset + 8:offset + 8 + size]])
        offset += 8 + size + (size & 1)
    return chunks


def movi_chunks(payload):
    assert payload[:4] == b"movi"
    items = []
    offset = 4
    while offset + 8 <= len(payload):
        fid = payload[offset:offset + 4]
        size = struct.unpack("<I", payload[offset + 4:offset + 8])[0]
        items.append([fid, payload[offset + 8:offset + 8 + size]])
        offset += 8 + size + (size & 1)
    return items


def idx1_entries(payload):
    return [list(struct.unpack("<4sIII", payload[i:i + 16]))
            for i in range(0, len(payload), 16)]


def avi_write(path, chunks, movi_items, keyflags, write_index=True):
    """Rebuild an AVI from top-level chunks, replacing movi and idx1."""
    movi = bytearray(b"movi")
    index = bytearray()
    for (fid, payload), flags in zip(movi_items, keyflags):
        index += struct.pack("<4sIII", fid, flags, len(movi), len(payload))
        movi += fid + struct.pack("<I", len(payload)) + payload
        if len(payload) & 1:
            movi += b"\0"
    body = bytearray(b"AVI ")
    for fid, payload in chunks:
        if fid == b"idx1":
            continue
        if fid == b"LIST" and payload[:4] == b"movi":
            payload = bytes(movi)
        body += fid + struct.pack("<I", len(payload)) + payload
        if len(payload) & 1:
            body += b"\0"
    if write_index:
        body += b"idx1" + struct.pack("<I", len(index)) + index
    Path(path).write_bytes(b"RIFF" + struct.pack("<I", len(body)) + body)


def avi_movi_and_flags(chunks):
    movi = next(p for f, p in chunks if f == b"LIST" and p[:4] == b"movi")
    items = movi_chunks(movi)
    index = next(p for f, p in chunks if f == b"idx1")
    flags = [entry[1] for entry in idx1_entries(index)]
    assert len(flags) == len(items), "idx1/movi mismatch"
    return items, flags


# --------------------------------------------------------------- normal/

@job
def legacy_codecs(outdir):
    d = outdir / "normal"
    specs = [
        # name, container, w, h, fps, sar, video args, pix tail, audio args, audio src rate, title
        ("avi_cinepak_pcmu8_320x240_22050hz.avi", "avi", 320, 240, 15, "1:1",
         ["-c:v", "cinepak"], "format=rgb24",
         ["-c:a", "pcm_u8", "-ar", "22050", "-ac", "1"], "CINEPAK / 8-BIT PCM 22K"),
        ("mov_cinepak_adpcmimaqt_320x240.mov", "mov", 320, 240, 15, "1:1",
         ["-c:v", "cinepak"], "format=rgb24",
         ["-c:a", "adpcm_ima_qt", "-ar", "22050", "-ac", "1"], "QT CINEPAK / IMA4"),
        ("mov_svq1_adpcmimaqt_320x240.mov", "mov", 320, 240, 15, "1:1",
         ["-c:v", "svq1", "-q:v", "6"], "format=yuv410p",
         ["-c:a", "adpcm_ima_qt", "-ar", "22050", "-ac", "2"], "SORENSON SVQ1 YUV410"),
        ("avi_msvideo1_pcmu8_160x120_11025hz.avi", "avi", 160, 120, 10, "1:1",
         ["-c:v", "msvideo1"], "format=rgb555le",
         ["-c:a", "pcm_u8", "-ar", "11025", "-ac", "1"], "MS VIDEO-1 CRAM"),
        ("mov_qtrle_pcms16be_160x120.mov", "mov", 160, 120, 10, "1:1",
         ["-c:v", "qtrle"], "format=rgb24",
         ["-c:a", "pcm_s16be", "-ar", "22050", "-ac", "1"], "QT ANIMATION RLE"),
        ("mov_smc_pcms16be_160x120.mov", "mov", 160, 120, 10, "1:1",
         ["-c:v", "smc"], "format=pal8",
         ["-c:a", "pcm_s16be", "-ar", "22050", "-ac", "1"], "QT GRAPHICS SMC PAL8"),
        ("mov_rpza_pcms16be_160x120.mov", "mov", 160, 120, 10, "1:1",
         ["-c:v", "rpza"], "format=rgb555le",
         ["-c:a", "pcm_s16be", "-ar", "22050", "-ac", "1"], "QT VIDEO RPZA"),
        ("avi_zmbv_pcm_320x200_70fps.avi", "avi", 320, 200, 70, "5:6",
         ["-c:v", "zmbv"], "format=bgr0",
         ["-c:a", "pcm_s16le", "-ar", "44100", "-ac", "2"], "DOSBOX ZMBV 70HZ 5:6"),
        ("flv_flashsv_adpcmswf_320x240.flv", "flv", 320, 240, 10, "1:1",
         ["-c:v", "flashsv"], "format=bgr24",
         ["-c:a", "adpcm_swf", "-ar", "22050", "-ac", "1"], "FLASH SCREEN VIDEO"),
        ("flv_flashsv2_speex_320x240.flv", "flv", 320, 240, 10, "1:1",
         ["-c:v", "flashsv2"], "format=bgr24",
         ["-c:a", "libspeex", "-ar", "16000", "-ac", "1"], "FLASH SCREEN V2 / SPEEX"),
        ("avi_h261_g726_352x288.avi", "avi", 352, 288, 15, "12:11",
         ["-c:v", "h261", "-b:v", "256k"], "format=yuv420p",
         ["-c:a", "g726", "-ar", "8000", "-ac", "1", "-b:a", "32k"], "H.261 CIF / G.726"),
        ("avi_huffyuv_yuv422_pcm_320x240.avi", "avi", 320, 240, 15, "1:1",
         ["-c:v", "huffyuv"], "format=yuv422p",
         ["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2"], "HUFFYUV 4:2:2 CAPTURE"),
        ("avi_xvid_qpel_gmc_bframes_mp3_640x352.avi", "avi", 640, 352, 25, "1:1",
         ["-c:v", "libxvid", "-q:v", "5", "-gmc", "1", "-flags", "+qpel", "-bf", "2"],
         "format=yuv420p",
         base.audio_encoder("mp3"), "XVID QPEL + GMC + 2 B"),
    ]
    for name, container, w, h, fps, sar, vargs, tail, aargs, title in specs:
        out = d / name
        ff([*video_src(w, h, fps), *beep_src(),
            "-vf", vf(w, h, sar, title, tail, fps), "-map", "0:v", "-map", "1:a",
            *vargs, *aargs, "-t", DURATION, "-f", container], out)
        row(f"normal/{name}", container, vargs[1], aargs[1], f"{w}x{h}", sar, fps)

    # DV is ~25 Mbit/s, so these two are 6 s long to keep the repository small.
    dv_len = 6
    out = d / "avi_dv_pal_bff_pcm48k_720x576_6s.avi"
    ff([*video_src(720, 576, 50, dv_len), *beep_src(dv_len),
        "-vf", vf(720, 576, "64:45", "DV PAL BFF 4:2:0 (6S)",
                  ["format=yuv420p", "tinterlace=mode=interleave_bottom", "setfield=bff"], 50),
        "-map", "0:v", "-map", "1:a", "-c:v", "dvvideo", "-flags", "+ildct",
        "-field_order", "bb", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
        "-t", dv_len, "-f", "avi"], out)
    row(f"normal/{out.name}", "avi", "dvvideo", "pcm_s16le", "720x576", "64:45", 25)
    out = d / "mov_dv_ntsc_411_pcm32k_720x480_6s.mov"
    ff([*video_src(720, 480, "59.94", dv_len), *beep_src(dv_len),
        "-vf", vf(720, 480, "8:9", "DV NTSC BFF 4:1:1 32KHZ (6S)",
                  ["format=yuv411p", "tinterlace=mode=interleave_bottom", "setfield=bff"],
                  "59.94"),
        "-map", "0:v", "-map", "1:a", "-c:v", "dvvideo", "-flags", "+ildct",
        "-field_order", "bb", "-pix_fmt", "yuv411p",
        "-c:a", "pcm_s16le", "-ar", "32000", "-ac", "2",
        "-t", dv_len, "-f", "mov"], out)
    row(f"normal/{out.name}", "mov", "dvvideo", "pcm_s16le", "720x480", "8:9", "29.97")


# ---------------------------------------------------------------- tracks/

@job
def audio_tracks(outdir):
    d = outdir / "tracks"
    d.mkdir(parents=True, exist_ok=True)

    out = d / "vcd_karaoke_left1khz_right500hz_mpeg1_352x240.mpg"
    ff([*video_src(352, 240, "23.976"),
        *aeval([tone_beep(1000), tone_beep(500, 0.25, 0.55)], "stereo", rate=44100),
        "-vf", vf(352, 240, "1:1", "L=1KHZ VOCAL  R=500HZ KARAOKE", None, "23.976"),
        "-map", "0:v", "-map", "1:a", "-f", "vcd"], out)
    row(f"tracks/{out.name}", "vcd", "mpeg1video", "mp2 L/R split", "352x240", "1:1", "23.976")

    out = d / "dvd_dual_audio_ac3-1khz_lpcm-2khz_720x480.vob"
    ff([*video_src(720, 480, "29.97"), *beep_src(),
        *aeval([tone_beep(2000)] * 2, "stereo"),
        "-vf", vf(720, 480, "32:27", "A1 AC3 1KHZ / A2 LPCM 2KHZ", None, "29.97"),
        "-map", "0:v", "-map", "1:a", "-map", "2:a",
        *base.video_encoder("mpeg2video"),
        "-c:a:0", "ac3", "-b:a:0", "192k", "-ac:a:0", "2",
        "-c:a:1", "pcm_dvd", "-ar:a:1", "48000",
        "-t", DURATION, "-f", "dvd"], out)
    row(f"tracks/{out.name}", "dvd", "mpeg2video", "ac3+pcm_dvd", "720x480", "32:27", "29.97")

    for codec, extra in (("ac3", ["-b:a", "448k"]), ("dca", ["-strict", "-2", "-b:a", "768k"])):
        label = "AC3" if codec == "ac3" else "DTS"
        out = d / f"dvd_{label.lower()}51_channel_id_720x480.vob"
        ff([*video_src(720, 480, "29.97"), *channel_id_51(),
            "-vf", vf(720, 480, "32:27",
                      f"{label} 5.1: SEC%6 0FL 1FR 2C 3LFE 4BL 5BR", None, "29.97"),
            "-map", "0:v", "-map", "1:a", *base.video_encoder("mpeg2video"),
            "-c:a", codec, *extra, "-t", DURATION, "-f", "dvd"], out)
        row(f"tracks/{out.name}", "dvd", "mpeg2video", f"{codec} 5.1", "720x480", "32:27",
            "29.97")

    out = d / "mkv_multilang_zho-1khz_eng-2khz-default_jpn51_320x240.mkv"
    ff([*video_src(320, 240, 25), *beep_src(),
        *aeval([tone_beep(2000)] * 2, "stereo"), *channel_id_51(),
        "-vf", vf(320, 240, "1:1", "DEFAULT=ENG 2KHZ", None, 25),
        "-map", "0:v", "-map", "1:a", "-map", "2:a", "-map", "3:a",
        *base.video_encoder("mpeg4"),
        "-c:a:0", "aac", "-b:a:0", "96k", "-c:a:1", "libmp3lame", "-b:a:1", "128k",
        "-c:a:2", "ac3", "-b:a:2", "384k",
        "-metadata:s:a:0", "language=zho", "-metadata:s:a:0", "title=国语 1 kHz",
        "-metadata:s:a:1", "language=eng", "-metadata:s:a:1", "title=English 2 kHz",
        "-metadata:s:a:2", "language=jpn", "-metadata:s:a:2", "title=5.1 channel ID",
        "-disposition:a:0", "0", "-disposition:a:1", "default", "-disposition:a:2", "0",
        "-t", DURATION, "-f", "matroska"], out)
    row(f"tracks/{out.name}", "matroska", "mpeg4", "aac+mp3+ac3 5.1", "320x240", "1:1", 25)

    out = d / "avi_mpeg4_mulaw_8khz_mono_320x240.avi"
    ff([*video_src(320, 240, 15), *beep_src(),
        "-vf", vf(320, 240, "1:1", "G.711 MU-LAW 8KHZ", None, 15),
        "-map", "0:v", "-map", "1:a", *base.video_encoder("mpeg4"),
        "-c:a", "pcm_mulaw", "-ar", "8000", "-ac", "1", "-t", DURATION, "-f", "avi"], out)
    row(f"tracks/{out.name}", "avi", "mpeg4", "pcm_mulaw", "320x240", "1:1", 15)


# ------------------------------------------------------------- subtitles/

SUB_LINES = [(n, f"第 {n} 秒　中文字幕測試", f"sec {n} subtitle") for n in range(1, 12)]


def srt_text():
    parts = []
    for i, (n, zh, en) in enumerate(SUB_LINES, 1):
        parts.append(f"{i}\n00:00:{n:02d},000 --> 00:00:{n:02d},900\n{zh}\n{en}\n")
    return "\n".join(parts) + "\n"


def ssa_text(fontname="Arial"):
    head = f"""[Script Info]
Title: Fossil Frame subtitle sync
ScriptType: v4.00
PlayResX: 720
PlayResY: 480

[V4 Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding
Style: Default,{fontname},28,16777215,65535,0,0,0,0,1,2,0,2,20,20,40,0,1
Style: Top,{fontname},22,65535,65535,0,0,0,0,1,2,0,6,20,20,60,0,1

[Events]
Format: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for n, zh, en in SUB_LINES:
        lines.append(f"Dialogue: Marked=0,0:00:{n:02d}.00,0:00:{n:02d}.90,Default,,0,0,0,,{zh}")
        lines.append(f"Dialogue: Marked=0,0:00:{n:02d}.00,0:00:{n:02d}.90,Top,,0,0,0,,{en}")
    return head + "\n".join(lines) + "\n"


def ass_text():
    head = """[Script Info]
Title: Fossil Frame ASS with attached font
ScriptType: v4.00+
PlayResX: 720
PlayResY: 480

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Pixel,Press Start 2P,20,&H0000FFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,8,20,20,70,1
Style: Default,Arial,28,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,2,20,20,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for n, zh, en in SUB_LINES:
        lines.append(f"Dialogue: 0,0:00:{n:02d}.00,0:00:{n:02d}.90,Pixel,,0,0,0,,"
                     f"PIXEL FONT = ATTACHMENT OK {n}")
        lines.append(f"Dialogue: 0,0:00:{n:02d}.00,0:00:{n:02d}.90,Default,,0,0,0,,"
                     f"{{\\c&H00FFFF&}}ASS{{\\c&HFFFFFF&}} {zh}")
    return head + "\n".join(lines) + "\n"


def microdvd_text(fps, header):
    lines = [f"{{1}}{{1}}{fps:g}"] if header else []
    for n, zh, en in SUB_LINES:
        start = round(n * fps)
        end = round((n + 0.9) * fps)
        lines.append(f"{{{start}}}{{{end}}}{zh}|{en}")
    return "\n".join(lines) + "\n"


# ---- VobSub (DVD SPU) writer -------------------------------------------

def render_text_bitmap(text, width, height):
    font = "/System/Library/Fonts/Hiragino Sans GB.ttc"
    if not Path(font).exists():
        font = base.FONT
    escaped = text.replace(":", "\\:").replace("'", "")
    result = subprocess.run([
        FFMPEG, "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
        f"color=black:s={width}x{height}:d=1",
        "-vf", f"drawtext=fontfile='{font}':text='{escaped}':fontcolor=white:"
               f"fontsize={int(height * 0.62)}:x=(w-text_w)/2:y=(h-text_h)/2:"
               "borderw=2:bordercolor=gray",
        "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    pixels = result.stdout
    rows = []
    for y in range(height):
        line = pixels[y * width:(y + 1) * width]
        # 0 transparent, 1 white text, 2 dark outline
        rows.append([1 if v > 170 else (2 if v > 40 else 0) for v in line])
    return rows


def rle_line(line, nibbles):
    start = len(nibbles)
    x = 0
    while x < len(line):
        color = line[x]
        run = 1
        while x + run < len(line) and line[x + run] == color and run < 255:
            run += 1
        if x + run >= len(line) and run > 63:
            nibbles += [0, 0, 0, color]  # until end of line
        elif run < 4:
            nibbles += [(run << 2) | color]
        elif run < 16:
            nibbles += [run >> 2, ((run & 3) << 2) | color]
        elif run < 64:
            nibbles += [0, run >> 2, ((run & 3) << 2) | color]
        else:
            nibbles += [0, run >> 6, (run >> 2) & 0xF, ((run & 3) << 2) | color]
        x += run
    if (len(nibbles) - start) & 1:
        nibbles.append(0)


def nibbles_to_bytes(nibbles):
    return bytes((nibbles[i] << 4) | nibbles[i + 1] for i in range(0, len(nibbles), 2))


def spu_packet(bitmap, x, y, duration):
    height = len(bitmap)
    width = len(bitmap[0])
    top, bottom = [], []
    for row_index in range(0, height, 2):
        rle_line(bitmap[row_index], top)
    for row_index in range(1, height, 2):
        rle_line(bitmap[row_index], bottom)
    top_bytes = nibbles_to_bytes(top)
    bottom_bytes = nibbles_to_bytes(bottom)
    top_offset = 4
    bottom_offset = top_offset + len(top_bytes)
    dcsq1 = bottom_offset + len(bottom_bytes)
    dcsq1_len = 4 + 3 + 3 + 7 + 5 + 1 + 1
    dcsq2 = dcsq1 + dcsq1_len
    x2 = x + width - 1
    y2 = y + height - 1
    seq1 = struct.pack(">HH", 0, dcsq2)
    # Pixel value -> palette index: bg(0)->0 black, pattern(1)->1 white,
    # emphasis1(2)->2 dark outline, emphasis2(3)->3. Nibble order: e2 e1 p b.
    seq1 += bytes([0x03, 0x32, 0x10])
    seq1 += bytes([0x04, 0xFF, 0xF0])          # alpha: e2 15, e1 15, p 15, bg 0
    seq1 += bytes([0x05, x >> 4, ((x & 0xF) << 4) | (x2 >> 8), x2 & 0xFF,
                   y >> 4, ((y & 0xF) << 4) | (y2 >> 8), y2 & 0xFF])
    seq1 += bytes([0x06]) + struct.pack(">HH", top_offset, bottom_offset)
    seq1 += bytes([0x01, 0xFF])
    assert len(seq1) == dcsq1_len, len(seq1)
    delay = round(duration * 90000 / 1024)
    seq2 = struct.pack(">HH", delay, dcsq2) + bytes([0x02, 0xFF])
    body = top_bytes + bottom_bytes + seq1 + seq2
    return struct.pack(">HH", 4 + len(body), dcsq1) + body


def pack_header(scr):
    b = bytearray(b"\x00\x00\x01\xba")
    b.append(0x44 | ((scr >> 27) & 0x38) | ((scr >> 28) & 0x03))
    b.append((scr >> 20) & 0xFF)
    b.append(((scr >> 12) & 0xF8) | 0x04 | ((scr >> 13) & 0x03))
    b.append((scr >> 5) & 0xFF)
    b.append(((scr & 0x1F) << 3) | 0x04)
    b.append(0x01)
    rate = 25200
    b += bytes([(rate >> 14) & 0xFF, (rate >> 6) & 0xFF, ((rate & 0x3F) << 2) | 0x03])
    b.append(0xF8)
    return bytes(b)


def pts_bytes(pts):
    return bytes([0x21 | ((pts >> 29) & 0x0E), (pts >> 22) & 0xFF,
                  ((pts >> 14) & 0xFE) | 1, (pts >> 7) & 0xFF, ((pts << 1) & 0xFE) | 1])


def vobsub_pack(spu, pts):
    """Split one SPU into 2048-byte MPEG-2 PS packs."""
    packs = []
    position = 0
    first = True
    while position < len(spu):
        header_data = pts_bytes(pts) if first else b""
        fixed = 14 + 6 + 3 + len(header_data) + 1
        chunk = spu[position:position + 2048 - fixed]
        position += len(chunk)
        leftover = 2048 - fixed - len(chunk)
        stuffing = b""
        padding = b""
        if 0 < leftover < 6:
            stuffing = b"\xff" * leftover
        elif leftover >= 6:
            padding = b"\x00\x00\x01\xbe" + struct.pack(">H", leftover - 6) + b"\xff" * (
                leftover - 6)
        pes_header = bytes([0x81, 0x80 if first else 0x00,
                            len(header_data) + len(stuffing)]) + header_data + stuffing
        payload = pes_header + b"\x20" + chunk
        pes = b"\x00\x00\x01\xbd" + struct.pack(">H", len(payload)) + payload
        pack = pack_header(pts) + pes + padding
        assert len(pack) == 2048, len(pack)
        packs.append(pack)
        first = False
    return b"".join(packs)


def write_vobsub(idx_path, width=720, height=480):
    sub_path = idx_path.with_suffix(".sub")
    sub = bytearray()
    entries = []
    bw, bh = 560, 44
    for n, zh, en in SUB_LINES:
        bitmap = render_text_bitmap(f"{zh}  VOBSUB {n}", bw, bh)
        spu = spu_packet(bitmap, (width - bw) // 2, height - bh - 24, 0.9)
        entries.append((n, len(sub)))
        sub += vobsub_pack(spu, n * 90000)
    sub_path.write_bytes(bytes(sub))
    palette = ["000000", "ffffff", "202020", "ffff00"] + ["808080"] * 12
    lines = [
        "# VobSub index file, v7 (do not modify this line!)",
        f"size: {width}x{height}", "org: 0, 0", "scale: 100%, 100%", "alpha: 100%",
        "smooth: OFF", "fadein/out: 0, 0", "align: OFF at LEFT TOP", "time offset: 0",
        "forced subs: OFF", "palette: " + ", ".join(palette),
        "custom colors: OFF, tridx: 0000, colors: 000000, 000000, 000000, 000000", "",
        "langidx: 0", "id: zh, index: 0",
    ]
    for n, pos in entries:
        lines.append(f"timestamp: 00:00:{n:02d}:000, filepos: {pos:09x}")
    idx_path.write_text("\n".join(lines) + "\n", encoding="ascii")
    return sub_path


@job
def subtitles(outdir):
    d = outdir / "subtitles"
    d.mkdir(parents=True, exist_ok=True)
    w, h, sar, fps = 720, 480, "32:27", 25
    ref = d / "subtitle_reference_mpeg4_mp3_720x480.avi"
    ff([*video_src(w, h, fps), *beep_src(),
        "-vf", vf(w, h, sar, "SUBTITLE SYNC: TEXT = SEC N AT BEEP", None, fps),
        "-map", "0:v", "-map", "1:a", *base.video_encoder("mpeg4"),
        *base.audio_encoder("mp3"), "-t", DURATION, "-f", "avi"], ref)
    row(f"subtitles/{ref.name}", "avi", "mpeg4", "mp3", f"{w}x{h}", sar, fps)

    stem = ref.with_suffix("")
    text = srt_text()
    for suffix, encoding, bom in (("gbk", "gbk", b""), ("big5", "big5", b""),
                                  ("utf8bom", "utf-8", b"\xef\xbb\xbf"),
                                  ("utf16le", "utf-16-le", b"\xff\xfe")):
        path = Path(f"{stem}.{suffix}.srt")
        path.write_bytes(bom + text.replace("\n", "\r\n").encode(encoding))
        row(f"subtitles/{path.name}", "srt", "", f"subrip {encoding}")
    path = Path(f"{stem}.ssa")
    path.write_bytes(b"\xef\xbb\xbf" + ssa_text().replace("\n", "\r\n").encode("utf-8"))
    row(f"subtitles/{path.name}", "ssa", "", "ssa v4 utf-8")
    path = Path(f"{stem}.microdvd-25fps.sub")
    path.write_text(microdvd_text(25, False), encoding="utf-8")
    row(f"subtitles/{path.name}", "microdvd", "", "frame-based, assumes video fps 25")
    path = Path(f"{stem}.microdvd-23.976fps-header.sub")
    path.write_text(microdvd_text(23.976, True), encoding="utf-8")
    row(f"subtitles/{path.name}", "microdvd", "", "frame-based, {1}{1}23.976 header")
    idx = Path(f"{stem}.vobsub.idx")
    sub = write_vobsub(idx, w, h)
    row(f"subtitles/{idx.name}", "vobsub", "", "dvd_subtitle index")
    row(f"subtitles/{sub.name}", "vobsub", "", "dvd_subtitle stream")

    with tempfile.TemporaryDirectory() as tmp:
        srt = Path(tmp) / "zh.srt"
        srt.write_text(text, encoding="utf-8")
        ass = Path(tmp) / "en.ass"
        ass.write_text(ass_text(), encoding="utf-8")

        out = d / "mkv_srt-zho_ass-fontattach_vobsub_720x480.mkv"
        ff(["-i", ref, "-i", srt, "-i", ass, "-i", idx,
            "-map", "0:v", "-map", "0:a", "-map", "1", "-map", "2", "-map", "3",
            "-c:v", "copy", "-c:a", "copy", "-c:s:0", "srt", "-c:s:1", "ass",
            "-c:s:2", "copy",
            "-metadata:s:s:0", "language=zho", "-metadata:s:s:0", "title=SRT 中文",
            "-metadata:s:s:1", "language=eng", "-metadata:s:s:1", "title=ASS attached font",
            "-metadata:s:s:2", "language=zho", "-metadata:s:s:2", "title=VobSub bitmap",
            "-disposition:s:0", "default",
            "-attach", FONT_ATTACHMENT, "-metadata:s:t", "mimetype=font/ttf",
            "-metadata:s:t", f"filename={FONT_ATTACHMENT.name}", "-f", "matroska"], out)
        row(f"subtitles/{out.name}", "matroska", "mpeg4", "mp3 + srt/ass/dvdsub + ttf",
            f"{w}x{h}", sar, fps)

    out = d / "dvd_mpeg2_ac3_vobsub_720x480.vob"
    ff([*video_src(w, h, "29.97"), *beep_src(), "-i", idx,
        "-vf", vf(w, h, sar, "DVD VOB + SUBPICTURE STREAM", None, "29.97"),
        "-map", "0:v", "-map", "1:a", "-map", "2:s", *base.video_encoder("mpeg2video"),
        *base.audio_encoder("ac3"), "-c:s", "copy", "-t", DURATION, "-f", "dvd"], out)
    row(f"subtitles/{out.name}", "dvd", "mpeg2video", "ac3 + dvd_subtitle", f"{w}x{h}", sar,
        "29.97")

    out = d / "mpegts_mpeg2_mp2_dvbsub_720x480.ts"
    ff([*video_src(w, h, 25), *beep_src(), "-i", idx,
        "-vf", vf(w, h, sar, "MPEG-TS + DVB SUBTITLES", None, 25),
        "-map", "0:v", "-map", "1:a", "-map", "2:s", *base.video_encoder("mpeg2video"),
        *base.audio_encoder("mp2"), "-c:s", "dvbsub", "-metadata:s:s:0", "language=zho",
        "-t", DURATION, "-f", "mpegts"], out)
    row(f"subtitles/{out.name}", "mpegts", "mpeg2video", "mp2 + dvb_subtitle", f"{w}x{h}",
        sar, 25)


# ------------------------------------------------------------- structure/

def simple_av(out, w, h, fps, title, fmt, vcodec="mpeg4", acodec="mp3", sar="1:1",
              extra_in=(), extra_out=(), vtail=None):
    ff([*video_src(w, h, fps), *beep_src(), *extra_in,
        "-vf", vf(w, h, sar, title, vtail, fps), "-map", "0:v", "-map", "1:a",
        *base.video_encoder(vcodec), *base.audio_encoder(acodec), *extra_out,
        "-t", DURATION, "-f", fmt], out)


@job
def structure_index(outdir):
    d = outdir / "structure"
    d.mkdir(parents=True, exist_ok=True)

    out = d / "mkv_no_cues_written_to_pipe_320x240.mkv"
    with out.open("wb") as handle:
        cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", *video_src(320, 240, 25),
               *beep_src(), "-vf", vf(320, 240, "1:1", "MKV WITHOUT CUES (SEEK)", None, 25),
               "-map", "0:v", "-map", "1:a", *base.video_encoder("mpeg4"),
               *base.audio_encoder("mp3"), "-t", str(DURATION), "-f", "matroska", "pipe:1"]
        subprocess.run(cmd, stdout=handle, check=True)
    row(f"structure/{out.name}", "matroska", "mpeg4", "mp3", "320x240", "1:1", 25)

    out = d / "mp4_faststart_moov_first_640x360.mp4"
    simple_av(out, 640, 360, 25, "MP4 FASTSTART (MOOV FIRST)", "mp4",
              extra_out=["-movflags", "+faststart"])
    row(f"structure/{out.name}", "mp4", "mpeg4", "mp3", "640x360", "1:1", 25)

    # Non-interleaved AVI: every video chunk first, all audio at the end.
    out = d / "avi_noninterleaved_audio_at_end_320x240.avi"
    simple_av(out, 320, 240, 15, "AVI NOT INTERLEAVED", "avi")
    chunks = avi_read(out)
    items, flags = avi_movi_and_flags(chunks)
    order = ([i for i, it in enumerate(items) if it[0].endswith(b"dc")] +
             [i for i, it in enumerate(items) if not it[0].endswith(b"dc")])
    avi_write(out, chunks, [items[i] for i in order], [flags[i] for i in order])
    row(f"structure/{out.name}", "avi", "mpeg4", "mp3", "320x240", "1:1", 15)

    # Zero-length video chunks (VirtualDub / capture style dropped frames).
    out = d / "avi_zero_length_dropped_frame_chunks_320x240.avi"
    ff([*video_src(320, 240, 25), *beep_src(),
        "-vf", vf(320, 240, "1:1", "ZERO-LENGTH DROP CHUNKS 3-4S", [
            "select='not(between(t\\,3\\,4)*mod(n\\,2))'"], 25),
        "-map", "0:v", "-map", "1:a", *base.video_encoder("mpeg4"),
        *base.audio_encoder("mp3"), "-fps_mode", "passthrough", "-t", DURATION,
        "-f", "avi"], out)
    items, _ = avi_movi_and_flags(avi_read(out))
    if not any(fid.endswith(b"dc") and not payload for fid, payload in items):
        raise RuntimeError("AVI muxer wrote no zero-length chunks")
    row(f"structure/{out.name}", "avi", "mpeg4", "mp3", "320x240", "1:1", 25)

    # DivX 5 style packed B-frames.
    out = d / "avi_divx5_packed_bframes_mpeg4_mp3_480x360.avi"
    ff([*video_src(480, 360, 25), *beep_src(),
        "-vf", vf(480, 360, "1:1", "DIVX5 PACKED B-FRAMES", None, 25),
        "-map", "0:v", "-map", "1:a", "-c:v", "mpeg4", "-q:v", "5", "-bf", "1",
        "-vtag", "DX50", *base.audio_encoder("mp3"), "-t", DURATION, "-f", "avi"], out)
    pack_bframes(out, time_increment_bits=5)
    row(f"structure/{out.name}", "avi", "mpeg4 packed", "mp3", "480x360", "1:1", 25)


def vop_type(payload):
    position = payload.find(b"\x00\x00\x01\xb6")
    if position < 0 or position + 4 >= len(payload):
        return None
    return "IPBS"[payload[position + 4] >> 6]


def nvop(time_increment_bits):
    bits = "01" + "0" + "1" + "0" * time_increment_bits + "1" + "0"
    bits += "0" + "1" * ((8 - (len(bits) + 1) % 8) % 8)
    return b"\x00\x00\x01\xb6" + int(bits, 2).to_bytes(len(bits) // 8, "big")


def pack_bframes(path, time_increment_bits):
    chunks = avi_read(path)
    items, flags = avi_movi_and_flags(chunks)
    video = [i for i, it in enumerate(items) if it[0].endswith(b"dc") and it[1]]
    packed = 0
    for a, b in zip(video, video[1:]):
        if vop_type(items[a][1]) in ("I", "P") and vop_type(items[b][1]) == "B":
            items[a][1] = items[a][1] + items[b][1]
            items[b][1] = nvop(time_increment_bits)
            packed += 1
    first = items[video[0]][1]
    vop = first.find(b"\x00\x00\x01\xb6")
    items[video[0]][1] = first[:vop] + b"\x00\x00\x01\xb2DivX503b1393p" + first[vop:]
    if not packed:
        raise RuntimeError("no B-frames to pack")
    avi_write(path, chunks, items, flags)


@job
def structure_timing(outdir):
    d = outdir / "structure"

    out = d / "mpegts_pts_wrap_33bit_at_3.7s_480x480.ts"
    simple_av(out, 480, 480, "29.97", "PTS WRAPS 2^33 AT ~3.7S", "mpegts",
              vcodec="mpeg2video", acodec="ac3", extra_out=["-output_ts_offset", "95440"])
    row(f"structure/{out.name}", "mpegts", "mpeg2video", "ac3", "480x480", "1:1", "29.97")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # Resolution / aspect switches in one TS (broadcast ad-break style).
        segs = [(720, 480, "8:9", "4:3"), (720, 480, "32:27", "16:9"),
                (352, 240, "10:11", "352 SD")]
        parts = []
        for k, (w, h, sar, label) in enumerate(segs):
            part = tmp / f"seg{k}.ts"
            ff([*video_src(w, h, "29.97"), *beep_src(),
                "-vf", vf(w, h, sar, f"TS SWITCH {k + 1}/3: {w}x{h} {label}", None, "29.97"),
                "-map", "0:v", "-map", "1:a", *base.video_encoder("mpeg2video"),
                *base.audio_encoder("mp2"), "-ss", k * 4, "-t", 4,
                "-output_ts_offset", 1.4 + k * 4, "-f", "mpegts"], part)
            parts.append(part)
        out = d / "mpegts_resolution_aspect_switch_720x480-4x3_16x9_352x240.ts"
        out.write_bytes(b"".join(p.read_bytes() for p in parts))
        row(f"structure/{out.name}", "mpegts", "mpeg2video", "mp2", "720x480/352x240",
            "8:9/32:27/10:11", "29.97")

        parts = []
        for k, rate in enumerate((48000, 44100, 32000)):
            part = tmp / f"aseg{k}.ts"
            ff([*video_src(320, 240, 25), *beep_src(rate=rate),
                "-vf", vf(320, 240, "1:1", f"AUDIO RATE {rate} HZ", None, 25),
                "-map", "0:v", "-map", "1:a", *base.video_encoder("mpeg2video"),
                "-c:a", "mp2", "-b:a", "160k", "-ar", rate, "-ac", "2",
                "-ss", k * 4, "-t", 4, "-output_ts_offset", 1.4 + k * 4, "-f", "mpegts"], part)
            parts.append(part)
        out = d / "mpegts_audio_samplerate_switch_48k_44k_32k_320x240.ts"
        out.write_bytes(b"".join(p.read_bytes() for p in parts))
        row(f"structure/{out.name}", "mpegts", "mpeg2video", "mp2 48/44.1/32 kHz", "320x240",
            "1:1", 25)

        # VOB_01 + VOB_02 style concatenation: timestamps restart at the joint.
        parts = []
        for k in range(2):
            part = tmp / f"vob{k}.vob"
            ff([*video_src(720, 480, "29.97"), *beep_src(),
                "-vf", vf(720, 480, "32:27", f"VTS_01_{k + 1}.VOB  TIMESTAMP RESET", None,
                          "29.97"),
                "-map", "0:v", "-map", "1:a", *base.video_encoder("mpeg2video"),
                *base.audio_encoder("ac3"), "-ss", k * 6, "-t", 6, "-f", "dvd"], part)
            parts.append(part)
        out = d / "concat_vts_01_1_plus_2_timestamp_reset_720x480.vob"
        out.write_bytes(b"".join(p.read_bytes() for p in parts))
        row(f"structure/{out.name}", "dvd", "mpeg2video", "ac3", "720x480", "32:27", "29.97")

        # Binary cat of an NTSC VCD and a PAL VCD.
        parts = []
        for k, (h, fps) in enumerate(((240, "29.97"), (288, 25))):
            part = tmp / f"vcd{k}.mpg"
            ff([*video_src(352, h, fps), *beep_src(rate=44100),
                "-vf", vf(352, h, "1:1", f"CAT PART {k + 1}: 352x{h} {fps}FPS", None, fps),
                "-map", "0:v", "-map", "1:a", "-ss", k * 6, "-t", 6, "-f", "vcd"], part)
            parts.append(part)
        out = d / "concat_cat_vcd_ntsc_352x240_plus_pal_352x288.mpg"
        out.write_bytes(b"".join(p.read_bytes() for p in parts))
        row(f"structure/{out.name}", "vcd", "mpeg1video", "mp2", "352x240/352x288", "1:1",
            "29.97/25")

        # Hybrid VFR: 0-6 s at 23.976, 6-12 s at 29.97.
        parts = []
        for k, fps in enumerate(("23.976", "29.97")):
            part = tmp / f"vfr{k}.mkv"
            ff([*video_src(640, 360, fps),
                "-vf", vf(640, 360, "1:1", f"VFR HYBRID {fps} FPS", None, fps),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p",
                "-bf", "0", "-ss", k * 6, "-t", 6, "-f", "matroska"], part)
            parts.append(part)
        concat = tmp / "concat.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in parts))
        audio = tmp / "beep.m4a"
        ff([*beep_src(), "-c:a", "aac", "-b:a", "96k", "-t", DURATION], audio)
        for fmt, ext in (("matroska", "mkv"), ("mp4", "mp4")):
            out = d / f"{ext}_vfr_hybrid_23.976_then_29.97_h264_640x360.{ext}"
            ff(["-f", "concat", "-safe", "0", "-i", concat, "-i", audio,
                "-map", "0:v", "-map", "1:a", "-c", "copy", "-f", fmt], out)
            row(f"structure/{out.name}", fmt, "h264 vfr", "aac", "640x360", "1:1",
                "23.976+29.97")

    out = d / "mkv_video_starts_0.5s_after_audio_320x240.mkv"
    simple_av(out, 320, 240, 25, "VIDEO STARTS AT 0.5S", "matroska",
              vtail=["trim=start=0.5"])
    row(f"structure/{out.name}", "matroska", "mpeg4", "mp3", "320x240", "1:1", 25)

    out = d / "mkv_audio_timestamp_gap_4s-5s_320x240.mkv"
    ff([*video_src(320, 240, 25), *beep_src(),
        "-vf", vf(320, 240, "1:1", "AUDIO PACKETS MISSING 4-5S", None, 25),
        "-af", "aselect='not(between(t\\,4\\,5))'",
        "-map", "0:v", "-map", "1:a", *base.video_encoder("mpeg4"),
        "-c:a", "libvorbis", "-q:a", "3", "-t", DURATION, "-f", "matroska"], out)
    row(f"structure/{out.name}", "matroska", "mpeg4", "vorbis", "320x240", "1:1", 25)

    out = d / "mkv_video_timestamp_gap_4s-5s_320x240.mkv"
    ff([*video_src(320, 240, 25), *beep_src(),
        "-vf", vf(320, 240, "1:1", "VIDEO FROZEN 4-5S (NO FRAMES)",
                  ["select='not(between(t\\,4\\,4.99))'"], 25),
        "-map", "0:v", "-map", "1:a", *base.video_encoder("mpeg4"),
        *base.audio_encoder("mp3"), "-fps_mode", "passthrough", "-t", DURATION,
        "-f", "matroska"], out)
    row(f"structure/{out.name}", "matroska", "mpeg4", "mp3", "320x240", "1:1", 25)

    out = d / "mov_editlist_empty_first_1s_320x240.mov"
    ff([*video_src(320, 240, 25), *beep_src(),
        "-vf", vf(320, 240, "1:1", "MOV EMPTY EDIT: BLACK 0-1S", ["trim=start=1"], 25),
        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "28", "-bf", "2", "-c:a", "aac", "-b:a", "96k", "-t", DURATION,
        "-f", "mov"], out)
    row(f"structure/{out.name}", "mov", "h264", "aac", "320x240", "1:1", 25)


@job
def structure_metadata(outdir):
    d = outdir / "structure"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # Rotation: stored frames are turned; display matrix turns them back.
        for name, fmt, rotate, transpose, w, h, acodec in (
                ("mp4_display_rotation_90_h264_aac_360x640.mp4", "mp4", 90, "clock",
                 640, 360, ["-c:a", "aac", "-b:a", "96k"]),
                ("3gp_display_rotation_270_h263_amrnb_176x144.3gp", "3gp", 270, "cclock",
                 176, 144, base.audio_encoder("amr_nb"))):
            raw = tmp / f"raw.{fmt}"
            vcodec = (["-c:v", "libx264", "-preset", "veryfast", "-crf", "27"]
                      if fmt == "mp4" else base.video_encoder("h263"))
            stored_w, stored_h = (h, w)
            if fmt == "3gp":
                # H.263 needs a legal picture size, so draw in portrait 144x176
                # and store as landscape 176x144.
                w, h = 144, 176
                stored_w, stored_h = 176, 144
            ff([*video_src(w, h, 15), *beep_src(),
                "-vf", vf(w, h, "1:1", f"UPRIGHT IF ROT {rotate} OK", [f"transpose={transpose}"],
                          15),
                "-map", "0:v", "-map", "1:a", *vcodec, *acodec,
                "-t", DURATION, "-f", fmt], raw)
            out = d / name
            ff(["-display_rotation:v:0", rotate, "-i", raw, "-c", "copy", "-f", fmt], out)
            row(f"structure/{out.name}", fmt, vcodec[1], acodec[1],
                f"{stored_w}x{stored_h}", "1:1", 15)

        meta = tmp / "chapters.txt"
        chapter_lines = [";FFMETADATA1", "title=Fossil Frame 章节测试"]
        for k in range(4):
            chapter_lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={k * 3000}",
                              f"END={(k + 1) * 3000}", f"title=第 {k + 1} 章 / sec {k * 3}"]
        meta.write_text("\n".join(chapter_lines) + "\n", encoding="utf-8")
        for fmt, ext in (("matroska", "mkv"), ("mp4", "mp4")):
            out = d / f"{ext}_chapters_every_3s_320x240.{ext}"
            ff([*video_src(320, 240, 25), *beep_src(), "-i", meta,
                "-vf", vf(320, 240, "1:1", "CHAPTERS AT 0/3/6/9 S", None, 25),
                "-map", "0:v", "-map", "1:a", "-map_metadata", "2", "-map_chapters", "2",
                *base.video_encoder("mpeg4"), *base.audio_encoder("mp3"),
                "-t", DURATION, "-f", fmt], out)
            row(f"structure/{out.name}", fmt, "mpeg4", "mp3", "320x240", "1:1", 25)

    # GBK titles in legacy metadata fields (patched in place, same byte length).
    title = "老电影 测试 GBK 标题".encode("gbk")
    placeholder = ("Z" * len(title)).encode()
    for name, fmt, vcodec, acodec in (("avi_info_title_gbk_320x240.avi", "avi", "mpeg4", "mp3"),
                                      ("rm_title_gbk_rv10_320x240.rm", "rm", "rv10", "ac3")):
        out = d / name
        simple_av(out, 320, 240, 15, "TITLE TAG IS GBK BYTES", fmt, vcodec=vcodec,
                  acodec=acodec, extra_out=["-metadata", f"title={placeholder.decode()}"])
        data = out.read_bytes()
        if data.count(placeholder) != 1:
            raise RuntimeError(f"title placeholder not unique in {name}")
        out.write_bytes(data.replace(placeholder, title))
        row(f"structure/{out.name}", fmt, vcodec, acodec, "320x240", "1:1", 15)

    # Colour matrix tags versus resolution-based guessing.
    color_cases = [
        ("mkv_sd_720x576_bt709_tagged_mpeg2.mkv", 720, 576, "64:45", "bt709", True,
         "mpeg2video", "SD BUT BT.709 TAGGED"),
        ("mkv_hd_1280x720_bt709_untagged_h264.mkv", 1280, 720, "1:1", "bt709", False,
         "h264", "HD BT.709 UNTAGGED"),
        ("mkv_hd_1280x720_bt601_tagged_h264.mkv", 1280, 720, "1:1", "bt470bg", True,
         "h264", "HD BUT BT.601 TAGGED"),
    ]
    for name, w, h, sar, matrix, tagged, vcodec, title in color_cases:
        out = d / name
        if tagged:
            primaries = "bt709" if matrix == "bt709" else "bt470bg"
            trc = "bt709" if matrix == "bt709" else "smpte170m"
            params = (f"setparams=range=tv:colorspace={matrix}:"
                      f"color_primaries={primaries}:color_trc={trc}")
        else:
            params = ("setparams=range=unknown:colorspace=unknown:"
                      "color_primaries=unknown:color_trc=unknown")
        venc = (["-c:v", "libx264", "-preset", "veryfast", "-crf", "28"]
                if vcodec == "h264" else base.video_encoder(vcodec))
        ff([*video_src(w, h, 25), *beep_src(),
            "-vf", vf(w, h, sar, title,
                      [f"scale=out_color_matrix={matrix}:out_range=tv", "format=yuv420p",
                       params], 25),
            "-map", "0:v", "-map", "1:a", *venc, *base.audio_encoder("ac3"),
            "-t", DURATION, "-f", "matroska"], out)
        row(f"structure/{out.name}", "matroska", vcodec, "ac3", f"{w}x{h}", sar, 25)


@job
def structure_interlaced_hd(outdir):
    d = outdir / "structure"
    out = d / "m2ts_h264_mbaff_tff_ac3_1440x1080i_sar4-3.m2ts"
    ff([*video_src(1440, 1080, "59.94"), *beep_src(),
        "-vf", vf(1440, 1080, "4:3", "AVCHD-STYLE H.264 MBAFF TFF",
                  ["tinterlace=mode=interleave_top", "setfield=tff"], "59.94"),
        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "30", "-flags", "+ildct+ilme", "-x264-params", "interlaced=1:tff=1",
        "-c:a", "ac3", "-b:a", "192k", "-t", DURATION, "-mpegts_m2ts_mode", "1",
        "-f", "mpegts"], out)
    row(f"structure/{out.name}", "m2ts", "h264 mbaff", "ac3", "1440x1080", "4:3", "29.97i")

    out = d / "hdv_mpeg2_tff_mp2_1440x1080i_sar4-3.m2t"
    ff([*video_src(1440, 1080, "59.94"), *beep_src(),
        "-vf", vf(1440, 1080, "4:3", "HDV MPEG-2 1080I TFF",
                  ["tinterlace=mode=interleave_top", "setfield=tff"], "59.94"),
        "-map", "0:v", "-map", "1:a", "-c:v", "mpeg2video", "-q:v", "9", "-g", "15",
        "-flags", "+ildct+ilme", "-field_order", "tt",
        "-c:a", "mp2", "-b:a", "384k", "-ar", "48000", "-t", DURATION, "-f", "mpegts"], out)
    row(f"structure/{out.name}", "mpegts", "mpeg2video", "mp2", "1440x1080", "4:3", "29.97i")


@job
def structure_edge(outdir):
    d = outdir / "structure"
    out = d / "mkv_single_frame_320x240.mkv"
    ff([*video_src(320, 240, 25, 1),
        "-vf", vf(320, 240, "1:1", "ONLY ONE FRAME", None, 25),
        *base.video_encoder("mpeg4"), "-frames:v", "1", "-f", "matroska"], out)
    row(f"structure/{out.name}", "matroska", "mpeg4", "", "320x240", "1:1", 25)

    out = d / "avi_audio_only_mp3.avi"
    ff([*beep_src(), "-map", "0:a", *base.audio_encoder("mp3"), "-f", "avi"], out)
    row(f"structure/{out.name}", "avi", "", "mp3")

    out = d / "avi_video_only_msmpeg4v3_320x240.avi"
    ff([*video_src(320, 240, 15),
        "-vf", vf(320, 240, "1:1", "NO AUDIO STREAM", None, 15),
        *base.video_encoder("msmpeg4v3"), "-f", "avi"], out)
    row(f"structure/{out.name}", "avi", "msmpeg4v3", "", "320x240", "1:1", 15)


# ----------------------------------------------------------- mislabeled/

MISLABELED = [
    ("normal/mkv_mpeg4asp_mp3_352x288_sar64-45.mkv", "actually_mkv_named.rmvb"),
    ("normal/mpeg1_mpeg1video_mp2_352x240.mpg", "actually_mpegps_named.avi"),
    ("normal/avi_msmpeg4v3_mp3_320x240.avi", "actually_avi_named.wmv"),
    ("normal/rm_rv10_ac3_320x240.rm", "actually_rm_named.avi"),
    ("normal/flv_flv1_mp3_320x240.flv", "actually_flv_named.mp4"),
    ("normal/mp4_mpeg4asp_mp3_160x106.mp4", "actually_mp4_named.3gp.avi"),
]


@job
def mislabeled(outdir):
    d = outdir / "mislabeled"
    d.mkdir(parents=True, exist_ok=True)
    for source, name in MISLABELED:
        shutil.copyfile(outdir / source, d / name)
        row(f"mislabeled/{name}", f"real: {Path(source).suffix[1:]}", "copy", "copy")


# ---------------------------------------------------------------- damage/

def zero_holes(data, piece, indices):
    data = bytearray(data)
    for index in indices:
        start = index * piece
        if start < len(data):
            data[start:start + piece] = bytes(min(piece, len(data) - start))
    return bytes(data)


@job
def damage_download(outdir):
    d = outdir / "damage"
    (d / "damage_zero_byte_empty_file.avi").write_bytes(b"")
    row("damage/damage_zero_byte_empty_file.avi", ".avi", "empty", "empty")

    for source in ("normal/avi_mpeg4asp_mp3_352x288_sar12-11.avi",
                   "normal/mkv_mpeg2video_ac3_720x480_sar32-27.mkv",
                   "normal/rm_rv20_ac3_320x240.rmvb"):
        src = outdir / source
        data = src.read_bytes()
        pieces = len(data) // 65536
        name = f"damage_p2p_zero_holes_{src.name}"
        (d / name).write_bytes(zero_holes(data, 65536, (pieces // 3, (pieces * 2) // 3)))
        row(f"damage/{name}", src.suffix, "zero_filled_64k_pieces", "")

    for source in ("normal/mpeg1_mpeg1video_mp2_352x240.mpg",
                   "normal/mpegts_mpeg2video_ac3_480x480_29-97.mpegts",
                   "normal/avi_msmpeg4v3_mp3_320x240.avi",
                   "normal/mkv_vp8_vorbis_320x240.mkv"):
        src = outdir / source
        name = f"damage_headless_first64k_{src.name}"
        (d / name).write_bytes(src.read_bytes()[65536:])
        row(f"damage/{name}", src.suffix, "first_64k_missing", "")

    src = outdir / "normal/avi_msmpeg4v3_mp3_320x240.avi"
    chunks = avi_read(src)
    items, flags = avi_movi_and_flags(chunks)
    out = d / "damage_noidx1_avi_msmpeg4v3_mp3_320x240.avi"
    avi_write(out, chunks, items, flags, write_index=False)
    row(f"damage/{out.name}", ".avi", "idx1_removed", "")

    out = d / "damage_badidx1_offsets_avi_msmpeg4v3_mp3_320x240.avi"
    avi_write(out, chunks, items, flags)
    data = bytearray(out.read_bytes())
    idx_pos = data.rfind(b"idx1")
    count = struct.unpack("<I", data[idx_pos + 4:idx_pos + 8])[0] // 16
    for i in range(count // 3, count):
        entry = idx_pos + 8 + i * 16
        offset = struct.unpack("<I", data[entry + 8:entry + 12])[0]
        data[entry + 8:entry + 12] = struct.pack("<I", offset + 4093)
    out.write_bytes(bytes(data))
    row(f"damage/{out.name}", ".avi", "idx1_offsets_shifted", "")

    src = outdir / "structure/mp4_faststart_moov_first_640x360.mp4"
    data = src.read_bytes()
    name = f"damage_trunc_{src.name}"
    (d / name).write_bytes(data[:int(len(data) * 0.97)])
    row(f"damage/{name}", ".mp4", "truncated_3pct_moov_first", "")


# -------------------------------------------------------------- manifest

def merge_manifest(outdir):
    path = outdir / "manifest.csv"
    fields = ["file", "container", "video_codec", "audio_codec", "pixels",
              "sample_aspect_ratio", "fps", "bytes"]
    old = []
    if path.exists():
        with path.open(newline="", encoding="utf-8") as handle:
            old = list(csv.DictReader(handle))
    new_files = {r["file"] for r in ROWS}
    kept = [r for r in old if r["file"] not in new_files]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(kept + ROWS)


def main():
    global VERBOSE, FFMPEG
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=ROOT / "dataset")
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--only", nargs="*", help="run only these job functions")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    VERBOSE = args.verbose
    FFMPEG = args.ffmpeg
    jobs = [legacy_codecs, audio_tracks, subtitles, structure_index, structure_timing,
            structure_metadata, structure_interlaced_hd, structure_edge, mislabeled,
            damage_download]
    for directory in ("normal", "damage", "structure"):
        (args.outdir / directory).mkdir(parents=True, exist_ok=True)
    for fn in jobs:
        if args.only and fn.__name__ not in args.only:
            continue
        fn(args.outdir)
    merge_manifest(args.outdir)
    print(f"\nGenerated {len(ROWS)} extra items; {len(FAILURES)} job groups failed.")
    for failure in FAILURES:
        print(f"  {failure.splitlines()[0]}")
    sys.exit(1 if FAILURES else 0)


if __name__ == "__main__":
    main()
