[English](STRUCTURE.md) | 中文

# 容器结构、时间戳与元数据（structure / mislabeled）

[← 返回 README](../README.zh-CN.md)

`structure/` 里都是合法或基本合法的文件，但带有老文件常见的结构特征；
`mislabeled/` 是扩展名与真实格式不符的副本。全部由 `generate_extra.py` 生成。

## 索引与交错

| 文件 | 特征 | 正确表现 |
|---|---|---|
| `mkv_no_cues_written_to_pipe_320x240.mkv` | 输出到管道写成，没有 Cues（流媒体录制常见） | 能播放；seek 时扫描 cluster，而不是禁止 seek |
| `mp4_faststart_moov_first_640x360.mp4` | moov 在文件头 | 与 `damage/damage_trunc_mp4_faststart...` 对照 |
| `avi_noninterleaved_audio_at_end_320x240.avi` | 所有视频 chunk 在前，所有音频 chunk 在后 | 用 idx1 随机读取，音画仍同步；顺序读取的播放器会没声音或大量读盘 |
| `avi_zero_length_dropped_frame_chunks_320x240.avi` | 3–4 秒内每隔一帧是 0 字节视频 chunk（采集丢帧占位） | 该处重复上一帧，时间不漂移 |
| `avi_divx5_packed_bframes_mpeg4_mp3_480x360.avi` | DivX 5 “packed bitstream”：P+B 放在同一 chunk，下一 chunk 是 N-VOP；带 `DivX503b1393p` 用户数据 | 正常播放，B 帧顺序正确；FFmpeg 会提示 packed B-frames，可用 `mpeg4_unpack_bframes` 还原 |

## 时间戳

| 文件 | 特征 | 正确表现 |
|---|---|---|
| `mpegts_pts_wrap_33bit_at_3.7s_480x480.ts` | 起始 PTS ≈ 95440 s，约 3.7 秒处越过 2^33 回绕 | 回绕点不停顿、不跳回开头、不卡死 |
| `mpegts_resolution_aspect_switch_720x480-4x3_16x9_352x240.ts` | 每 4 秒切换：720×480 4:3 → 720×480 16:9 → 352×240 | 每次切换后几何正确、不黑屏 |
| `mpegts_audio_samplerate_switch_48k_44k_32k_320x240.ts` | MP2 采样率每 4 秒变化：48 → 44.1 → 32 kHz | 音高不变、蜂鸣仍对齐；切换处允许一个短间断 |
| `concat_vts_01_1_plus_2_timestamp_reset_720x480.vob` | 两个 VOB 直接拼接，第 6 秒处时间戳归零 | 继续播放 sec 6–11；时长显示可能不准，但不能卡住 |
| `concat_cat_vcd_ntsc_352x240_plus_pal_352x288.mpg` | `cat` 拼接 NTSC VCD 与 PAL VCD：分辨率、帧率、时间戳都变化 | 第二段画面不被裁切、不拉伸 |
| `mkv_vfr_hybrid_23.976_then_29.97_h264_640x360.mkv` | 0–6 s 为 23.976 fps，6–12 s 为 29.97 fps | 运动白条匀速；没有每秒重复帧 |
| `mp4_vfr_hybrid_23.976_then_29.97_h264_640x360.mp4` | 同上，MP4 stts | 同上 |
| `mkv_video_starts_0.5s_after_audio_320x240.mkv` | 视频首帧 PTS 0.52 s，音频从 0 开始 | 前 0.5 秒黑屏或停在首帧，之后蜂鸣与白条对齐 |
| `mkv_audio_timestamp_gap_4s-5s_320x240.mkv` | 4–5 秒没有音频包 | 补静音，第 5 秒后仍然同步；没有提前播放后续音频 |
| `mkv_video_timestamp_gap_4s-5s_320x240.mkv` | 4–5 秒没有视频帧 | 画面冻结 1 秒，之后跳到 sec 5，音频不受影响 |
| `mov_editlist_empty_first_1s_320x240.mov` | edit list 第一段为 1 秒空编辑；H.264 带 B 帧 | 第一秒无画面，之后同步；忽略 edit list 会整体提前 1 秒 |

## 元数据

| 文件 | 特征 | 正确表现 |
|---|---|---|
| `mp4_display_rotation_90_h264_aac_360x640.mp4` | 存储为横屏 640×360，display matrix 逆时针转 90° | 竖屏显示，画面文字正立（“UPRIGHT IF ROT 90 OK”） |
| `3gp_display_rotation_270_h263_amrnb_176x144.3gp` | 手机 3GP，H.263 176×144，rotation 270 | 同上 |
| `mkv_chapters_every_3s_320x240.mkv` / `mp4_chapters_every_3s_320x240.mp4` | 4 个中文章节，在 0/3/6/9 秒 | 章节列表显示“第 N 章 / sec …”，跳转准确 |
| `avi_info_title_gbk_320x240.avi` | AVI `INFO/INAM` 是 GBK 字节“老电影 测试 GBK 标题” | 正确显示或按系统代码页回退；不能崩溃 |
| `rm_title_gbk_rv10_320x240.rm` | RealMedia CONT 标题为 GBK | 同上 |
| `mkv_sd_720x576_bt709_tagged_mpeg2.mkv` | SD 分辨率，但用 BT.709 编码并标注 | 按标签解码；按分辨率猜 601 会出现色偏 |
| `mkv_hd_1280x720_bt709_untagged_h264.mkv` | HD，BT.709 编码，**没有**色彩标签 | 按分辨率猜 709，色块正确 |
| `mkv_hd_1280x720_bt601_tagged_h264.mkv` | HD，但用 BT.601 编码并标注 | 按标签解码；忽略标签会让红绿偏移 |

## 隔行 HD

| 文件 | 特征 | 正确表现 |
|---|---|---|
| `m2ts_h264_mbaff_tff_ac3_1440x1080i_sar4-3.m2ts` | AVCHD 风格：192 字节 M2TS 包，H.264 MBAFF，顶场优先，SAR 4:3 | 去隔行后平滑；显示为 1920×1080 |
| `hdv_mpeg2_tff_mp2_1440x1080i_sar4-3.m2t` | HDV 风格：MPEG-2 1440×1080i，顶场优先，MP2 384k | 同上 |

## 边界文件

| 文件 | 特征 |
|---|---|
| `mkv_single_frame_320x240.mkv` | 只有 1 帧，没有音频 |
| `avi_audio_only_mp3.avi` | 只有 MP3 音轨的 AVI |
| `avi_video_only_msmpeg4v3_320x240.avi` | 没有音轨 |

0 字节文件放在 `damage/damage_zero_byte_empty_file.avi`。

## mislabeled/：扩展名与内容不符

| 文件 | 真实格式 |
|---|---|
| `actually_mkv_named.rmvb` | Matroska（MPEG-4 ASP） |
| `actually_mpegps_named.avi` | MPEG-1 PS |
| `actually_avi_named.wmv` | AVI（MSMPEG4 v3） |
| `actually_rm_named.avi` | RealMedia（RV10） |
| `actually_flv_named.mp4` | FLV（Sorenson Spark） |
| `actually_mp4_named.3gp.avi` | MP4（双扩展名） |

播放器应按文件内容探测格式。只看扩展名会选错 demuxer，表现为“文件损坏”或直接拒绝打开。
