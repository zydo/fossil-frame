[English](TRACKS_AND_SUBTITLES.md) | 中文

# 音轨与字幕（tracks / subtitles）

[← 返回 README](../README.zh-CN.md)

两类样本都由 `generate_extra.py` 生成，画面仍是 12 秒参考信号；黄色标题行写明
“应该听到/看到什么”。

## tracks/：多音轨、声道语义、老采样参数

| 文件 | 内容 | 正确表现 | 常见错误 |
|---|---|---|---|
| `vcd_karaoke_left1khz_right500hz_mpeg1_352x240.mpg` | VCD；左声道每秒 1 kHz 短蜂鸣（“原唱”），右声道每秒 500 Hz 长蜂鸣（“伴奏”） | 切换“左/右声道”或“原唱/伴奏”时只剩一种音高 | 没有声道选择功能；左右声道被提前混成单声道 |
| `dvd_dual_audio_ac3-1khz_lpcm-2khz_720x480.vob` | DVD VOB；音轨 1 AC-3 1 kHz，音轨 2 LPCM (`pcm_dvd`) 2 kHz | 两条音轨都能列出并切换 | LPCM 子流被忽略；默认选错轨 |
| `dvd_ac351_channel_id_720x480.vob` | AC-3 5.1；第 N 秒只有一个声道响：`N mod 6` = 0 FL、1 FR、2 C、3 LFE（80 Hz）、4 BL、5 BR | 环绕输出时声道位置对；下混成立体声时 C/LFE/后置也能听到 | 声道顺序错位；下混丢掉中置或 LFE |
| `dvd_dts51_channel_id_720x480.vob` | 同上，DTS 5.1 | 同上；也可测 S/PDIF/HDMI 直通 | DTS 解码缺失；直通失败没有声音 |
| `mkv_multilang_zho-1khz_eng-2khz-default_jpn51_320x240.mkv` | 三条音轨：zho AAC 1 kHz（非默认）、eng MP3 2 kHz（**default**）、jpn AC-3 5.1 声道识别 | 默认播放 2 kHz；轨道名/语言标签正确显示 | 忽略 default 标志、总是播第一轨 |
| `avi_mpeg4_mulaw_8khz_mono_320x240.avi` | G.711 μ-law 8 kHz 单声道 | 蜂鸣清楚、和白条对齐 | μ-law 当线性 PCM 播放导致刺耳失真 |

8-bit PCM（11.025 / 22.05 kHz）、32 kHz DV 音频、IMA4、G.726、Speex、SWF ADPCM
分别在 [CATALOG.md](CATALOG.zh-CN.md) 的追加经典编码表里。

已知限制：MPEG-PS 本身不携带音轨语言，DVD 的语言信息在 IFO 里，所以 VOB 样本
只能测轨道列举与切换。FFmpeg 的 PS 封装器会在 AC-3/DTS 5.1 VOB 的文件末尾留下
一个重复 DTS 的包，解码时出现 1–5 条 “non monotonically increasing dts” 提示，
不影响内容。

## subtitles/：字幕编码与格式

参考视频：`subtitle_reference_mpeg4_mp3_720x480.avi`（MPEG-4/MP3，720×480，SAR
32:27，25 fps）。所有字幕都在第 N 秒的 N.000–N.900 显示“第 N 秒 中文字幕測試 / sec N”，
即和蜂鸣、白条、`sec N` 同时出现。提前或滞后就是字幕时序错误。

外挂字幕（文件名都以参考视频名开头，可自动加载，也可手动指定）：

| 文件 | 格式/编码 | 测试点 |
|---|---|---|
| `*.gbk.srt` | SRT，GBK，无 BOM，CRLF | 无 BOM 中文的编码探测；乱码说明按 Latin-1/UTF-8 读取 |
| `*.big5.srt` | SRT，Big5 | 繁体编码探测；GBK/Big5 误判会出现错字 |
| `*.utf8bom.srt` | SRT，UTF-8 带 BOM | BOM 不应显示为首行乱码字符 |
| `*.utf16le.srt` | SRT，UTF-16LE 带 BOM | 宽字符编码；不支持时全是乱码或空白 |
| `*.ssa` | SubStation Alpha v4（非 ASS） | 老 SSA 样式头、`Marked=` 字段；底部中文、顶部英文 |
| `*.microdvd-25fps.sub` | MicroDVD，按帧号计时，无帧率头 | 播放器应按视频 25 fps 换算 |
| `*.microdvd-23.976fps-header.sub` | MicroDVD，首行 `{1}{1}23.976` | 应按头里的 23.976 换算；若按 25 fps 会越来越早 |
| `*.vobsub.idx` + `*.vobsub.sub` | VobSub 位图字幕（DVD SPU，2-bit RLE） | 位图字幕解析、调色板与透明度 |

内封字幕：

| 文件 | 内容 | 测试点 |
|---|---|---|
| `mkv_srt-zho_ass-fontattach_vobsub_720x480.mkv` | SRT（zho，default）、ASS（eng）、VobSub；附件字体 `PressStart2P-Regular.ttf` | ASS 顶部一行写着 “PIXEL FONT = ATTACHMENT OK N”。显示为像素字体说明附件字体已加载，显示为普通字体说明附件被忽略 |
| `dvd_mpeg2_ac3_vobsub_720x480.vob` | DVD subpicture 流 0x20 | VOB 内的字幕流探测 |
| `mpegts_mpeg2_mp2_dvbsub_720x480.ts` | DVB 位图字幕（由 VobSub 转码） | 广播 TS 字幕；每条字幕有显示包和清除包，共 22 个包 |

VobSub 位图由 `generate_extra.py` 内置的 SPU 编码器生成：先用 FFmpeg `drawtext`
把文字渲染成灰度图，再量化为 透明 / 白 / 深灰描边 三色并做 DVD RLE 编码。
渲染使用系统字体，生成的是位图，字体文件本身不进入数据集。
