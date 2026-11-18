[English](PROPRIETARY_GAPS.md) | 中文

# 无法合成的专有格式

[← 返回 README](../README.zh-CN.md)

数据集只包含 FFmpeg 能编码的格式。下列格式 FFmpeg 只有解码器，没有开源编码器，
所以这里**没有**对应样本：

| 格式 | 年代/场景 | 现有替代样本 | 替代样本测不到什么 |
|---|---|---|---|
| RealVideo 3/4 (RV30/RV40) | 2000 年代 `.rmvb` 下载 | `normal/rm_rv20_ac3_320x240.rmvb`（RV20） | RV40 解码器、真正 VBR RMVB 的索引行为 |
| Cook (RealAudio G2/8)、SIPR | 同一时期的 RM 音频 | RM 内 AC-3、RealAudio 1.0 (`real_144`) | Cook/SIPR 解码 |
| WMV3 / VC-1 (WMV9) | 2003 年后的 `.wmv` | WMV1、WMV2 | WMV9 解码、VC-1 profile |
| WMA Pro / WMA Lossless / WMA Voice | WMV9 时代 | WMA v1、v2 | 多声道 WMA Pro |
| Intel Indeo 3/4/5 | 90 年代游戏、光盘 | Cinepak、MS Video-1 | Indeo 解码 |
| QDesign Music 2 (QDM2) | QuickTime 4–6 预告片 | IMA4、PCM | QDM2 解码 |

Cinepak、Sorenson Video 1、MS Video-1、QuickTime RLE/SMC/RPZA、DV、HuffYUV、
ZMBV、Flash Screen Video、H.261 有开源编码器，已经收录，见 [CATALOG.md](CATALOG.zh-CN.md)。

## 如果需要补这些格式

1. 只使用来源合法、允许测试使用的样本，例如用自己持有许可证的原厂编码器
   （RealProducer、Windows Media Encoder 9 等）对本仓库的参考信号重新编码。
   这样内容仍可自解释，也不涉及第三方版权素材。
2. 放进单独的 `dataset/external/`，不要混进由生成器复现的目录。
3. 在 `manifest.csv` 追加行，并在本文件及其英文版记录来源、编码器版本和授权依据。
