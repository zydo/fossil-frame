English | [中文](STRUCTURE.zh-CN.md)

# Container structure, timestamps and metadata (structure / mislabeled)

[← Back to README](../README.md)

Files in `structure/` are valid (or nearly valid) but carry structural traits
common in old files. `mislabeled/` holds copies whose extension does not match
the real format. Everything is produced by `generate_extra.py`.

## Indexes and interleaving

| File | Trait | Correct behavior |
|---|---|---|
| `mkv_no_cues_written_to_pipe_320x240.mkv` | Written to a pipe, so it has no Cues (common for stream recordings) | Plays; seeking scans clusters instead of being disabled |
| `mp4_faststart_moov_first_640x360.mp4` | moov at the front | Compare with `damage/damage_trunc_mp4_faststart...` |
| `avi_noninterleaved_audio_at_end_320x240.avi` | All video chunks first, all audio chunks after | Random access via idx1 keeps A/V in sync; sequential readers lose audio or thrash the disk |
| `avi_zero_length_dropped_frame_chunks_320x240.avi` | Between 3 and 4 s every other video chunk is 0 bytes (capture drop placeholders) | The previous frame repeats; no timing drift |
| `avi_divx5_packed_bframes_mpeg4_mp3_480x360.avi` | DivX 5 "packed bitstream": P+B in one chunk followed by an N-VOP chunk; carries `DivX503b1393p` user data | Plays with correct B-frame order; FFmpeg reports packed B-frames, and `mpeg4_unpack_bframes` restores them |

## Timestamps

| File | Trait | Correct behavior |
|---|---|---|
| `mpegts_pts_wrap_33bit_at_3.7s_480x480.ts` | Starting PTS ≈ 95440 s, wraps past 2^33 at about 3.7 s | No stall, jump to start or hang at the wrap |
| `mpegts_resolution_aspect_switch_720x480-4x3_16x9_352x240.ts` | Switches every 4 s: 720×480 4:3 → 720×480 16:9 → 352×240 | Correct geometry after each switch, no black screen |
| `mpegts_audio_samplerate_switch_48k_44k_32k_320x240.ts` | MP2 sample rate changes every 4 s: 48 → 44.1 → 32 kHz | Pitch unchanged, beeps still aligned; a short gap at a switch is acceptable |
| `concat_vts_01_1_plus_2_timestamp_reset_720x480.vob` | Two VOBs concatenated; timestamps restart at 6 s | Keeps playing sec 6–11; duration may be wrong but must not hang |
| `concat_cat_vcd_ntsc_352x240_plus_pal_352x288.mpg` | `cat` of an NTSC VCD and a PAL VCD: resolution, frame rate and timestamps all change | The second part is neither cropped nor stretched |
| `mkv_vfr_hybrid_23.976_then_29.97_h264_640x360.mkv` | 0–6 s at 23.976 fps, 6–12 s at 29.97 fps | The moving bar stays smooth; no repeated frame every second |
| `mp4_vfr_hybrid_23.976_then_29.97_h264_640x360.mp4` | Same, MP4 stts | Same |
| `mkv_video_starts_0.5s_after_audio_320x240.mkv` | First video PTS 0.52 s, audio starts at 0 | Black or first frame for 0.5 s, then beep and bar aligned |
| `mkv_audio_timestamp_gap_4s-5s_320x240.mkv` | No audio packets between 4 and 5 s | Silence is inserted and sync holds after 5 s; later audio is not played early |
| `mkv_video_timestamp_gap_4s-5s_320x240.mkv` | No video frames between 4 and 5 s | Picture freezes for 1 s, then jumps to sec 5; audio unaffected |
| `mov_editlist_empty_first_1s_320x240.mov` | First edit-list entry is a 1 s empty edit; H.264 with B-frames | No picture for the first second, then in sync; ignoring the edit list shifts everything 1 s early |

## Metadata

| File | Trait | Correct behavior |
|---|---|---|
| `mp4_display_rotation_90_h264_aac_360x640.mp4` | Stored landscape 640×360, display matrix rotates 90° counter-clockwise | Shown in portrait with upright text ("UPRIGHT IF ROT 90 OK") |
| `3gp_display_rotation_270_h263_amrnb_176x144.3gp` | Phone-style 3GP, H.263 176×144, rotation 270 | Same |
| `mkv_chapters_every_3s_320x240.mkv` / `mp4_chapters_every_3s_320x240.mp4` | Four Chinese-titled chapters at 0/3/6/9 s | Chapter list shows "第 N 章 / sec …" and jumps accurately |
| `avi_info_title_gbk_320x240.avi` | AVI `INFO/INAM` holds the GBK bytes for "老电影 测试 GBK 标题" | Shown correctly or with a code-page fallback; must not crash |
| `rm_title_gbk_rv10_320x240.rm` | RealMedia CONT title in GBK | Same |
| `mkv_sd_720x576_bt709_tagged_mpeg2.mkv` | SD resolution, but encoded and tagged as BT.709 | Decoded per the tag; guessing 601 from resolution shifts colors |
| `mkv_hd_1280x720_bt709_untagged_h264.mkv` | HD, BT.709 encoded, **no** color tags | Guessing 709 from resolution gives correct patches |
| `mkv_hd_1280x720_bt601_tagged_h264.mkv` | HD, but encoded and tagged as BT.601 | Decoded per the tag; ignoring it shifts reds and greens |

## Interlaced HD

| File | Trait | Correct behavior |
|---|---|---|
| `m2ts_h264_mbaff_tff_ac3_1440x1080i_sar4-3.m2ts` | AVCHD style: 192-byte M2TS packets, H.264 MBAFF, top field first, SAR 4:3 | Smooth after deinterlacing; displayed as 1920×1080 |
| `hdv_mpeg2_tff_mp2_1440x1080i_sar4-3.m2t` | HDV style: MPEG-2 1440×1080i, top field first, MP2 384k | Same |

## Edge-case files

| File | Trait |
|---|---|
| `mkv_single_frame_320x240.mkv` | A single frame, no audio |
| `avi_audio_only_mp3.avi` | AVI with only an MP3 track |
| `avi_video_only_msmpeg4v3_320x240.avi` | No audio track |

The 0-byte file is `damage/damage_zero_byte_empty_file.avi`.

## mislabeled/: extension does not match content

| File | Real format |
|---|---|
| `actually_mkv_named.rmvb` | Matroska (MPEG-4 ASP) |
| `actually_mpegps_named.avi` | MPEG-1 PS |
| `actually_avi_named.wmv` | AVI (MSMPEG4 v3) |
| `actually_rm_named.avi` | RealMedia (RV10) |
| `actually_flv_named.mp4` | FLV (Sorenson Spark) |
| `actually_mp4_named.3gp.avi` | MP4 (double extension) |

A player should probe the content to pick the format. One that trusts the
extension picks the wrong demuxer and reports a "corrupt file" or refuses to open.
