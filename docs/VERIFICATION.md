English | [中文](VERIFICATION.zh-CN.md)

# Generation and verification record

[← Back to README](../README.md)

- Generated: 2026-11-17.
- Environment: macOS/arm64; FFmpeg 9.0.2.
- FFmpeg libraries: libx264, libx265, libxvid, libtheora, libvorbis, libvpx,
  libmp3lame, libopencore-amrnb, libspeex and others.
- File counts: normal 50, degraded 10, damage 21, tracks 6, subtitles 13,
  structure 30, mislabeled 6; 136 total, all listed in `dataset/manifest.csv`.

## What `tools/verify.sh` checks

| Category | Check |
|---|---|
| `normal/` | `ffmpeg -v error -i FILE -f null -` must print nothing and exit 0 |
| `degraded/`, `tracks/`, `structure/`, `mislabeled/` | The decode process must exit successfully (warnings allowed) |
| `subtitles/` | Containers read fully; every external subtitle parses with the right `-sub_charenc` |
| `damage/` | Decoding is not checked, only that the manifest is complete |

## Spot checks from this run

- SAR/DAR: the non-square SARs in `asf/mkv/dvd/mpeg2` stay 32:27 or 64:45; MPEG-4
  ASP in AVI stays 12:11; MPEG-4 ASP in MOV stays 16:15.
- FFV1/NUT keeps exactly 161×107; FFV1/MKV keeps exactly 227×127.
- Field order: MOV DV probes as `bt`, M2TS/HDV as `tt`; AVI DV carries field order
  only inside the DV bitstream, so the container probes as `unknown`.
- Rotation: MP4 side-data rotation is 90, 3GP is −90 (i.e. 270). Extracted frames
  confirm the text is upright.
- Color tags: the SD-tagged-BT.709, HD-tagged-BT.601 and HD-untagged samples all
  match their file names.
- VFR: the MKV/MP4 hybrid samples decode to 324 frames (6 s × 23.976 +
  6 s × 29.97). `-f null` with its default CFR output prints
  "non monotonically increasing dts"; with `-fps_mode passthrough` or
  `-f framemd5` there are no messages.
- Audio gap: no audio packets between 4.008 s and 5.013 s.
- Packed B-frames: FFmpeg detects packing and decodes 300 frames.
- Subtitles: MKV has 11 SRT, 22 ASS and 11 VobSub packets; DVB has 22 (display +
  clear). Extracted frames confirm both the VobSub bitmaps and the attached ASS
  pixel font render correctly.
- GBK metadata: AVI and RM each contain one verbatim GBK-encoded title.
- AC-3/DTS 5.1 VOB: FFmpeg's PS muxer leaves one packet with a duplicate DTS at
  the end of the file; decoding prints 1–5 messages and the content is complete.

## How damage/ behaves with FFmpeg 9.0.2

| File | Exit | Frames decoded |
|---|---|---|
| `damage_headless_first64k_*.mpg` | 0 | 276 / 288 |
| `damage_headless_first64k_*.mpegts` | 0 | 348 / 360 |
| `damage_headless_first64k_*.avi`, `*.mkv` | non-zero (not recognized) | — |
| `damage_noidx1_*`, `damage_badidx1_*` | 0 | 180 / 180 |
| `damage_trunc_mp4_faststart_*` | 0 | 289 / 300 |
| `damage_trunc_mp4_mpeg4asp_*` (moov at the end) | non-zero | — |
| `damage_p2p_zero_holes_*.avi` / `.mkv` / `.rmvb` | 0 | 278 / 338 / 145 |

## Commands for re-checking

```bash
./tools/verify.sh
ffprobe -hide_banner -show_format -show_streams dataset/normal/FILE
ffmpeg -hide_banner -v error -i dataset/normal/FILE -f null -
```
