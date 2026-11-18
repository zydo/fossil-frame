English | [中文](PROPRIETARY_GAPS.zh-CN.md)

# Proprietary formats that cannot be synthesized

[← Back to README](../README.md)

The dataset only contains formats FFmpeg can encode. FFmpeg has decoders but no
open-source encoders for the formats below, so there are **no** samples for them:

| Format | Era / use | Closest sample here | What that sample cannot test |
|---|---|---|---|
| RealVideo 3/4 (RV30/RV40) | 2000s `.rmvb` downloads | `normal/rm_rv20_ac3_320x240.rmvb` (RV20) | The RV40 decoder, index behavior of true VBR RMVB |
| Cook (RealAudio G2/8), SIPR | RM audio of the same era | AC-3 in RM, RealAudio 1.0 (`real_144`) | Cook/SIPR decoding |
| WMV3 / VC-1 (WMV9) | `.wmv` after 2003 | WMV1, WMV2 | WMV9 decoding, VC-1 profiles |
| WMA Pro / WMA Lossless / WMA Voice | WMV9 era | WMA v1, v2 | Multichannel WMA Pro |
| Intel Indeo 3/4/5 | 1990s games and CD-ROMs | Cinepak, MS Video-1 | Indeo decoding |
| QDesign Music 2 (QDM2) | QuickTime 4–6 trailers | IMA4, PCM | QDM2 decoding |

Cinepak, Sorenson Video 1, MS Video-1, QuickTime RLE/SMC/RPZA, DV, HuffYUV, ZMBV,
Flash Screen Video and H.261 do have open-source encoders and are included; see
the [Catalog](CATALOG.md).

## Adding these formats

1. Use only samples that are lawfully obtained and allowed for testing, for
   example by re-encoding this repository's reference signal with an original
   encoder you hold a license for (RealProducer, Windows Media Encoder 9, …).
   The content then stays self-explaining and involves no third-party
   copyrighted material.
2. Put them in a separate `dataset/external/`, not in the directories the
   generators reproduce.
3. Add rows to `manifest.csv`, and record the source, encoder version and
   licensing basis in this file and its Chinese counterpart.
