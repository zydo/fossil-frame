> **Snapshot** of <https://en.wikipedia.org/wiki/Generation_loss>
> Retrieved 2026-11-17; main content converted to Markdown.
> Copyright belongs to the original authors and publisher. This copy is kept
> only as a reference backup and is **not** covered by this repository's MIT license.
> Wikipedia text is available under CC BY-SA 4.0.

---

Loss of quality between copies

For other uses, see [Generation Loss (disambiguation)](https://en.wikipedia.org/wiki/Generation_Loss_(disambiguation) "Generation Loss (disambiguation)").

.png)

Digital generation loss induced by rotating a [JPEG](https://en.wikipedia.org/wiki/JPEG "JPEG") image 90 degrees (from top to bottom) 0, 100, 200, 500, 900, and 2000 times (without using lossless tools)

**Generation loss** is the loss of quality between subsequent [copies](https://en.wikipedia.org/wiki/Copying "Copying") or [transcodes](https://en.wikipedia.org/wiki/Transcoding "Transcoding") of data. Compression, as well as [up-scaling](https://en.wikipedia.org/wiki/Image_scaling "Image scaling") (with images) or [up-sampling](https://en.wikipedia.org/wiki/Upsampling "Upsampling") (with sound and other recordings) are common causes of generation loss. The introduction of [compression artifacts](https://en.wikipedia.org/wiki/Compression_artifact "Compression artifact") may increase the entropy of the data through each generation. Other causes include signal noise in analog systems and conversion between analog and digital formats.

## Analog generation loss

\[[edit](https://en.wikipedia.org/w/index.php?title=Generation_loss&action=edit&section=1 "Edit section: Analog generation loss")\]

In [analog](https://en.wikipedia.org/wiki/Analog_signal "Analog signal") systems (including systems that use [digital recording](https://en.wikipedia.org/wiki/Digital_recording "Digital recording") but make the copy over an analog connection), generation loss is mostly due to [noise](https://en.wikipedia.org/wiki/Signal_noise "Signal noise") and [bandwidth](https://en.wikipedia.org/wiki/Bandwidth_(signal_processing) "Bandwidth (signal processing)") issues in [cables](https://en.wikipedia.org/wiki/Electrical_cable "Electrical cable"), [amplifiers](https://en.wikipedia.org/wiki/Amplifier "Amplifier"), [mixers](https://en.wikipedia.org/wiki/Audio_mixer "Audio mixer"), recording equipment and anything else between the source and the destination. Poorly adjusted [distribution amplifiers](https://en.wikipedia.org/wiki/Distribution_amplifier "Distribution amplifier") and [mismatched impedances](https://en.wikipedia.org/wiki/Mismatched_impedance "Mismatched impedance") can make these problems even worse. Repeated conversion between analog and digital can also cause loss.

Generation loss was a major consideration in complex analog audio and [video editing](https://en.wikipedia.org/wiki/Video_editing "Video editing"), where multi-layered edits were often created by making intermediate mixes which were then "bounced down" back onto tape. Careful planning was required to minimize generation loss, and the resulting noise and poor frequency response.

One way of minimizing the number of generations needed was to use an audio mixing or video editing suite capable of mixing a large number of channels at once; in the extreme case, for example with a 48-track recording studio, an entire complex mixdown could be done in a single generation, although this was prohibitively expensive for all but the best-funded projects.

The introduction of professional [analog noise reduction systems](https://en.wikipedia.org/wiki/Noise_reduction#In_audio "Noise reduction") such as [Dolby A](https://en.wikipedia.org/wiki/Dolby_A "Dolby A") helped reduce the amount of audible generation loss, but were eventually superseded by digital systems which vastly reduced generation loss.^([\[1\]](#cite_note-ATIS-1))

According to [ATIS](https://en.wikipedia.org/wiki/Alliance_for_Telecommunications_Industry_Solutions "Alliance for Telecommunications Industry Solutions"), "Generation loss is limited to analog recording because digital recording and reproduction may be performed in a manner that is essentially free from generation loss."^([\[1\]](#cite_note-ATIS-1))

## Digital generation loss

\[[edit](https://en.wikipedia.org/w/index.php?title=Generation_loss&action=edit&section=2 "Edit section: Digital generation loss")\]

When used correctly, digital technology can eliminate generation loss. This implies the exclusive use of lossless compression codecs or uncompressed data from recording or creation until the final lossy encode for distribution through internet streaming or optical discs. Copying a digital file gives an exact copy if the equipment is operating properly which eliminates generation loss caused by copying, while reencoding digital files with lossy compression codecs can cause generation loss. This trait of digital technology has given rise to awareness of the risk of unauthorized copying. Before digital technology was widespread, a [record label](https://en.wikipedia.org/wiki/Record_label "Record label"), for example, could be confident knowing that unauthorized copies of their music tracks were never as good as the originals.

Generation loss can still occur when using lossy video or audio compression codecs as these introduce artifacts into the source material with each encode or reencode. Lossy compression codecs such as [Apple ProRes](https://en.wikipedia.org/wiki/Apple_ProRes "Apple ProRes"), [Advanced Video Coding](https://en.wikipedia.org/wiki/Advanced_Video_Coding "Advanced Video Coding") and [mp3](https://en.wikipedia.org/wiki/Mp3 "Mp3") are very widely used as they allow for dramatic reductions on file size while being indistinguishable from the uncompressed or losslessly compressed original for viewing purposes. The only way to avoid generation loss is by using uncompressed or losslessly compressed files; which may be expensive from a storage standpoint as they require larger amounts of storage space in flash memory or hard drives per second of runtime. Uncompressed video requires a high data rate; for example, a 1080p video at 60 frames per second require approximately 370 megabytes per second.^([\[2\]](#cite_note-2)) Lossy codecs make Blu-rays and streaming video over the internet feasible since neither can deliver the amounts of data needed for uncompressed or losslessly compressed video at acceptable frame rates and resolutions. Images can suffer from generation loss in the same way video and audio can.

Processing a [lossily compressed](https://en.wikipedia.org/wiki/Data_compression "Data compression") file rather than an original usually results in more loss of quality than generating the same output from an uncompressed original. For example, a low-resolution digital image for a web page is better if generated from an uncompressed [raw image](https://en.wikipedia.org/wiki/Raw_image "Raw image") than from an already-compressed [JPEG](https://en.wikipedia.org/wiki/JPEG "JPEG") file of higher quality.

### Techniques that cause generation loss in digital systems

\[[edit](https://en.wikipedia.org/w/index.php?title=Generation_loss&action=edit&section=3 "Edit section: Techniques that cause generation loss in digital systems")\]

In [digital systems](https://en.wikipedia.org/wiki/Digital_systems "Digital systems"), several techniques such as lossy compression codecs and algorithms, used because of other advantages, may introduce generation loss and must be used with caution. However, copying a digital file itself incurs no generation loss—the copied file is identical to the original, provided a perfect copying [channel](https://en.wikipedia.org/wiki/Communication_channel "Communication channel") is used.

Some [digital transforms](https://en.wikipedia.org/wiki/Digital_transform "Digital transform") are reversible, while some are not. [Lossless compression](https://en.wikipedia.org/wiki/Lossless_compression "Lossless compression") is, by definition, fully reversible, while [lossy compression](https://en.wikipedia.org/wiki/Lossy_compression "Lossy compression") throws away some data which cannot be restored. Similarly, many [DSP](https://en.wikipedia.org/wiki/Digital_signal_processing "Digital signal processing") processes are not reversible.

Thus careful planning of an [audio](https://en.wikipedia.org/wiki/Sound "Sound") or [video](https://en.wikipedia.org/wiki/Video "Video") signal chain from beginning to end and rearranging to minimize multiple conversions is important to avoid generation loss when using lossy compression codecs. Often, arbitrary choices of numbers of pixels and sampling rates for source, destination, and intermediates can seriously degrade digital signals in spite of the potential of digital technology for eliminating generation loss completely.

Similarly, when using lossy compression, it will ideally only be done once, at the end of the workflow involving the file, after all required changes have been made.

#### Transcoding

\[[edit](https://en.wikipedia.org/w/index.php?title=Generation_loss&action=edit&section=4 "Edit section: Transcoding")\]

Main article: [Transcoding](https://en.wikipedia.org/wiki/Transcoding "Transcoding")

Converting between lossy formats – be it decoding and re-encoding to the same format, between different formats, or between different [bitrates](https://en.wikipedia.org/wiki/Bit_rate "Bit rate") or parameters of the same format – causes generation loss.

Repeated applications of [lossy compression](https://en.wikipedia.org/wiki/Lossy_compression "Lossy compression") and decompression can cause generation loss, particularly if the parameters used are not consistent across generations. Ideally an algorithm will be both *[idempotent](https://en.wikipedia.org/wiki/Idempotent "Idempotent"),* meaning that if the signal is decoded and then re-encoded with identical settings, there is no loss, and *scalable,* meaning that if it is re-encoded with lower quality settings, the result will be the same as if it had been encoded from the original signal – see [Scalable Video Coding](https://www.intel.com/content/www/us/en/developer/articles/technical/scalable-video-technology.html). More generally, transcoding between different parameters of a particular encoding will ideally yield the greatest common shared quality – for instance, converting from an image with 4 bits of red and 8 bits of green to one with 8 bits of red and 4 bits of green would ideally yield simply an image with 4 bits of red color depth and 4 bits of green color depth without further degradation.

Some lossy compression [algorithms](https://en.wikipedia.org/wiki/Algorithm "Algorithm") are much worse than others in this regard, being neither idempotent nor scalable, and introducing further degradation if parameters are changed.

For example, with [JPEG](https://en.wikipedia.org/wiki/JPEG "JPEG"), changing the quality setting will cause different quantization constants to be used, causing additional loss. Further, as JPEG is divided into 16×16 blocks (or 16×8, or 8×8, depending on [chroma subsampling](https://en.wikipedia.org/wiki/Chroma_subsampling "Chroma subsampling")), cropping that does not fall on an 8×8 boundary shifts the encoding blocks, causing substantial degradation – similar problems happen on rotation. This can be avoided by the use of jpegtran or similar tools for cropping. Similar degradation occurs if [video keyframes](https://en.wikipedia.org/wiki/Keyframe#Key_frames_of_video_editing "Keyframe") do not line up from generation to generation.

#### Editing

\[[edit](https://en.wikipedia.org/w/index.php?title=Generation_loss&action=edit&section=5 "Edit section: Editing")\]

Digital [resampling](https://en.wikipedia.org/wiki/Resampling_(bitmap) "Resampling (bitmap)") such as [image scaling](https://en.wikipedia.org/wiki/Image_scaling "Image scaling"), and other [DSP](https://en.wikipedia.org/wiki/Digital_signal_processing "Digital signal processing") techniques can also introduce artifacts or degrade [signal-to-noise ratio](https://en.wikipedia.org/wiki/Signal-to-noise_ratio "Signal-to-noise ratio") (S/N ratio) each time they are used, even if the underlying storage is lossless. When making a copy of a copy, the quality of the image will deteriorate with every ‘generation’.

Lossy image formats, such as [JPEG](https://en.wikipedia.org/wiki/JPEG "JPEG"), introduce degradation when files are repeatedly edited and re-saved. While directly copying a JPEG file preserves its quality, opening and saving it in an image editor creates a new, re-encoded version, introducing subtle changes. Social media platforms like [Facebook](https://en.wikipedia.org/wiki/Facebook "Facebook") and [X, formerly known as Twitter](https://en.wikipedia.org/wiki/Twitter "Twitter"), automatically re-encode uploaded images at low-quality settings to optimize storage and bandwidth, further compounding compression artifacts. Over time, repeated re-encoding or processing can significantly degrade the image's quality.

Resampling causes [aliasing](https://en.wikipedia.org/wiki/Aliasing "Aliasing"), both blurring low-frequency components and adding high-frequency noise, causing [jaggies](https://en.wikipedia.org/wiki/Jaggies "Jaggies"), while rounding off computations to fit in finite precision introduces [quantization](https://en.wikipedia.org/wiki/Quantization_(signal_processing) "Quantization (signal processing)"), causing [banding](https://en.wikipedia.org/wiki/Colour_banding "Colour banding"); if fixed by [dither](https://en.wikipedia.org/wiki/Dither "Dither"), this instead becomes noise. In both cases, these at best degrade the signal's S/N ratio, and may cause artifacts. Quantization can be reduced by using high precision while editing (notably floating point numbers), only reducing back to fixed precision at the end.

Often, particular implementations fall short of theoretical ideals.

## Examples

\[[edit](https://en.wikipedia.org/w/index.php?title=Generation_loss&action=edit&section=6 "Edit section: Examples")\]

|  |  |
|----|----|
| [![\[icon\]](https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1c/Wiki_letter_w_cropped.svg/20px-Wiki_letter_w_cropped.svg.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail)](https://en.wikipedia.org/wiki/File:Wiki_letter_w_cropped.svg) | This section **needs expansion** with: additional examples and further details. You can help by [adding missing information](https://en.wikipedia.org/w/index.php?title=Generation_loss&action=edit&section=). *(February 2017)* |

Successive generations of photocopies result in image distortion and degradation.^([\[3\]](#cite_note-3)) Repeatedly downloading and then reposting / reuploading content to platforms such as [Instagram](https://en.wikipedia.org/wiki/Instagram "Instagram") or [YouTube](https://en.wikipedia.org/wiki/YouTube "YouTube") can result to noticeable quality degradation.^([\[4\]](#cite_note-Simpson-4)[\[5\]](#cite_note-5)[\[6\]](#cite_note-6)) Similar effects have been documented in copying of [VHS](https://en.wikipedia.org/wiki/VHS "VHS") tapes.^([\[7\]](#cite_note-7)) This is because both services use lossy codecs on all data that is uploaded to them, even if the data being uploaded is a duplicate of data already hosted on the service, while VHS is an analog medium, where effects such as noise from interference can have a much more noticeable impact on recordings.

## See also

\[[edit](https://en.wikipedia.org/w/index.php?title=Generation_loss&action=edit&section=7 "Edit section: See also")\]

- [Signal-to-noise ratio](https://en.wikipedia.org/wiki/Signal-to-noise_ratio "Signal-to-noise ratio")
- [Editing digital images](https://en.wikipedia.org/wiki/Editing_digital_images "Editing digital images")
- [Lossless data compression](https://en.wikipedia.org/wiki/Lossless_data_compression "Lossless data compression")
- [Data degradation](https://en.wikipedia.org/wiki/Data_degradation "Data degradation")
- [Data loss](https://en.wikipedia.org/wiki/Data_loss "Data loss")
- [Model collapse](https://en.wikipedia.org/wiki/Model_collapse "Model collapse")
- [Software rot](https://en.wikipedia.org/wiki/Software_rot "Software rot")
- *[I Am Sitting in a Room](https://en.wikipedia.org/wiki/I_Am_Sitting_in_a_Room "I Am Sitting in a Room")*
- *[The Disintegration Loops](https://en.wikipedia.org/wiki/The_Disintegration_Loops "The Disintegration Loops")*
- [Ship of Theseus](https://en.wikipedia.org/wiki/Ship_of_Theseus "Ship of Theseus")

## Notes

\[[edit](https://en.wikipedia.org/w/index.php?title=Generation_loss&action=edit&section=8 "Edit section: Notes")\]

1.  [1](#cite_ref-ATIS_1-0) [2](#cite_ref-ATIS_1-1) ["generation loss"](https://web.archive.org/web/20170123114527/http://www.atis.org/glossary/definition.aspx?id=5003). *ATIS Telecom Glossary*. [Alliance for Telecommunications Industry Solutions](https://en.wikipedia.org/wiki/Alliance_for_Telecommunications_Industry_Solutions "Alliance for Telecommunications Industry Solutions"). September 28, 2016. Archived from [the original](http://www.atis.org/glossary/definition.aspx?id=5003) on 2017-01-23. Retrieved September 28, 2016.
2.  [↑](#cite_ref-2) ["H.264 is magic: A technical walkthrough of a remarkable technology"](https://sidbala.com/h-264-is-magic/). 2 November 2016.
3.  [↑](#cite_ref-3) ["Generation loss"](http://www.webopedia.com/TERM/G/generation_loss.html). Webopedia. March 2007. Retrieved September 28, 2016.
4.  [↑](#cite_ref-Simpson_4-0) Simpson, Isaac (December 4, 2013). ["Copying a YouTube video 1,000 times is a descent into hell"](http://www.dailydot.com/unclick/youtube-video-1000-copies-generation-loss/). *[The Daily Dot](https://en.wikipedia.org/wiki/The_Daily_Dot "The Daily Dot")*. Retrieved September 28, 2016 – via YouTube.
5.  [↑](#cite_ref-5) [Zhang, Michael](https://en.wikipedia.org/wiki/Xiaoquan_(Michael)_Zhang "Xiaoquan (Michael) Zhang") (February 11, 2015). ["Experiment Shows What Happens When You Repost a Photo to Instagram 90 Times"](http://petapixel.com/2015/02/11/experiment-shows-happens-repost-photo-instagram-90-times/). Petapixel. Retrieved September 28, 2016.
6.  [↑](#cite_ref-6) Zhang, Michael (June 4, 2010). ["I Am Sitting in a Room, YouTube Style"](http://petapixel.com/2010/06/04/i-am-sitting-in-a-room-youtube-style/). Petapixel. Retrieved September 28, 2016.
7.  [↑](#cite_ref-7) ["VHS generation loss (50fps)"](https://www.youtube.com/watch?v=G8GOcB6H0uQ). *YouTube*. December 4, 2016. Retrieved September 11, 2024.

## External links

\[[edit](https://en.wikipedia.org/w/index.php?title=Generation_loss&action=edit&section=9 "Edit section: External links")\]

- Sneyers, Jon (April 10, 2016). ["Generation Loss at High Quality Settings"](https://www.youtube.com/watch?v=N1pSch9F9ZQ) (Video). [Archived](https://ghostarchive.org/varchive/youtube/20211213/N1pSch9F9ZQ) from the original on 2021-12-13. Retrieved September 29, 2016 – via YouTube.
