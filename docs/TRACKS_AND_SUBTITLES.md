English | [中文](TRACKS_AND_SUBTITLES.zh-CN.md)

# Audio tracks and subtitles (tracks / subtitles)

[← Back to README](../README.md)

Both categories are produced by `generate_extra.py`. The picture is still the
12-second reference signal; the yellow title line says what you should hear or
see.

## tracks/: multiple tracks, channel semantics, legacy sample formats

| File | Content | Correct behavior | Common failure |
|---|---|---|---|
| `vcd_karaoke_left1khz_right500hz_mpeg1_352x240.mpg` | VCD; left channel a short 1 kHz beep every second ("vocal"), right channel a longer 500 Hz beep ("karaoke") | Switching left/right channel (or vocal/karaoke) leaves only one pitch | No channel selector; L/R mixed to mono up front |
| `dvd_dual_audio_ac3-1khz_lpcm-2khz_720x480.vob` | DVD VOB; track 1 AC-3 at 1 kHz, track 2 LPCM (`pcm_dvd`) at 2 kHz | Both tracks listed and switchable | LPCM substream ignored; wrong track chosen by default |
| `dvd_ac351_channel_id_720x480.vob` | AC-3 5.1; in second N only one channel sounds: `N mod 6` = 0 FL, 1 FR, 2 C, 3 LFE (80 Hz), 4 BL, 5 BR | Correct speaker positions on surround output; C/LFE/rears still audible when downmixed to stereo | Channel order shifted; downmix drops center or LFE |
| `dvd_dts51_channel_id_720x480.vob` | Same as above, DTS 5.1 | Same; also tests S/PDIF/HDMI passthrough | Missing DTS decoder; silent when passthrough fails |
| `mkv_multilang_zho-1khz_eng-2khz-default_jpn51_320x240.mkv` | Three tracks: zho AAC 1 kHz (not default), eng MP3 2 kHz (**default**), jpn AC-3 5.1 channel ID | Plays 2 kHz by default; track names and language tags shown correctly | Ignores the default flag and always plays the first track |
| `avi_mpeg4_mulaw_8khz_mono_320x240.avi` | G.711 μ-law 8 kHz mono | Clean beep aligned with the bar | μ-law played as linear PCM sounds harshly distorted |

8-bit PCM (11.025 / 22.05 kHz), 32 kHz DV audio, IMA4, G.726, Speex and SWF ADPCM
are in the additional-codecs table of the [Catalog](CATALOG.md).

Known limits: MPEG-PS does not carry track languages (on DVD they live in the
IFO), so the VOB samples only test track listing and switching. FFmpeg's PS
muxer leaves one packet with a duplicate DTS at the end of the AC-3/DTS 5.1 VOBs,
which shows up as 1–5 "non monotonically increasing dts" messages when
decoding; the content is complete.

## subtitles/: subtitle encodings and formats

Reference video: `subtitle_reference_mpeg4_mp3_720x480.avi` (MPEG-4/MP3, 720×480,
SAR 32:27, 25 fps). Every subtitle shows "第 N 秒 中文字幕測試 / sec N" from N.000
to N.900 s, i.e. together with the beep, the bar and the `sec N` counter. Early
or late subtitles mean a timing bug.

External subtitles (all file names start with the reference video name, so
players can auto-load them; they can also be loaded by hand):

| File | Format / encoding | What it tests |
|---|---|---|
| `*.gbk.srt` | SRT, GBK, no BOM, CRLF | Detecting Chinese without a BOM; mojibake means it was read as Latin-1/UTF-8 |
| `*.big5.srt` | SRT, Big5 | Traditional Chinese detection; GBK/Big5 confusion produces wrong characters |
| `*.utf8bom.srt` | SRT, UTF-8 with BOM | The BOM must not appear as a stray character |
| `*.utf16le.srt` | SRT, UTF-16LE with BOM | Wide encodings; unsupported means all garbage or blank |
| `*.ssa` | SubStation Alpha v4 (not ASS) | Legacy SSA style header, `Marked=` field; Chinese at the bottom, English at the top |
| `*.microdvd-25fps.sub` | MicroDVD, frame-based, no frame-rate header | The player should convert using the video's 25 fps |
| `*.microdvd-23.976fps-header.sub` | MicroDVD with `{1}{1}23.976` first line | Should honor the 23.976 header; using 25 fps makes subtitles drift earlier |
| `*.vobsub.idx` + `*.vobsub.sub` | VobSub bitmap subtitles (DVD SPU, 2-bit RLE) | Bitmap subtitle parsing, palette and transparency |

Embedded subtitles:

| File | Content | What it tests |
|---|---|---|
| `mkv_srt-zho_ass-fontattach_vobsub_720x480.mkv` | SRT (zho, default), ASS (eng), VobSub; attached font `PressStart2P-Regular.ttf` | The top ASS line reads "PIXEL FONT = ATTACHMENT OK N". A pixel font means the attachment was loaded; a regular font means it was ignored |
| `dvd_mpeg2_ac3_vobsub_720x480.vob` | DVD subpicture stream 0x20 | Detecting subtitle streams in VOB |
| `mpegts_mpeg2_mp2_dvbsub_720x480.ts` | DVB bitmap subtitles (transcoded from VobSub) | Broadcast TS subtitles; each cue has a display and a clear packet, 22 packets total |

The VobSub bitmaps come from an SPU encoder built into `generate_extra.py`: the
text is rendered to grayscale with FFmpeg `drawtext`, quantized to transparent /
white / dark-gray outline, and DVD-RLE encoded. Rendering uses a system font, but
only the resulting bitmap goes into the dataset, not the font file.
