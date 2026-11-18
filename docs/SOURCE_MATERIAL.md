English | [中文](SOURCE_MATERIAL.zh-CN.md)

# Source material

[← Back to README](../README.md)

`dataset/` uses no external photos, music videos, downloaded footage or
third-party media files:

- Pictures are synthesized live from FFmpeg's `testsrc2` and `color` sources and
  the `drawtext`/`drawbox`/`drawgrid` filters; `degraded/` adds filters such as
  `noise`, `rgbashift`, `chromashift`, `lagfun`, `tmix` and `tinterlace`.
- All audio is synthesized with `aevalsrc`: a short beep every second (1 kHz by
  default). Multi-track and channel-ID samples use beeps of different pitches.
- Subtitle text is written by `generate_extra.py`; VobSub/DVB bitmaps are
  rendered by the generator with `drawtext` and then encoded.
- The `damage/` and `mislabeled/` samples and some of `structure/` come from
  deterministic byte edits, truncation, concatenation or reordering of the
  synthesized files above.

On-screen text is rendered with local system fonts (macOS Arial, Hiragino Sans
GB, …; override with `SUITE_FONT`). Fonts are only used to produce pixels; no
font file goes into the dataset.

## Bundled third-party font

`assets/fonts/PressStart2P-Regular.ttf` is embedded as an MKV attachment in
`dataset/subtitles/mkv_srt-zho_ass-fontattach_vobsub_720x480.mkv` to test
attached-font loading. The font is Copyright 2012 The Press Start 2P Project
Authors, released under the SIL Open Font License 1.1, which permits
redistribution with software. The full license text is in
`assets/fonts/OFL.txt`.

## Reference snapshots

`docs/references/` holds Markdown snapshots of the external pages cited in the
docs, taken on 2026-11-17 so the citations survive link rot. Each one is linked
next to its original URL. They are third-party content: copyright stays with
their authors and publishers, and they are **not** covered by this repository's
MIT license. Each snapshot starts with a header naming its source.

## Illustrations

`assets/aspect_preview.png` and `assets/degradation_preview.png` are frames
extracted from the dataset for documentation; they are not generator input.

## Regenerating

```bash
python3 generate_suite.py --outdir dataset
python3 generate_degradation.py --outdir dataset
python3 generate_extra.py --outdir dataset
./tools/verify.sh
```
