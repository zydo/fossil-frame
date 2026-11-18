[English](SOURCE_MATERIAL.md) | 中文

# 素材来源

[← 返回 README](../README.zh-CN.md)

`dataset/` 没有使用外部照片、音乐视频、下载素材或第三方媒体文件：

- 画面由 FFmpeg `testsrc2`、`color` 源和 `drawtext`/`drawbox`/`drawgrid` 滤镜实时
  合成；`degraded/` 在此之上追加 `noise`、`rgbashift`、`chromashift`、`lagfun`、
  `tmix`、`tinterlace` 等滤镜。
- 音频全部由 `aevalsrc` 合成：每秒一次的短蜂鸣（默认 1 kHz）。多音轨和声道
  识别样本使用不同频率的蜂鸣。
- 字幕文本由 `generate_extra.py` 写出；VobSub/DVB 位图由生成器用 `drawtext`
  渲染后编码。
- `damage/`、`mislabeled/` 和部分 `structure/` 样本是对上述合成文件做确定性
  字节改写、截断、拼接或重排得到的。

画面文字渲染使用本机系统字体（macOS Arial / Hiragino Sans GB 等，可用
`SUITE_FONT` 指定）。字体只用来生成像素，字体文件不进入数据集。

## 附带的第三方字体

`assets/fonts/PressStart2P-Regular.ttf` 作为 MKV 附件字体，嵌入
`dataset/subtitles/mkv_srt-zho_ass-fontattach_vobsub_720x480.mkv`，用来测试附件
字体加载。字体为 Copyright 2012 The Press Start 2P Project Authors，采用
SIL Open Font License 1.1，允许随软件再分发；许可证全文见
`assets/fonts/OFL.txt`。

## 参考资料快照

`docs/references/` 保存文档所引用外部网页的 Markdown 快照（2026-11-17 抓取），
防止原链接失效；每个快照都与原链接并列给出。它们属于第三方内容，版权归原作者
与发布方所有，**不**适用本仓库的 MIT 许可证。每个快照开头都注明了来源。

## 说明图

`assets/aspect_preview.png` 和 `assets/degradation_preview.png` 是从数据集抽帧
得到的说明图，不是生成器的输入。

## 重新生成

```bash
python3 generate_suite.py --outdir dataset
python3 generate_degradation.py --outdir dataset
python3 generate_extra.py --outdir dataset
./tools/verify.sh
```
