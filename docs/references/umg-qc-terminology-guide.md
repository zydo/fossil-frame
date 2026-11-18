> **Snapshot** of <https://contentguide.universalmusic.com/qc-terminology-guide>
> Retrieved 2026-11-17; main content converted to Markdown.
> Copyright belongs to the original authors and publisher. This copy is kept
> only as a reference backup and is **not** covered by this repository's MIT license.
> The site blocks direct downloads (Incapsula), so this copy was extracted with Tavily. Images were dropped; one Outlook SafeLinks tracking URL was replaced by its target.

---

# QC TERMINOLOGY GUIDE

This page contains brief explanations for common audio and video terms that are used during QC of video assets submitted to Universal Music Group.

# VIDEO ISSUES

### Compression Artifacts

* Noticeable distortion of video caused by the application of lossy compression (for example, the H.264 video codec) or lower than 10-bit color processing. The two most common varieties of compression artifacts are:
* **Macroblocking**
  + When areas of an image appear to be made up of small squares rather than lifelike detail without boundary.
* **Banding / Posterization**
  + Abrupt, sometimes jagged change from one shade of color to another instead of a smooth, fading gradient.

### Digital Hit

* Visual corruption in a video file that results in (usually momentary) shifts in pixels or visible artifacts. Typically caused by an encoding error.
* The best fix for a hit is to re-encode / re-export the file from a source without the hit.
* Also known as a “video hit,” or when specific to tape sourced material, a “tape hit”.

### Chroma or Luma Shift

* A sudden change in color or brightness. Typically caused by human error in the color grading process. More rarely caused by computational error in the encoding/render process.

### Chroma Bleed

* When pigments in a color image appear out of place or spill over from the photographed location. Can be caused by color signals in a video being misaligned.

### Chroma Noise

* Splotchy fluctuations of color tone between pixels.

### Moiré

* A rippled pattern appearing in images when lines are so close that the imaging system has difficulty differentiating them. Striped clothing and Venetian blinds are common sources of moiré.
* Can be colored or colorless.

### Dead Pixel

* A loss of data at a specific spot in an image. Usually the result of an image recorded on a camera with a sensor defect.
* More rarely, dead pixels can also be the result of an encoding or editing error.

### Blanking

* A loss of video at the edge of a frame, presenting as a black band, either horizontal or vertical. Typically the result of an editing error or an older SD video master being submitted without first being cropped to it’s clean aperture.

### Visible VBI Information

* In an analog video signal, the vertical blanking interval (VBI), is the time between the end of the final line of a frame or field and the beginning of the first line of the next frame. The vertical blanking interval was often used to datacast information such as timecode and closed captioning, since nothing sent during the VBI is displayed on the screen when broadcast correctly. This information can become visible as white lines along the top edge of the image when an improper transfer from analog to digital video is performed.

### Matte Shifts

* When mattes slightly change size from shot-to-shot. This is rarely intentional, and usually an editing error.
* Please note these are different than major, symmetrical matte changes, which are typical of mixed aspect ratio videos and generally intended.

### Aliasing

* When the limited spatial sampling of an image causes the edges of objects or subjects to appear jagged.
* Can be unintentionally introduced through scaling operations, deinterlace processing, or lossy video compression.
* Often referred to as “jaggies” or “stair-stepping”.

### Skipped Frames

* When one or more frames of the originally captured video have been removed, causing a jump in motion or continuously choppy motion.
* A consistent pattern of skipped frames is a severe issue that is usually caused by a destructive frame rate conversion. Common manifestations of this include:
  + Every 4th frame being skipped in a 24 fps video.
    - This indicates a destructive frame rate conversion from 30 to 24 fps has occurred.
  + Every 5th frame being skipped in a 25 fps video.
    - This indicates a destructive frame rate conversion from 30 to 25 fps has occurred.
  + Every 25th frame being skipped in a 24 fps video.
    - This indicates a destructive frame rate conversion from 25 to 24 fps has occurred.

### Duplicate Frames

* When one or more frames of the video appear identical to the frame before it, causing choppy motion.
* A consistent pattern of duplicate frames is referred to as a “duplicate frame cadence” and is a severe issue that is usually caused by a destructive frame rate conversion. Common manifestations of this include:
  + 4:1 duplicate frame cadence on a 30 fps file.
    - Four frames of active motion, followed by one duplicate frame throughout program.
    - This indicates a destructive frame rate conversion from 24 to 30 fps has occurred.
  + 5:1 duplicate frame cadence on a 30 fps file.
    - Five frames of active motion, followed by one duplicate frame throughout program.
    - This indicates a destructive frame rate conversion from 25 to 30 fps has occurred.
  + 24:1 duplicate frame cadence on a 25 fps file.
    - Twenty-four frames of active motion, followed by one duplicate frame throughout program.
    - This indicates a destructive frame rate conversion from 24 to 25 fps has occurred.

### 3:2 Pulldown / Telecine

* A process in which native 23.98 or 24 fps progressive video is converted to 29.97 fps interlaced video to comply with legacy NTSC broadcast standards. For every three progressive frames in the resulting output, there are two interlaced frames.
* Telecined assets are not accepted for Ingestion by UMG. If no pre-telecine source asset exists for a given video, an inverse telecine process must be performed before Ingestion.

### Combing / Interlacing Artifacts

* If interlaced source videos are incorrectly handled during the post-production process, interlacing artifacts (aka combing artifacts) can become “baked-in” to a progressive image and cannot be removed by a standard deinterlace process.
* Interlacing artifacts appear as horizontal lines around objects in motion.
* These artifacts are most often introduced when an interlaced video is scaled to a different frame size without first being deinterlaced.
* See the Scan Type / Interlacing section on this page for more information about interlaced video.

### Ghosting / Blended Frames

* When information from a set of adjacent frames has been combined and overlaid. Often caused by an improper standards conversion from interlaced to progressive video or a destructive frame rate conversion.

### Slates / Bars & Tone

* A slate is a static screen containing descriptive information (such as title, producer, and running time) that appears at the head of a video program.
* Bars & Tone are material traditionally placed at the head of a video program distributed for television broadcast or prepared for video duplication, including color bars, audio tone, and a countdown clock.

### P2P Formatting

* P2P is an abbreviation for “Program to Program”.
* All videos submitted to UMG shall be formatted with a maximum of two seconds of black and silence before Program Start and after Program End.
* Program Start is defined as the first frame of active video or audio, and Program End as the last frame of active video or audio.
* Over two seconds of leading or trailing black (video at or below 0 IRE) and silence (audio below -90 dB) will result in a QC failure.
* Please note this requirement only applies to a combination of black and silence. There is no specific limit on the duration of black video in conjunction with audible music underneath it.

### Copyright Formatting

* Copyright Notice cards are often included at the end of UMG videos.
* The presence of a Copyright Notice card is not required or enforced by Video Services and is up to the record label’s discretion.
* When Copyright Notice cards are present, they must adhere to the below criteria:
  + Must be centered in the frame, left-to-right.
  + Must not overlap any mattes that are present.
  + Must have a runtime of 3 to 5 seconds.
  + Must not overlap with active video or audio.

### Apple Flags

* Apple Music has strict content guidelines and restrictions for videos delivered to their service. See the below links for more information.
  + UMG Apple Sharepoint – Videos (internal)
  + [Apple Music Style Guide](https://help.apple.com/itc/musicstyleguide/en.lproj/static.html)

# AUDIO ISSUES

### Dual Mono

* Audio is referred to as “Dual Mono” when it has two channels, but both channels are identical to one another. When played back, Dual Mono audio will have no stereophonic image and all audio will sound as if it is coming from the “[phantom center](https://en.wikipedia.org/wiki/Phantom_center)“.
* Modern music is almost always mixed in stereo, so video files containing music must have a “True Stereo” audio track in order to maintain the music’s creative intent.
* Software applications with audio technical metadata readouts (such as QuickTime Player) will typically refer to any audio track with two channels as “Stereo” regardless of whether the two channels are identical, so audio meters in an editing application should be checked before submitting.
* See our Dual Mono Troubleshooting Guide on the [Editor Help](https://lnk.to/umg-video-services-editor-help) page for advice on fixing a Dual Mono issue.

### Inverse Phase

* Occurs when the polarity of different channels in an audio mix are inadvertently opposite of each other. This causes the music to sound, thin, hollow, diffuse, and unnatural.
* True, global inverse phase issues between channels are easy to fix by flipping the polarity of a single channel.

### Channel Imbalance

* When two audio channels have noticeably different volume levels and this causes the entire soundstage to skew unintentionally left or right.

### Lossy Audio Compression

* The reduction of audio quality in order to reduce file size.
* Audio tracks submitted to UMG must not be encoded in a lossy format (MP3, AAC, etc) or be converted to PCM from a lossy source. All submissions must be encoded from the best quality master possible.

# TECHNICAL ATTRIBUTES – VIDEO

### Video Codec

* An algorithm that encodes and decodes digital video data.
* UMG only accepts the Apple ProRes 422 HQ, 4444, and 4444 XQ video codecs. Apple ProRes 422, 422 Proxy, or 422 LT files will be rejected.
* The commonplace, web-quality H.264 video codec will be rejected.

### Frame Size

* The size of of a video frame (width x height) measured in pixels.
* Videos **must** be delivered to UMG with one of the accepted Frame Sizes listed in the [Video Servicing Asset Specs](https://lnk.to/umg-video-services-specs-and-support).
  + 3840×2160 or 1920×1080 are ideal frame sizes for the majority of HD/UHD new release content but more options are listed in the linked specs.
* For videos which feature active picture that is wider or narrower than any accepted frame size dimension, it is **unacceptable** to submit “active picture only” deliveries.
* UMG requires industry standard frame size deliveries because the vast majority of DSPs also require these standard frame sizes.
* If you would like your matted video delivery to appear without mattes at the DSPs that do accept active picture only deliveries (YouTube, Spotify, and Tidal), the label should make sure to set “Crop to Active Picture?” to “Yes” when submitting the VSP job. More info on Crop to Active Picture can be found on the [Crop to Active Picture tab.](https://lnk.to/umg-video-services-crop-to-active-picture)
* If a video is shot or mastered in a resolution that does not match an accepted frame size, the best course of action is to upscale your final edit to the nearest supported frame size.
  + For example, source footage in a 3200×1800 resolution can be upscaled to 3840×2160.

### Display Aspect Ratio

* The proportional relationship between the width and height of a video frame during playback.
* Videos submitted to UMG must contain the correct Display Aspect Ratio (DAR) technical metadata based on [Video Servicing Asset Specs](https://lnk.to/umg-video-services-specs-and-support).
* For SD videos, whether 16:9 or 4:3 is correct will depend on the content present within the video.
* A Display Aspect Ratio Conform video tutorial can be found in the [Editor Help](https://lnk.to/umg-video-services-editor-help) tab of this page.

### Upscaling

* The process of converting natively lower resolution video to a higher resolution.
* Upscaling typically does not increase perceived visual quality and this process may actually reduce quality, depending on the scaling algorithm.
* Videos submitted to UMG must not be up-scaled from SD to HD or from HD to 4K/UHD.

### Frame Rate

* The frequency at which consecutive images are captured or displayed in a video signal. Typically expressed in “fps” – frames per second.
* Videos submitted to UMG must be in their native source frame rate.
  + See the Skipped Frames and Duplicate Frames sections of this page for a detailed description of the issues a video will most likely fail QC for if they are not submitted in their native frame rate.
* For the rare videos which have a native frame rate that is not listed as supported in our [Video Servicing Asset Specs](https://lnk.to/umg-video-services-specs-and-support), we recommend they be submitted in a supported frame rate which is a multiple or factor of the native frame rate.
  + For example, a stop-motion video animated at 15 fps can be submitted as 30 fps.
  + In another example, a video shot at 48 fps can submitted as 24 fps.
* Masters which have been standards-converted (i.e. converted from NTSC 29.97 fps to PAL 25 fps or vice-versa) are NOT acceptable.

### Scan Type / Interlacing

* There are three possible video Scan Types: Progressive, Interlaced Bottom Field First (BFF), and Interlaced Top Field First (TFF).
* Progressive scan type is the modern standard in the streaming era.
  + When images are captured progressively, this results in generally higher video quality.
* Interlacing is a technique for doubling the perceived frame rate of a video display without consuming extra bandwidth. It was developed to enable the transmission of video through legacy broadcast infrastructure with limited bandwidth.
  + Images captured in an interlaced format will be of generally lower quality.
  + Interlaced image capture is often still used for new content that has traditional broadcast transmission in mind as its first or primary distribution method.
* Videos that were originally captured in an Interlaced format should be submitted to UMG as such without any deinterlacing.
* There are two Scan Type readouts on a UMG Video Services Auto-QC report:
  + Scan Type Decoded
    - This value is the Scan Type of the actual video bitstream, as determined to the best our our Auto-QC process’ ability.
  + Scan Type Flag
    - This value is the Scan Type “label” that is listed in the file’s metadata.
* In order to pass UMG’s Auto-QC, the Scan Type Decoded and Scan Type Flag must match AND be listed as supported for a given frame size and frame rate combination in our [Video Servicing Asset Spec](https://lnk.to/umg-video-servicing-asset-spec).
* Note especially that files submitted with a frame rate of 23.976 or 24 fps must only contain Progressive video.

### Color Primaries

* “Color Primaries” is a technical metadata flag or “label” that is stored in a QuickTime file. The term refers to the three “primary” red, green and blue coordinates that define a color space.
* Videos submitted to UMG must contain the correct Color Primaries technical metadata flag based on the frame size and dynamic range combinations listed in our [Video Servicing Asset Spec](https://lnk.to/umg-video-servicing-asset-spec).
* Ensuring the correct Color Primaries flag in your output is a function of timeline and export settings in your editing software.

### HDR vs SDR Video

* SDR refers to “Standard Dynamic Range” video, typically in the BT.709 or BT.601 color spaces with BT.1886 or a specified gamma curve as the transfer function.
* HDR refers to “High Dynamic Range” video, typically in the BT.2020 or P3 color spaces with ST.2084 (PQ) or HLG as the transfer function.
* UMG does not currently support HDR video submissions. All videos must be submitted as SDR (Standard Dynamic Range).
* For a tentative draft of HDR specs UMG plans to support in the future, please reference the “NEXT GENERATION SPECIFICATIONS” section of our [Video Servicing Asset Spec.](https://lnk.to/umg-video-servicing-asset-spec)

### Letterbox

* Black mattes (black bars) at the top and bottom of the frame – these are cropped by some partners.

### Pillarbox

* Black mattes (black bars) on the left and right of the frame – these are cropped by some partners.

### Windowbox

* An image presented inside a black box (black bars on all sides).

# TECHNICAL ATTRIBUTES – AUDIO

### Audio Configuration

* A way of describing how many audio tracks and audio channels are present in a file and what their intended playback layout is.
* There are six possible readouts to UMG Video Service’s Auto-QC “Channels” check. Each represent a different audio configuration:
  + STEREO
    - The only readout that will lead to a PASS in Auto-QC.
    - This result indicates that the submitted asset contains one audio track with two non-identical channels that are properly tagged in file metadata as “Left” and “Right”.
  + DUAL MONO
    - This Auto-QC failure indicates that the submitted asset contains one audio track with two identical channels.
    - See the Dual Mono section on this page for more information
  + TWO DISCRETE TRACKS
    - This Auto-QC failure indicates that the submitted asset contains two discrete Tracks of audio, with 1 Channel on each Track. Per our [Video Servicing Asset Spec](https://lnk.to/umg-video-services-specs-and-support), all audio must be delivered as a 2 Channel Stereo Pair contained on 1 audio Track.
    - NOTE: This failure does not indicate whether or not the underlying audio content is Dual Mono or Stereo. The audio content will need to be reviewed via audio meters as outlined in the Dual Mono section to determine if the audio can be re-configured to meet our specs.
  + MULTICHANNEL
    - This Auto-QC failure indicates that the submitted asset contains more than 2 audio Channels, regardless of the number of audio Tracks. Per our [Video Servicing Asset Spec](https://lnk.to/umg-video-services-specs-and-support), all audio must be delivered as a 2 Channel Stereo Pair contained on 1 audio Track.
    - NOTE: Depending on the content of each audio channel, Video Services may be able to re-configure a file with this failure to meet our specs. The label may reply to a MULTICHANNEL Auto-QC failure notification and ask Video Services to determine if any two audio channels in the file appear to be an intended stereo mix.
  + SINGLE CHANNEL MONO
    - This Auto-QC failure indicates that the submitted asset contains 1 audio Track containing 1 audio Channel. Per our [Video Servicing Asset Spec](https://lnk.to/umg-video-services-specs-and-support), all audio must be delivered as a 2 Channel Stereo Pair contained on 1 Track.
  + UNSUPPORTED CHANNEL TAGGING
    - This Auto-QC failure indicates that the submitted asset contains audio channels that are not properly assigned a speaker position in file metadata. Per our [Video Servicing Asset Spec](https://lnk.to/umg-video-services-specs-and-support), channel 1 must be assigned “Left” and channel 2 must be assigned “Right” in the Stereo Pair.

### Audio Codec

* An algorithm that encodes and decodes digital audio data.
* Audio must be delivered to UMG as uncompressed Linear PCM.
* The common place, web-quality AAC and MP3 audio codecs will be rejected.

### Audio Sample Rate / Bit Depth

* Sample rate is the number of audio samples recorded per unit of time and bit depth measures how precisely the samples were encoded. Together bit depth and sample rate determine audio resolution.
* All audio tracks in video submission to UMG must have a sample rate of 48 kHz and bit depth of 16 or 24.
* Audio tracks in video files with a sample rate of 44.1 kHz will be rejected.
* Audio tracks in video files with a 32-bit “float” depth will be rejected.

# TECHNICAL ATTRIBUTES – DOLBY ATMOS AUDIO

### What is Dolby Atmos?

* Dolby Atmos is a type of spatial/immersive/surround sound audio. While conventional audio formats are channel based, like Stereo with two channels and 5.1 with six channels, Dolby Atmos is object based which means the mix engineer can assign specific 3-D X, Y, and Z coordinates to indicate the position in the room they want an object/instrument/sound to be heard from. Dolby Atmos audio is then delivered and decoded on the consumer’s end in such a way that it will recreate this positioning to the best of the device’s / system’s capabilities.

### ADM BWF (Audio Definition Model Broadcast Wave Format)

* Pronounced as “ADM B-wave”.
* A more sophisticated type of .wav file that, in addition to an uncompressed audio essence, can carry complex and dynamic associated metadata. It is used as a servicing asset for storing and delivering Dolby Atmos audio.

### FFOA (First Frame of Action)

* A manually set timecode metadata value that is meant to indicate the position in an audio file where any pre-roll (reference tones, etc), if any, ends and the main program intended for distribution begins.
* UMG will not accept a Dolby Atmos file with FFOA present.

### Bed Channels

* Bed channels map audio to fixed locations in space that are tightly constrained to speaker positions utilized in traditional channel-based audio formats such as 2.0, 5.1, and 7.1.

### Object Channels

* Object channels map audio to discrete audio elements that can be placed and dynamically panned anywhere in a three-dimensional soundfield. The audio content of an object channel will be heard in as few, or as many, speakers as dictated by the positional and size metadata for that object, as well as the layout and number of speakers in a given playback environment.

### LFE (Low Frequency Effects)

* Information that occupies the lowest section of the audible frequency band can be provided in Dolby Atmos masters on a special type of bed channel referred to as an “LFE” channel. In traditional home theater systems, the audio content of these LFE bed channels will be sent directly to the subwoofer, regardless of any bass management settings.
* As the name implies, these LFE bed channels are intended to only contain low-frequency information, and as such, UMG requires these channels to be band limited using a low pass filter with a cut off frequency of between 100 and 150 Hz during the mix creation process.

### 5.1 Downmix Mode

* A metadata value which dictates the base algorithm that will be used to map audio information into the more limited soundfield provided by 5.1 and 5.1.x speaker configurations.
* UMG requires Dolby Atmos assets be submitted with a 5.1 Downmix Mode of Direct Render.

### Trim Controls

* Trim controls are metadata values that allow mix engineers to fine tune the balance of audio energy across the X, Y, and Z planes in a specific playback speaker configuration. The readout indicated in the VSP AQC report is an aggregate summary of the various trim settings that are set for the 5.1 & 2.0, 5.1.2, 5.1.4, and 7.1 speaker layouts. Possible readouts are Automatic, Manual (All 0), Manual (Custom), or any combination of the three.

### Binaural Metadata

* Metadata values assigned on a per-channel basis that affect the perceived spatial positioning of the audio in each channel when rendered for binaural playback on headphones. This field in the VSP AQC report provides an aggregate summary of each unique binaural setting specified in a file. Possible readouts are Off, Near, Mid, Far, or any combination of the four.
* UMG will not accept Dolby Atmos assets where all binaural metadata values are set to “Off” since this will disable the intended “simulated surround sound” effect when listening to Dolby Atmos audio on headphones.

### True Peak

* A calculated measurement of the highest instantaneous amplitude level within the audio, accounting for potential clipping or distortion when the digital audio signal is converted into analog sound waves. Measured in decibels.
* UMG requires Dolby Atmos assets to have a true peak no higher than -1.0 dBTP.

### Integrated Loudness

* A calculated measurement that indicates the average perceptual volume level of the audio. Measured in LKFS (loudness, k-weighted, relative to full scale).
* UMG requires Dolby Atmos assets to have an integrated loudness no higher than -18.0 LKFS.

# TECHNICAL ATTRIBUTES – FILE

### File Container

* The file format that the video (and audio) is stored in.
* UMG only accepts videos in the QuickTime (.mov) container.
* The commonplace .mp4 container will be rejected.
* Files submitted to UMG must not contain any Tracks other than Video, Audio, or Timecode within the file container.

### File Corruption

* Errors can occur during video file render, export, encode, upload, download, or copy operations that cause the underlying data to become corrupt. This can manifest itself with certain frames of video not playing back correctly or a file not opening at all.
* Videos submitted to UMG must not contain any data corruption, even just a single frame. Please be sure to playback your video file before submission to make sure that all frames and audio play back normally, with no corruption artifacts.

### File Naming

* File names submitted to UMG must only contain standard characters (a-z, A-Z, 0-9, and underscores), and cannot begin with a period or underscore. Do not use special characters such as dashes, spaces, forward slashes, back slashes, accents, &, @, #, etc. Blank spaces are not allowed within the file name or folders in your file path.
* The maximum file name length is 120 characters.

### MD5 Checksum

* An MD5 checksum is a 32-character code that uniquely represents a file’s contents, serving as a distinct digital fingerprint. If two files have the same MD5 checksum, they are identical with extremely high mathematical probability, even if the file names are different or one file is a copy of another. UMG uses MD5 checksum calculation to detect duplicate video files and will reject any new submission with a checksum matching a previous submission.
