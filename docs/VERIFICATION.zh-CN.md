[English](VERIFICATION.md) | 中文

# 生成与验收记录

[← 返回 README](../README.zh-CN.md)

- 生成日期：2026-11-17。
- 生成环境：macOS/arm64；FFmpeg 9.0.2。
- FFmpeg 启用库：libx264、libx265、libxvid、libtheora、libvorbis、libvpx、
  libmp3lame、libopencore-amrnb、libspeex 等。
- 文件数：normal 50、degraded 10、damage 21、tracks 6、subtitles 13、
  structure 30、mislabeled 6，共 136 个，均已登记到 `dataset/manifest.csv`。

## `tools/verify.sh` 的判定

| 类别 | 判定 |
|---|---|
| `normal/` | `ffmpeg -v error -i FILE -f null -` 必须零输出、零退出码 |
| `degraded/`、`tracks/`、`structure/`、`mislabeled/` | 解码进程必须成功退出（允许 warning） |
| `subtitles/` | 容器全量读取成功；每个外挂字幕都能用正确的 `-sub_charenc` 解析 |
| `damage/` | 不检查解码结果，只检查清单完整性 |

## 本次抽查结果

- 实际 SAR/DAR：`asf/mkv/dvd/mpeg2` 中的非方形 SAR 保持 32:27 或 64:45；AVI
  中的 MPEG-4 ASP 保持 12:11；MOV 中的 MPEG-4 ASP 保持 16:15。
- FFV1/NUT 精确保留 161×107；FFV1/MKV 精确保留 227×127。
- 场序：MOV DV 为 `bt`，M2TS/HDV 为 `tt`；AVI DV 的场序只存在于 DV 码流内，
  容器层探测为 `unknown`。
- 旋转：MP4 side data rotation 为 90，3GP 为 −90（即 270）。抽帧确认文字正立。
- 色彩标签：SD BT.709 标注、HD BT.601 标注、HD 无标注三个样本均符合文件名。
- VFR：MKV/MP4 混合帧率样本解码 324 帧（6 s×23.976 + 6 s×29.97）。
  `-f null` 默认 CFR 输出会产生 “non monotonically increasing dts” 提示，
  使用 `-fps_mode passthrough` 或 `-f framemd5` 时无提示。
- 音频空洞：4.008 s 到 5.013 s 之间没有音频包。
- packed B-frames：FFmpeg 识别为 packed 并解码出 300 帧。
- 字幕：MKV 内 SRT 11 包、ASS 22 包、VobSub 11 包；DVB 22 包（显示+清除）。
  抽帧确认 VobSub 位图和 ASS 附件像素字体都能正确渲染。
- GBK 元数据：AVI 与 RM 中各有一份原样 GBK 字节标题。
- AC-3/DTS 5.1 VOB：FFmpeg PS 封装器在文件末尾留下一个重复 DTS 的包，
  解码提示 1–5 条，内容完整。

## damage/ 在 FFmpeg 9.0.2 下的实际表现

| 文件 | 退出码 | 解码帧数 |
|---|---|---|
| `damage_headless_first64k_*.mpg` | 0 | 276 / 288 |
| `damage_headless_first64k_*.mpegts` | 0 | 348 / 360 |
| `damage_headless_first64k_*.avi`、`*.mkv` | 非 0（无法识别） | — |
| `damage_noidx1_*`、`damage_badidx1_*` | 0 | 180 / 180 |
| `damage_trunc_mp4_faststart_*` | 0 | 289 / 300 |
| `damage_trunc_mp4_mpeg4asp_*`（moov 在尾部） | 非 0 | — |
| `damage_p2p_zero_holes_*.avi` / `.mkv` / `.rmvb` | 0 | 278 / 338 / 145 |

## 复查命令

```bash
./tools/verify.sh
ffprobe -hide_banner -show_format -show_streams dataset/normal/FILE
ffmpeg -hide_banner -v error -i dataset/normal/FILE -f null -
```
