[English](CATALOG.md) | 中文

# 逐文件清单（normal / damage / degraded）

[← 返回 README](../README.zh-CN.md) · 其他类别见 [TRACKS_AND_SUBTITLES.md](TRACKS_AND_SUBTITLES.zh-CN.md)、[STRUCTURE.md](STRUCTURE.zh-CN.md)。

## 正常文件逐项清单

时长均为 12 秒上下。实际参数来自 FFmpeg 9.0.2 探测结果；“可能缺陷”指播放器
在这类文件上容易暴露的兼容性问题，不是文件制作错误。

| 文件 | 实际视频参数 | 音频参数 | 大小 | 主要测试点 | 可能缺陷/风险 |
|---|---|---|---:|---|---|
| `dataset/normal/3gp_h263_amrnb_176x144.3gp` | H.263，176×144，SAR 1:1，DAR 11:9，15 fps | AMR-NB 8 kHz 单声道 | 336 KiB | 3GPP 基础组合、低码率音频 | H.263 老解码路径、AMR 采样率转换、小画面缩放 |
| `dataset/normal/3gp_mpeg4_amrnb_128x96.3gp` | MPEG-4，128×96，SAR 1:1，4:3，10 fps | AMR-NB 8 kHz 单声道 | 211 KiB | 3GP/MPEG-4、极小分辨率 | 最低画质路径、IMEI/brand 兼容标记、缩放锯齿 |
| `dataset/normal/asf_msmpeg4v3_wmav2_256x144_sar32-27.asf` | MSMPEG4 v3，256×144，SAR 32:27，DAR 512:243，15 fps | WMAv2 44.1 kHz 立体声 | 789 KiB | ASF、WMV 老编码、非方形 SAR | ASF 包边界、WMV FourCC、SAR 被误当 1:1 |
| `dataset/normal/asf_wmv1_wmav1_320x240.wmv` | WMV1，320×240，4:3，15 fps | WMAv1 44.1 kHz 立体声 | 763 KiB | WMV7/WMA1 组合 | WMV1 解码器缺失、WMA1 旧格式探测 |
| `dataset/normal/asf_wmv2_wmav2_320x240.wmv` | WMV2，320×240，4:3，15 fps | WMAv2 44.1 kHz 立体声 | 798 KiB | WMV8/WMA2 组合 | WMV2 老解码器、ASF seek 索引 |
| `dataset/normal/avi_h263_adpcm_176x144.avi` | H.263，176×144，SAR 1:1，11:9，15 fps | ADPCM IMA 44.1 kHz 立体声 | 859 KiB | AVI/H.263、ADPCM | AVI FourCC 不一致、H.263 帧头损坏后恢复 |
| `dataset/normal/avi_mpeg1video_mp2_320x240_25fps.avi` | MPEG-1，320×240，4:3，25 fps | MP2 44.1 kHz 立体声 | 1.21 MiB | AVI 封 MPEG-1、MP2 | MPEG-1 GOP 在 AVI 中的时间戳映射 |
| `dataset/normal/avi_mpeg4asp_mp3_352x288_sar12-11.avi` | MPEG-4 ASP/Xvid，352×288，SAR 12:11，DAR 4:3，25 fps | MP3 44.1 kHz 立体声 | 1.59 MiB | MPEG-4 ASP、Xvid FourCC、SAR | ASP B 帧重排、SAR 丢失导致画面变方 |
| `dataset/normal/avi_msmpeg4v2_adpcm_320x180_8fps.avi` | MSMPEG4 v2，320×180，16:9，8 fps | ADPCM MS 44.1 kHz 立体声 | 1.15 MiB | 8 fps、MSMPEG4 v2、ADPCM MS | 极低帧率 seek、音频连续但视频停顿感 |
| `dataset/normal/avi_msmpeg4v2_mp3_320x240_7fps.avi` | MSMPEG4 v2，320×240，4:3，7 fps | MP3 44.1 kHz 立体声 | 847 KiB | 7 fps、AVI vprn 时间基 | 视频时钟粗颗粒、MP3 帧与视频帧不对齐 |
| `dataset/normal/avi_msmpeg4v3_mp3_320x240.avi` | MSMPEG4 v3，320×240，4:3，15 fps | MP3 44.1 kHz 立体声 | 891 KiB | DivX 老生态常见组合 | FourCC 分支、老解码器/现代 MPEG-4 解码器差异 |
| `dataset/normal/avi_rawvideo_bgr24_136x76_10fps.avi` | RawVideo BGR24，136×76，10 fps | PCM S16LE 44.1 kHz 立体声 | 5.47 MiB | 无压缩 RGB、非标宽高 | BGR/RGB 通道颠倒、行尾 padding、bottom-up AVI |
| `dataset/normal/dvd_mpeg2video_ac3_720x480_sar32-27.vob` | MPEG-2，720×480，SAR 32:27，DAR 16:9，29.97 fps；含 DVD 导航数据流 | AC-3 48 kHz 立体声 | 2.64 MiB | DVD-VOB、导航包、模拟 NTSC | 忽略/错误消费 nav 包、GOP seek、29.97 时间基 |
| `dataset/normal/flv_flv1_mp3_320x240.flv` | FLV1/Sorenson Spark，320×240，15 fps | MP3 44.1 kHz 立体声 | 921 KiB | FLV1、老 Flash 视频 | FLV1 编码器缺失、标签顺序和时间戳重排 |
| `dataset/normal/flv_h264_nellymoser_320x240.flv` | H.264 Baseline，320×240，4:3，15 fps | Nellymoser 44.1 kHz 单声道 | 422 KiB | FLV+H.264、Nellymoser | 新视频/旧音频混合；Nellymoser声音粗糙属编码特性 |
| `dataset/normal/mkv_ffv1_rgb_flac_227x127_12-5fps.mkv` | FFV1，227×127，BGR0/GBR，full-range，12.5 fps | FLAC 44.1 kHz 立体声 | 766 KiB | 精确奇数分辨率、RGB 路径 | 奇数宽高被错误取整、RGB/GBR 色彩空间转换 |
| `dataset/normal/mkv_h263_mp3_176x144.mkv` | H.263，176×144，11:9，15 fps | MP3 44.1 kHz 立体声 | 482 KiB | MKV 封 H.263、limited-range | H.263 色彩标记缺失时的默认假设 |
| `dataset/normal/mkv_mjpeg_pcm_320x240.mkv` | M-JPEG，320×240，YUVJ420P，full-range，15 fps | PCM S16LE 44.1 kHz 立体声 | 4.37 MiB | 帧内 JPEG、旧 full-range 标记 | YUVJ 弃用标记导致过暗/过亮、帧内流不能借用前后帧纠错 |
| `dataset/normal/mkv_mpeg2video_ac3_720x480_sar32-27.mkv` | MPEG-2，720×480，SAR 32:27，DAR 16:9，29.97 fps | AC-3 48 kHz 立体声 | 2.48 MiB | MKV/MPEG-2/AC-3、NTSC SAR | MPEG-2 GOP、AC-3 起始帧、时间戳不连续 |
| `dataset/normal/mkv_mpeg4asp_mp3_352x288_sar64-45.mkv` | MPEG-4 ASP，352×288，SAR 64:45，DAR 704:405，25 fps | MP3 44.1 kHz 立体声 | 1.61 MiB | 极端 SAR、MPEG-4 ASP | 容器/码流 SAR 冲突、画面横向比例错误 |
| `dataset/normal/mkv_vp8_vorbis_320x240.mkv` | VP8，320×240，4:3，15 fps | Vorbis 44.1 kHz 立体声 | 640 KiB | WebM 老生代组合 | VP8 错误传播、Vorbis 头包顺序 |
| `dataset/normal/mov_mjpeg_pcm_320x240.mov` | M-JPEG，320×240，YUVJ420P，full-range，15 fps | PCM S16LE 44.1 kHz 立体声 | 4.38 MiB | QuickTime/M-JPEG/PCM | QuickTime 原子索引、full-range 解释 |
| `dataset/normal/mov_mpeg4asp_mp2_256x144_sar16-15.mov` | MPEG-4 ASP，256×144，SAR 16:15，DAR 256:135，12 fps | MP2 44.1 kHz 立体声 | 651 KiB | MOV/MPEG-4 ASP、非方形 SAR | 编辑列表、SAR 元数据、12 fps 时钟 |
| `dataset/normal/mp4_mpeg4asp_mp3_160x106.mp4` | MPEG-4 ASP，160×106，80:53，10 fps | MP3 44.1 kHz 立体声 | 427 KiB | 小尺寸 MP4/MPEG-4 ASP | 奇比例尺寸缩放、moov 缺失、MP3 in MP4 |
| `dataset/normal/mp4_mpeg4asp_mp3_640x360.mp4` | MPEG-4 ASP，640×360，16:9，25 fps | MP3 44.1 kHz 立体声 | 2.47 MiB | MP4/MPEG-4 ASP/Xvid 生态 | B 帧、旧 MP4V tag、GOP 边界 seek |
| `dataset/normal/mpeg1_mpeg1video_mp2_352x240.mpg` | MPEG-1，352×240，DAR 22:15，23.976 fps | MP2 44.1 kHz 立体声 | 1.18 MiB | MPEG-1 PS、23.976 fps | MPEG-1 受限帧率/几何、PS 时间戳漂移 |
| `dataset/normal/mpeg2_mpeg2video_mp2_720x576_sar64-45.mpg` | MPEG-2，720×576，SAR 64:45，DAR 16:9，25 fps | MP2 44.1 kHz 立体声 | 2.65 MiB | PAL 几何、MPEG-2 PS | SAR 与像素尺寸混淆、MPEG-2 limited-range |
| `dataset/normal/mpegts_mpeg2video_ac3_480x480_29-97.mpegts` | MPEG-2，480×480，1:1，29.97 fps | AC-3 48 kHz 立体声 | 2.04 MiB | MPEG-TS、 discontinuity、广播流 | PTS 复位、PCR/PTS 不连续、TS 包丢失纠错 |
| `dataset/normal/nut_ffv1_rgb_pcm_161x107_12-5fps.nut` | FFV1，161×107，BGR0/GBR，full-range，12.5 fps | PCM S16LE 44.1 kHz 立体声 | 2.47 MiB | NUT 容器、精确奇数尺寸 | 小众容器探测、RGB 奇数宽高 |
| `dataset/normal/ogv_theora_vorbis_320x240.ogv` | Theora，320×240，4:3，15 fps | Vorbis 44.1 kHz 立体声 | 519 KiB | Ogg/Theora/Vorbis | Ogg 页边界、Theora/Vorbis 头包 |
| `dataset/normal/rm_rv10_ac3_320x240.rm` | RealVideo 1.0，320×240，15 fps；探测 SAR 不可用 | AC-3 48 kHz 立体声 | 766 KiB | RealMedia/RV10 | RM demuxer、RM 内 AC-3 兼容性；无 SAR 元数据时按方形像素处理 |
| `dataset/normal/rm_rv10_real144_176x144_sar12-11.rm` | RealVideo 1.0，176×144，12 fps；生成目标 SAR 12:11，RM 实际探测 SAR 不可用 | RealAudio 1.0 8 kHz 单声道 | 586 KiB | 最老 Real 组合、SAR 元数据缺失 | RV10/RA14.4 解码；无法携带 SAR 时画面比例可能错误 |
| `dataset/normal/rm_rv20_ac3_320x240.rmvb` | RealVideo 2.0，320×240，15 fps | AC-3 48 kHz 立体声 | 800 KiB | `.rmvb` 扩展名、RV20 | RV20 解码、RMVB 扩展名识别；不是 RV30/RV40 RMVB |
| `dataset/normal/svcd_mpeg2video_mp2_480x480.mpg` | MPEG-2，480×480，1:1，23.976 fps | MP2 44.1 kHz 立体声 | 1.82 MiB | SVCD PS、方形 480×480 | SVCD 系统流约束、23.976 fps 与扫描比例 |
| `dataset/normal/vcd_mpeg1video_mp2_352x240.mpg` | MPEG-1，352×240，DAR 22:15，23.976 fps | MP2 44.1 kHz 立体声 | 1.18 MiB | VCD 系统流 | VCD 流约束、旧 MPEG-1 序列头、seek 到 GOP |

说明：RM 容器探测不到 SAR 是老格式/封装器的已知限制。`rm_rv10_real144...` 故意
保留生成目标 SAR 与实际探测缺失之间的落差，用来观察播放器是否自行做出稳定、
可解释的回退。

### 追加的经典编码（`generate_extra.py`）

画面左上方的黄色标题行写明了编码名。除 DV 外都是 12 秒参考信号。

| 文件 | 视频 | 音频 | 主要测试点 | 可能缺陷/风险 |
|---|---|---|---|---|
| `normal/avi_cinepak_pcmu8_320x240_22050hz.avi` | Cinepak，RGB24 输入，15 fps | 8-bit 无符号 PCM，22.05 kHz 单声道 | 90 年代光盘视频；8-bit PCM | Cinepak 解码缺失；u8 当 s8 处理导致满幅噪声 |
| `normal/mov_cinepak_adpcmimaqt_320x240.mov` | QuickTime Cinepak | IMA4（QuickTime ADPCM） | QT 早期组合 | `ima4` 块大小、QT 原子 |
| `normal/mov_svq1_adpcmimaqt_320x240.mov` | Sorenson Video 1，YUV410P | IMA4 立体声 | QuickTime 3–5 预告片时代 | 4:1:0 色度上采样、SVQ1 缺失 |
| `normal/avi_msvideo1_pcmu8_160x120_11025hz.avi` | MS Video-1 (CRAM)，RGB555，10 fps | u8 PCM 11.025 kHz | Win 3.1/95 AVI | RGB555 位序、11 kHz 重采样 |
| `normal/mov_qtrle_pcms16be_160x120.mov` | QuickTime Animation (RLE)，RGB24 | 大端 PCM | QT RLE | 大端 PCM 字节序、RLE 跳过行 |
| `normal/mov_smc_pcms16be_160x120.mov` | QuickTime Graphics (SMC)，PAL8 | 大端 PCM | 调色板视频 | 调色板载入、PAL8 转换 |
| `normal/mov_rpza_pcms16be_160x120.mov` | QuickTime Video (RPZA)，RGB555 | 大端 PCM | 最老 QT 编码之一 | RPZA 解码缺失 |
| `normal/avi_zmbv_pcm_320x200_70fps.avi` | ZMBV（DOSBox），320×200，SAR 5:6，70 fps | PCM 44.1 kHz | DOS 游戏录像 | 70 fps 时钟、320×200 应显示为 4:3 |
| `normal/flv_flashsv_adpcmswf_320x240.flv` | Flash Screen Video，10 fps | SWF ADPCM 22.05 kHz | Flash 屏幕录制 | 块更新编码、SWF ADPCM |
| `normal/flv_flashsv2_speex_320x240.flv` | Flash Screen Video 2 | Speex 16 kHz | Flash 8+ 录屏/网聊 | FLV Speex 时间戳、flashsv2 缺失 |
| `normal/avi_h261_g726_352x288.avi` | H.261 CIF，SAR 12:11 | G.726 32 kbit/s 8 kHz | 视频会议最老标准 | H.261 解码、G.726 位宽探测 |
| `normal/avi_huffyuv_yuv422_pcm_320x240.avi` | HuffYUV，YUV 4:2:2 | PCM 48 kHz | VirtualDub 采集中间文件 | 4:2:2 输出路径、高码率读盘 |
| `normal/avi_xvid_qpel_gmc_bframes_mp3_640x352.avi` | Xvid，QPel + GMC + 2 B 帧 | MP3 | 当年 DivX 硬件播放器不支持的 ASP 工具 | QPel/GMC 解码错误表现为抖动、糊化 |
| `normal/avi_dv_pal_bff_pcm48k_720x576_6s.avi` | DV PAL，4:2:0，**底场优先**，SAR 64:45，6 秒 | PCM 48 kHz | MiniDV type-2 AVI | 场序反了会抖；AVI 头不带场序，只在 DV 码流里 |
| `normal/mov_dv_ntsc_411_pcm32k_720x480_6s.mov` | DV NTSC，**4:1:1**，底场优先，SAR 8:9，6 秒 | PCM 32 kHz | MiniDV 32 kHz 录音模式 | 4:1:1 色度、32 kHz 音频 |

DV 码率固定约 25 Mbit/s，为控制仓库体积只保留 6 秒。

## 损坏文件清单

| 损坏文件 | 来源 | 缺陷 | 预期现象 | 测试指标 |
|---|---|---|---|---|
| `dataset/damage/damage_corrupt_3gp_h263_amrnb_176x144.3gp` | 对应 3GP/H.263 片段 | 中段约 8 KiB 被改写 | H.263 花屏、色块、马赛克；AMR 可能出现短噪声 | 解码器错误恢复、3GP 包跳过 |
| `dataset/damage/damage_corrupt_asf_wmv1_wmav1_320x240.wmv` | 对应 ASF/WMV1 片段 | 中段约 8 KiB 被改写 | WMV 块状破损或音频爆音；理想情况只影响局部 | ASF 包定位、WMA/WMV 容错 |
| `dataset/damage/damage_corrupt_avi_msmpeg4v3_mp3_320x240.avi` | 对应 AVI/MSMPEG4 片段 | 中段约 8 KiB 被改写 | MSMPEG4 花屏、可能短音频错位 | AVI index/chunk 恢复、帧内错误传播控制 |
| `dataset/damage/damage_corrupt_mkv_mpeg2video_ac3_720x480_sar32-27.mkv` | 对应 MKV/MPEG-2 片段 | 中段约 8 KiB 被改写 | GOP 内破损后应等到下一个关键帧恢复 | Matroska cluster 修复、MPEG-2 concealment |
| `dataset/damage/damage_corrupt_mpegts_mpeg2video_ac3_480x480_29-97.mpegts` | 对应 MPEG-TS 片段 | 中段约 8 KiB 被改写 | TS 连续性错误、短花屏/爆音 | PAT/PMT 重扫、continuity counter、丢包恢复 |
| `dataset/damage/damage_corrupt_rm_rv10_ac3_320x240.rm` | 对应 RM/RV10 片段 | 中段约 8 KiB 被改写 | RV10 花屏或 demuxer 报错 | RealMedia 包边界识别、RV10 恢复 |
| `dataset/damage/damage_trunc_3gp_mpeg4_amrnb_128x96.3gp` | 对应 3GP/MPEG-4 片段 | 移除末尾约 3% | 播放到接近末尾时应报错或优雅停止 | 尾包缺失、moov/索引处理 |
| `dataset/damage/damage_trunc_mkv_mpeg4asp_mp3_352x288_sar64-45.mkv` | 对应 MKV/MPEG-4 ASP 片段 | 移除末尾约 3% | 最后 cluster 不完整；应播放可用部分 | 尾部 cluster 恢复、Cues 缺失 |
| `dataset/damage/damage_trunc_mp4_mpeg4asp_mp3_640x360.mp4` | 对应 MP4/MPEG-4 片段 | 移除末尾约 3% | 若 moov 在尾部可能完全不可打开；理想播放器提示修复 | moov 缺失、mp4 修复、索引重建 |
| `dataset/damage/damage_trunc_rm_rv20_ac3_320x240.rmvb` | 对应 RMVB/RV20 片段 | 移除末尾约 3% | 末尾索引/包缺失；应避免死循环 | RealMedia 索引缺失处理 |

### 追加：下载未完成 / 索引损坏（`generate_extra.py`）

| 损坏文件 | 缺陷 | 预期现象 | 测试指标 |
|---|---|---|---|
| `damage/damage_zero_byte_empty_file.avi` | 0 字节 | 立即报错，不能卡住或崩溃 | 空文件处理 |
| `damage/damage_p2p_zero_holes_*`（AVI / MKV / RMVB） | 文件 1/3 和 2/3 处各有一个按 64 KiB 对齐的全零块，模拟 BT/eMule 未下完的 piece | 两段花屏或跳段，之后恢复 | 零填充区跳过、重新同步 |
| `damage/damage_headless_first64k_*`（MPG / TS / AVI / MKV） | 开头 64 KiB 缺失 | PS/TS 应能重新同步并播放；AVI/MKV 无头通常打不开，应明确报错 | 无文件头时的码流同步 |
| `damage/damage_noidx1_avi_msmpeg4v3_mp3_320x240.avi` | 删除 `idx1`，但 `avih` 仍声明有索引 | 能播放；seek 需要扫描或重建索引 | 索引缺失回退 |
| `damage/damage_badidx1_offsets_avi_msmpeg4v3_mp3_320x240.avi` | 后 2/3 的 `idx1` 偏移被加 4093 字节 | 只信索引会读到垃圾；理想播放器发现后改为顺序扫描 | 索引校验 |
| `damage/damage_trunc_mp4_faststart_moov_first_640x360.mp4` | moov 在头部的 MP4 截掉末尾 3% | 与原有 moov 在尾的截断样本对照：这个应能播放到截断点 | moov 位置对截断容忍度的影响 |

## 退化文件逐项清单

这些是合法媒体，但预置了“老源、老采集、反复压制、反复传播”后的典型缺陷。
详细来源见 [docs/DEGRADATION.md](DEGRADATION.zh-CN.md)。

| 文件 | 主要参数 | 预置缺陷 | 播放器测试点 |
|---|---|---|---|
| `dataset/degraded/vhs_composite_wear_mpeg2_ac3_720x480.mkv` | MPEG-2/AC-3，720×480，SAR 32:27，29.97 fps | RGB/chroma 偏移、噪声、拖影、dropout、跟踪带 | 脏画面稳定渲染；色彩转换与错误恢复 |
| `dataset/degraded/chroma_under_bleed_mpeg2_ac3_720x480.mkv` | MPEG-2/AC-3，720×480，SAR 32:27，29.97 fps | VHS color-under 色度拖尾 | 色度上采样、红蓝边缘错位 |
| `dataset/degraded/motion_ghost_trails_mpeg4_mp3_480x360.mp4` | MPEG-4/MP3，480×360，25 fps | `lagfun`/`tmix` 帧间残影 | 运动轮廓拖尾和参考帧显示 |
| `dataset/degraded/generation_loss_x3_mpeg4_mp3_352x240.avi` | MPEG-2 → MPEG-4 → MPEG-4 三代压制 | 低码率方块、振铃、色带、细节糊化 | 有损链路后的稳定解码 |
| `dataset/degraded/long_gop_bitstream_errors_mpeg4_mp3_480x360.avi` | MPEG-4/MP3，300 帧 GOP，encoder error-rate | 长 GOP 预测结构和低质量编码 | 错误传播、seek 后恢复 |
| `dataset/degraded/damaged_i_frame_mpeg4_mp3_480x360.avi` | MPEG-4/MP3，480×360，I 帧 96 字节改写 | 关键帧损坏并扩散到依赖帧 | 花点/鬼影/马赛克，等下一 I 帧恢复 |
| `dataset/degraded/interlaced_wrong_handling_mpeg2_ac3_720x480.mkv` | MPEG-2/AC-3，720×480，29.97 fps，top-field | 59.94 场合成隔行 | field order、combing、渐进误播 |
| `dataset/degraded/telecine_judder_mpeg2_mp3_720x480.mpg` | MPEG-2/MP3，720×480，23.976 → 29.97 | 胶卷电视电影化重复帧 | cadence、IVTC、节奏抖动 |
| `dataset/degraded/vbr_mp3_audio_offset_mpeg4_352x240.avi` | MPEG-4/VBR MP3，352×240 | AVI VBR MP3 + 350 ms 偏移 | 音画延迟、旧 AVI 音频时间基 |
| `dataset/degraded/dropped_duplicated_frames_mpeg4_mp3_480x360.mkv` | MPEG-4/MP3，480×360，25 fps | 丢帧后按帧号重排 PTS | 跳步、重复帧、运动连续性 |

