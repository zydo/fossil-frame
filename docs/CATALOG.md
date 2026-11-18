English | [中文](CATALOG.zh-CN.md)

# File catalog (normal / damage / degraded)

[← Back to README](../README.md) · Other categories: [Tracks & subtitles](TRACKS_AND_SUBTITLES.md),
[Structure](STRUCTURE.md).

## Normal files

All clips are about 12 seconds long. Parameters are the values FFmpeg 9.0.2
actually probes. The "risk" column lists compatibility problems a player tends to
show on that kind of file; it does not describe a defect in the file.

| File | Video | Audio | Size | What it tests | Risk |
|---|---|---|---:|---|---|
| `dataset/normal/3gp_h263_amrnb_176x144.3gp` | H.263, 176×144, SAR 1:1, DAR 11:9, 15 fps | AMR-NB 8 kHz mono | 336 KiB | Basic 3GPP combination, low-bitrate audio | Legacy H.263 path, AMR resampling, scaling small frames |
| `dataset/normal/3gp_mpeg4_amrnb_128x96.3gp` | MPEG-4, 128×96, SAR 1:1, 4:3, 10 fps | AMR-NB 8 kHz mono | 211 KiB | 3GP/MPEG-4, tiny resolution | Lowest-quality path, brand compatibility marks, scaling aliasing |
| `dataset/normal/asf_msmpeg4v3_wmav2_256x144_sar32-27.asf` | MSMPEG4 v3, 256×144, SAR 32:27, DAR 512:243, 15 fps | WMAv2 44.1 kHz stereo | 789 KiB | ASF, legacy WMV codec, non-square SAR | ASF packet boundaries, WMV FourCC, SAR treated as 1:1 |
| `dataset/normal/asf_wmv1_wmav1_320x240.wmv` | WMV1, 320×240, 4:3, 15 fps | WMAv1 44.1 kHz stereo | 763 KiB | WMV7/WMA1 | Missing WMV1 decoder, WMA1 probing |
| `dataset/normal/asf_wmv2_wmav2_320x240.wmv` | WMV2, 320×240, 4:3, 15 fps | WMAv2 44.1 kHz stereo | 798 KiB | WMV8/WMA2 | Legacy WMV2 decoder, ASF seek index |
| `dataset/normal/avi_h263_adpcm_176x144.avi` | H.263, 176×144, SAR 1:1, 11:9, 15 fps | IMA ADPCM 44.1 kHz stereo | 859 KiB | AVI/H.263, ADPCM | Inconsistent AVI FourCC, recovery from bad H.263 headers |
| `dataset/normal/avi_mpeg1video_mp2_320x240_25fps.avi` | MPEG-1, 320×240, 4:3, 25 fps | MP2 44.1 kHz stereo | 1.21 MiB | MPEG-1 in AVI, MP2 | Mapping MPEG-1 GOP timestamps in AVI |
| `dataset/normal/avi_mpeg4asp_mp3_352x288_sar12-11.avi` | MPEG-4 ASP/Xvid, 352×288, SAR 12:11, DAR 4:3, 25 fps | MP3 44.1 kHz stereo | 1.59 MiB | MPEG-4 ASP, Xvid FourCC, SAR | ASP B-frame reordering, lost SAR makes the picture squarer |
| `dataset/normal/avi_msmpeg4v2_adpcm_320x180_8fps.avi` | MSMPEG4 v2, 320×180, 16:9, 8 fps | MS ADPCM 44.1 kHz stereo | 1.15 MiB | 8 fps, MSMPEG4 v2, MS ADPCM | Seeking at very low frame rates; continuous audio over choppy video |
| `dataset/normal/avi_msmpeg4v2_mp3_320x240_7fps.avi` | MSMPEG4 v2, 320×240, 4:3, 7 fps | MP3 44.1 kHz stereo | 847 KiB | 7 fps, AVI time base | Coarse video clock, MP3 frames not aligned with video frames |
| `dataset/normal/avi_msmpeg4v3_mp3_320x240.avi` | MSMPEG4 v3, 320×240, 4:3, 15 fps | MP3 44.1 kHz stereo | 891 KiB | Classic early DivX combination | FourCC branches, old vs modern MPEG-4 decoders |
| `dataset/normal/avi_rawvideo_bgr24_136x76_10fps.avi` | Raw BGR24, 136×76, 10 fps | PCM S16LE 44.1 kHz stereo | 5.47 MiB | Uncompressed RGB, unusual size | Swapped BGR/RGB, row padding, bottom-up AVI |
| `dataset/normal/dvd_mpeg2video_ac3_720x480_sar32-27.vob` | MPEG-2, 720×480, SAR 32:27, DAR 16:9, 29.97 fps; DVD navigation stream | AC-3 48 kHz stereo | 2.64 MiB | DVD VOB, nav packets, analog NTSC | Mishandled nav packets, GOP seeking, 29.97 time base |
| `dataset/normal/flv_flv1_mp3_320x240.flv` | FLV1/Sorenson Spark, 320×240, 15 fps | MP3 44.1 kHz stereo | 921 KiB | FLV1, legacy Flash video | Missing FLV1 decoder, tag order and timestamp reordering |
| `dataset/normal/flv_h264_nellymoser_320x240.flv` | H.264 Baseline, 320×240, 4:3, 15 fps | Nellymoser 44.1 kHz mono | 422 KiB | FLV + H.264, Nellymoser | New video with old audio; Nellymoser sounds rough by design |
| `dataset/normal/mkv_ffv1_rgb_flac_227x127_12-5fps.mkv` | FFV1, 227×127, BGR0/GBR, full range, 12.5 fps | FLAC 44.1 kHz stereo | 766 KiB | Exact odd dimensions, RGB path | Odd sizes rounded wrongly, RGB/GBR conversion |
| `dataset/normal/mkv_h263_mp3_176x144.mkv` | H.263, 176×144, 11:9, 15 fps | MP3 44.1 kHz stereo | 482 KiB | H.263 in MKV, limited range | Default assumptions when H.263 has no color tags |
| `dataset/normal/mkv_mjpeg_pcm_320x240.mkv` | M-JPEG, 320×240, YUVJ420P, full range, 15 fps | PCM S16LE 44.1 kHz stereo | 4.37 MiB | Intra-only JPEG, legacy full-range tag | Deprecated YUVJ tag gives too dark/bright output; no inter-frame concealment |
| `dataset/normal/mkv_mpeg2video_ac3_720x480_sar32-27.mkv` | MPEG-2, 720×480, SAR 32:27, DAR 16:9, 29.97 fps | AC-3 48 kHz stereo | 2.48 MiB | MKV/MPEG-2/AC-3, NTSC SAR | MPEG-2 GOPs, AC-3 start frame, timestamp discontinuities |
| `dataset/normal/mkv_mpeg4asp_mp3_352x288_sar64-45.mkv` | MPEG-4 ASP, 352×288, SAR 64:45, DAR 704:405, 25 fps | MP3 44.1 kHz stereo | 1.61 MiB | Extreme SAR, MPEG-4 ASP | Container vs bitstream SAR conflict, wrong horizontal proportion |
| `dataset/normal/mkv_vp8_vorbis_320x240.mkv` | VP8, 320×240, 4:3, 15 fps | Vorbis 44.1 kHz stereo | 640 KiB | Early WebM combination | VP8 error propagation, Vorbis header order |
| `dataset/normal/mov_mjpeg_pcm_320x240.mov` | M-JPEG, 320×240, YUVJ420P, full range, 15 fps | PCM S16LE 44.1 kHz stereo | 4.38 MiB | QuickTime/M-JPEG/PCM | QuickTime atom index, full-range interpretation |
| `dataset/normal/mov_mpeg4asp_mp2_256x144_sar16-15.mov` | MPEG-4 ASP, 256×144, SAR 16:15, DAR 256:135, 12 fps | MP2 44.1 kHz stereo | 651 KiB | MOV/MPEG-4 ASP, non-square SAR | Edit lists, SAR metadata, 12 fps clock |
| `dataset/normal/mp4_mpeg4asp_mp3_160x106.mp4` | MPEG-4 ASP, 160×106, 80:53, 10 fps | MP3 44.1 kHz stereo | 427 KiB | Small MP4/MPEG-4 ASP | Scaling odd ratios, missing moov, MP3 in MP4 |
| `dataset/normal/mp4_mpeg4asp_mp3_640x360.mp4` | MPEG-4 ASP, 640×360, 16:9, 25 fps | MP3 44.1 kHz stereo | 2.47 MiB | MP4/MPEG-4 ASP/Xvid era | B-frames, old `mp4v` tag, seeking at GOP boundaries |
| `dataset/normal/mpeg1_mpeg1video_mp2_352x240.mpg` | MPEG-1, 352×240, DAR 22:15, 23.976 fps | MP2 44.1 kHz stereo | 1.18 MiB | MPEG-1 PS, 23.976 fps | MPEG-1 constrained parameters, PS timestamp drift |
| `dataset/normal/mpeg2_mpeg2video_mp2_720x576_sar64-45.mpg` | MPEG-2, 720×576, SAR 64:45, DAR 16:9, 25 fps | MP2 44.1 kHz stereo | 2.65 MiB | PAL geometry, MPEG-2 PS | Confusing SAR with pixel size, MPEG-2 limited range |
| `dataset/normal/mpegts_mpeg2video_ac3_480x480_29-97.mpegts` | MPEG-2, 480×480, 1:1, 29.97 fps | AC-3 48 kHz stereo | 2.04 MiB | MPEG-TS, broadcast stream | PTS resets, PCR/PTS discontinuities, recovering from lost TS packets |
| `dataset/normal/nut_ffv1_rgb_pcm_161x107_12-5fps.nut` | FFV1, 161×107, BGR0/GBR, full range, 12.5 fps | PCM S16LE 44.1 kHz stereo | 2.47 MiB | NUT container, exact odd size | Probing a niche container, RGB odd dimensions |
| `dataset/normal/ogv_theora_vorbis_320x240.ogv` | Theora, 320×240, 4:3, 15 fps | Vorbis 44.1 kHz stereo | 519 KiB | Ogg/Theora/Vorbis | Ogg page boundaries, Theora/Vorbis headers |
| `dataset/normal/rm_rv10_ac3_320x240.rm` | RealVideo 1.0, 320×240, 15 fps; SAR not probed | AC-3 48 kHz stereo | 766 KiB | RealMedia/RV10 | RM demuxer, AC-3 inside RM; square pixels assumed without SAR |
| `dataset/normal/rm_rv10_real144_176x144_sar12-11.rm` | RealVideo 1.0, 176×144, 12 fps; target SAR 12:11, RM cannot carry it | RealAudio 1.0 8 kHz mono | 586 KiB | Oldest Real combination, missing SAR | RV10/RA14.4 decoding; aspect may be wrong without SAR |
| `dataset/normal/rm_rv20_ac3_320x240.rmvb` | RealVideo 2.0, 320×240, 15 fps | AC-3 48 kHz stereo | 800 KiB | `.rmvb` extension, RV20 | RV20 decoding, `.rmvb` recognition; not RV30/RV40 RMVB |
| `dataset/normal/svcd_mpeg2video_mp2_480x480.mpg` | MPEG-2, 480×480, 1:1, 23.976 fps | MP2 44.1 kHz stereo | 1.82 MiB | SVCD PS, square 480×480 | SVCD system-stream constraints, 23.976 fps and scan aspect |
| `dataset/normal/vcd_mpeg1video_mp2_352x240.mpg` | MPEG-1, 352×240, DAR 22:15, 23.976 fps | MP2 44.1 kHz stereo | 1.18 MiB | VCD system stream | VCD constraints, old MPEG-1 sequence header, seeking to GOPs |

Note: the RM container cannot carry SAR, a known limitation of the format and
muxer. `rm_rv10_real144...` deliberately keeps the gap between the target SAR and
what is probed, to see whether the player falls back in a stable, explainable way.

### Additional classic codecs (`generate_extra.py`)

The yellow title line at the top left names the codec. Every clip except the DV
ones is the 12-second reference signal.

| File | Video | Audio | What it tests | Risk |
|---|---|---|---|---|
| `normal/avi_cinepak_pcmu8_320x240_22050hz.avi` | Cinepak, RGB24 input, 15 fps | 8-bit unsigned PCM, 22.05 kHz mono | 1990s CD-ROM video; 8-bit PCM | Missing Cinepak decoder; u8 treated as s8 gives full-scale noise |
| `normal/mov_cinepak_adpcmimaqt_320x240.mov` | QuickTime Cinepak | IMA4 (QuickTime ADPCM) | Early QuickTime combination | `ima4` block size, QT atoms |
| `normal/mov_svq1_adpcmimaqt_320x240.mov` | Sorenson Video 1, YUV410P | IMA4 stereo | QuickTime 3–5 trailer era | 4:1:0 chroma upsampling, missing SVQ1 |
| `normal/avi_msvideo1_pcmu8_160x120_11025hz.avi` | MS Video-1 (CRAM), RGB555, 10 fps | u8 PCM 11.025 kHz | Windows 3.1/95 AVI | RGB555 bit order, 11 kHz resampling |
| `normal/mov_qtrle_pcms16be_160x120.mov` | QuickTime Animation (RLE), RGB24 | Big-endian PCM | QT RLE | Big-endian PCM byte order, RLE skipped lines |
| `normal/mov_smc_pcms16be_160x120.mov` | QuickTime Graphics (SMC), PAL8 | Big-endian PCM | Palettized video | Palette loading, PAL8 conversion |
| `normal/mov_rpza_pcms16be_160x120.mov` | QuickTime Video (RPZA), RGB555 | Big-endian PCM | One of the oldest QT codecs | Missing RPZA decoder |
| `normal/avi_zmbv_pcm_320x200_70fps.avi` | ZMBV (DOSBox), 320×200, SAR 5:6, 70 fps | PCM 44.1 kHz | DOS game capture | 70 fps clock; 320×200 must display as 4:3 |
| `normal/flv_flashsv_adpcmswf_320x240.flv` | Flash Screen Video, 10 fps | SWF ADPCM 22.05 kHz | Flash screen recording | Block-update coding, SWF ADPCM |
| `normal/flv_flashsv2_speex_320x240.flv` | Flash Screen Video 2 | Speex 16 kHz | Flash 8+ screen recording / web chat | Speex timestamps in FLV, missing flashsv2 |
| `normal/avi_h261_g726_352x288.avi` | H.261 CIF, SAR 12:11 | G.726 32 kbit/s 8 kHz | Oldest videoconferencing standard | H.261 decoding, G.726 bit-depth probing |
| `normal/avi_huffyuv_yuv422_pcm_320x240.avi` | HuffYUV, YUV 4:2:2 | PCM 48 kHz | VirtualDub capture intermediates | 4:2:2 output path, high read bitrate |
| `normal/avi_xvid_qpel_gmc_bframes_mp3_640x352.avi` | Xvid, QPel + GMC + 2 B-frames | MP3 | ASP tools old DivX hardware players lacked | Broken QPel/GMC shows as wobble or blur |
| `normal/avi_dv_pal_bff_pcm48k_720x576_6s.avi` | DV PAL, 4:2:0, **bottom field first**, SAR 64:45, 6 s | PCM 48 kHz | MiniDV type-2 AVI | Wrong field order judders; AVI headers carry no field order, only the DV bitstream does |
| `normal/mov_dv_ntsc_411_pcm32k_720x480_6s.mov` | DV NTSC, **4:1:1**, bottom field first, SAR 8:9, 6 s | PCM 32 kHz | MiniDV 32 kHz audio mode | 4:1:1 chroma, 32 kHz audio |

DV runs at a fixed ~25 Mbit/s, so these clips are only 6 seconds long to keep
the repository small.

## Damaged files

| File | Source | Defect | Expected behavior | What it tests |
|---|---|---|---|---|
| `dataset/damage/damage_corrupt_3gp_h263_amrnb_176x144.3gp` | 3GP/H.263 clip | ~8 KiB overwritten mid-file | H.263 garbage, blocks, mosaic; AMR may click briefly | Decoder error recovery, skipping 3GP packets |
| `dataset/damage/damage_corrupt_asf_wmv1_wmav1_320x240.wmv` | ASF/WMV1 clip | ~8 KiB overwritten mid-file | Blocky WMV damage or audio pops; ideally only local | ASF packet location, WMA/WMV resilience |
| `dataset/damage/damage_corrupt_avi_msmpeg4v3_mp3_320x240.avi` | AVI/MSMPEG4 clip | ~8 KiB overwritten mid-file | MSMPEG4 garbage, maybe a short audio misalignment | AVI index/chunk recovery, limiting error propagation |
| `dataset/damage/damage_corrupt_mkv_mpeg2video_ac3_720x480_sar32-27.mkv` | MKV/MPEG-2 clip | ~8 KiB overwritten mid-file | Damage inside a GOP should recover at the next keyframe | Matroska cluster resync, MPEG-2 concealment |
| `dataset/damage/damage_corrupt_mpegts_mpeg2video_ac3_480x480_29-97.mpegts` | MPEG-TS clip | ~8 KiB overwritten mid-file | TS continuity errors, brief garbage or pops | PAT/PMT rescans, continuity counter, packet-loss recovery |
| `dataset/damage/damage_corrupt_rm_rv10_ac3_320x240.rm` | RM/RV10 clip | ~8 KiB overwritten mid-file | RV10 garbage or demuxer errors | RealMedia packet boundaries, RV10 recovery |
| `dataset/damage/damage_trunc_3gp_mpeg4_amrnb_128x96.3gp` | 3GP/MPEG-4 clip | Last ~3% removed | Error or graceful stop near the end | Missing tail, moov/index handling |
| `dataset/damage/damage_trunc_mkv_mpeg4asp_mp3_352x288_sar64-45.mkv` | MKV/MPEG-4 ASP clip | Last ~3% removed | Incomplete last cluster; play what is there | Tail cluster recovery, missing Cues |
| `dataset/damage/damage_trunc_mp4_mpeg4asp_mp3_640x360.mp4` | MP4/MPEG-4 clip | Last ~3% removed | moov is at the end, so the file may not open at all; ideally the player offers repair | Missing moov, MP4 repair, index rebuild |
| `dataset/damage/damage_trunc_rm_rv20_ac3_320x240.rmvb` | RMVB/RV20 clip | Last ~3% removed | Missing tail index/packets; must not loop forever | Missing RealMedia index |

### Additional: incomplete downloads and broken indexes (`generate_extra.py`)

| File | Defect | Expected behavior | What it tests |
|---|---|---|---|
| `damage/damage_zero_byte_empty_file.avi` | 0 bytes | Immediate error; no hang or crash | Empty files |
| `damage/damage_p2p_zero_holes_*` (AVI / MKV / RMVB) | One 64 KiB-aligned all-zero block at 1/3 and at 2/3 of the file, like unfinished BT/eMule pieces | Two stretches of garbage or skips, then recovery | Skipping zero-filled regions, resync |
| `damage/damage_headless_first64k_*` (MPG / TS / AVI / MKV) | First 64 KiB missing | PS/TS should resync and play; headless AVI/MKV usually cannot open and should fail clearly | Bitstream sync without a header |
| `damage/damage_noidx1_avi_msmpeg4v3_mp3_320x240.avi` | `idx1` removed while `avih` still claims an index | Plays; seeking needs a scan or index rebuild | Missing-index fallback |
| `damage/damage_badidx1_offsets_avi_msmpeg4v3_mp3_320x240.avi` | Last 2/3 of `idx1` offsets shifted by 4093 bytes | Trusting the index reads garbage; an ideal player notices and scans sequentially | Index validation |
| `damage/damage_trunc_mp4_faststart_moov_first_640x360.mp4` | MP4 with moov at the front, last 3% removed | Compare with the moov-at-end truncation above: this one should play up to the cut | How moov placement affects truncation tolerance |

## Degraded files

These are valid media files with typical defects from old sources, old capture,
repeated transcoding and repeated redistribution. See
[Degradation](DEGRADATION.md) for where each defect comes from.

| File | Parameters | Built-in defect | What it tests |
|---|---|---|---|
| `dataset/degraded/vhs_composite_wear_mpeg2_ac3_720x480.mkv` | MPEG-2/AC-3, 720×480, SAR 32:27, 29.97 fps | RGB/chroma shift, noise, smear, dropouts, tracking band | Stable rendering of a dirty picture; color conversion and error recovery |
| `dataset/degraded/chroma_under_bleed_mpeg2_ac3_720x480.mkv` | MPEG-2/AC-3, 720×480, SAR 32:27, 29.97 fps | VHS color-under chroma smear | Chroma upsampling, red/blue edge misregistration |
| `dataset/degraded/motion_ghost_trails_mpeg4_mp3_480x360.mp4` | MPEG-4/MP3, 480×360, 25 fps | `lagfun`/`tmix` inter-frame ghosting | Motion trails and reference-frame display |
| `dataset/degraded/generation_loss_x3_mpeg4_mp3_352x240.avi` | MPEG-2 → MPEG-4 → MPEG-4, three generations | Low-bitrate blocking, ringing, banding, smeared detail | Stable decoding after a lossy chain |
| `dataset/degraded/long_gop_bitstream_errors_mpeg4_mp3_480x360.avi` | MPEG-4/MP3, 300-frame GOP, encoder error rate | Long-GOP prediction and low-quality encoding | Error propagation, recovery after seeking |
| `dataset/degraded/damaged_i_frame_mpeg4_mp3_480x360.avi` | MPEG-4/MP3, 480×360, 96 bytes of an I-frame overwritten | Keyframe damage spreading into dependent frames | Specks/ghosts/mosaic until the next I-frame |
| `dataset/degraded/interlaced_wrong_handling_mpeg2_ac3_720x480.mkv` | MPEG-2/AC-3, 720×480, 29.97 fps, top field first | Interlaced frames built from 59.94 fields | Field order, combing, wrong progressive display |
| `dataset/degraded/telecine_judder_mpeg2_mp3_720x480.mpg` | MPEG-2/MP3, 720×480, 23.976 → 29.97 | Telecine repeated fields | Cadence detection, IVTC, judder |
| `dataset/degraded/vbr_mp3_audio_offset_mpeg4_352x240.avi` | MPEG-4/VBR MP3, 352×240 | AVI VBR MP3 + 350 ms offset | A/V delay, old AVI audio time base |
| `dataset/degraded/dropped_duplicated_frames_mpeg4_mp3_480x360.mkv` | MPEG-4/MP3, 480×360, 25 fps | Frames dropped, PTS renumbered | Skips, repeated frames, motion continuity |
