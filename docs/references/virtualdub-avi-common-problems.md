> **Snapshot** of <https://www.virtualdub.org/blog2/entry_025.html>
> Retrieved 2026-11-17; main content converted to Markdown.
> Copyright belongs to the original authors and publisher. This copy is kept
> only as a reference backup and is **not** covered by this repository's MIT license.

---

## AVI files and common problems

I thought today I'd actually post some advice that was relevant to desktop video. But first, some commenters to my "I hate Windows" story asked for me to post my port of the Samba 4.x "editreg" tool, so here it is: [editreg_src_win32.zip](https://www.virtualdub.org/misc/editreg_src_win32.zip). I've only included the source code because the port is VERY rough and doesn't do full argument passing, and realistically you have to hack it to use it; also, it doesn't actually allow you to edit the registry, only dump its contents. Still, it works. At the time of this writing, you can [get the original source code from the official Samba CVS web browser.](http://cvs.samba.org/cgi-bin/cvsweb/samba4/source/utils/editreg.c?rev=1.1.1.1&content-type=text/x-cvsweb-markup)

Now, about AVI files....

AVI stands for "Audio/Video Interleaved" and holds both audio and video together in a playable format. The basic structure of an AVI file comes from a general file structure called the Resource Interchange File Format (RIFF), which is in turn based off of the Electronic Arts IFF specification that had its roots on the Amiga. RIFF files consist of a series of chunks, each prefixed by a four-character chunk ID and a four-byte length. These chunks may in turn be nested to form a structured file. This chunk structure is nice because any unrecognized chunk can simply be skipped, allowing a file format to be extended without breaking backwards compatibility. The Portable Network Graphics (PNG) standard has an even more evolved tagging system that also encodes "should-copy" and "must-understand" bits so that old programs even have an idea of what they should do with an unrecognized chunk.

Here's what the structure of a sample AVI file looks like:

> RIFF 'AVI '            Audio/Video Interleaved file\
>     LIST 'hdrl'        Header LIST\
>         'avih'         Main AVI header\
>         LIST 'strl'    Video stream LIST\
>             'strh'     Video stream header\
>             'strf'     Video format\
>         LIST 'strl'    Audio stream LIST\
>             'strh'     Audio stream header\
>             'strf'     Audio format\
>     LIST 'movi'        Main data LIST\
>         '01wb'         Audio data\
>         '00dc'         Video frame\
>         ...\
>     'idx1'             Index

Some notes:

- AVI files are composed of general streams; this one consists of one video and one audio stream. You can actually store text streams and even multiple video and audio streams in a single AVI file. (VirtualDub's AVI parser supports multi-video and multi-audio stream AVIs; it's the UI and output modules that don't.)
- Audio and video data is stored in the 'movi' LIST chunk in chronological order. (This isn't actually true of MUSTUSEINDEX is set in the stream header, but I've never seen this used.) Combined with the header being at the front this means that AVI files *can* actually be played in streaming mode across a network. They won't play that well given that AVI doesn't interleave data finely enough, doesn't have scrambling mechanisms for enhanced audio error masking and doesn't have a rigid enough structure for good error recovery, but you can do it.
- Audio and video data are broken into blocks and mixed together; each video frame has its own chunk, but audio data is organized in small packets. This is the "interleaved" part of the file. The reason for it is so that a player can read the AVI file sequentially and pick up the audio and video it needs without seeking all over the place. This isn't too important for playback from a hard disk, and modern players are very good at handling non-interleaved or badly interleaved files, but proper interleaving is critical for proper playback in embedded devices and CD-ROM playback. Note that despite common belief, the interleaving of audio and video chunks has **nothing** to do with the timing of the streams, and thus no effect on sync.
- The 'idx1' index lists all of the chunks in the main 'movi' LIST, which in turn holds all audio and video frames. Without this chunk, the only way to find frame 400 would be to run forward through all the chunks in the 'movi' LIST and count them until you hit the 401st video frame. That would be very sloooooooowwwww. The index chunk also says whether video frames are key frames. In fact, it is the ONLY chunk in this file that does. More on that later.
- Note that the header and index are at the beginning and end of the file. Lose the index at the end, and your AVI file will become unseekable or even refuse to play in some players. Lose the headers at the start, and your file is unusable.

If you load an AVI file into VirtualDub's hex editor, the Show RIFF Tree (Ctrl+R) command will display the RIFF tree for the file.

Overall, AVI isn't a very complex file format, and in particular it's very easy to write -- so it's not surprising that a lot of programs support it. Often AVI gets a lot of flak for not supporting a lot of newer video storage functionality, such as subtitles, timestamps, and more complex frame dependencies. Keep in mind, however, complexity has a cost, and not every file format has to, or should, support everything. The MPEG-1 file format is improved in a number of ways but is significantly more complex to support with its precise per-byte timing and bandwidth constraints and lack of a central index. In general, the more features that are put into a file format, the nicer it becomes to write and the harder it is to read... and the harder a file format is to read, the less universally it tends to be supported properly. If a file format is way too complex but still becomes popular, generally the number of incomplete and broken clients using it grows and the usable part of the file spec contracts to the part that people actually need. So file format designers beware!

Now, as for AVI files, there are a lot of mistakes that can be made in creating or transferring AVI files, and VirtualDub tries to be tolerant. Here are some of the problems I've seen:

- **Misaligned or broken data chunks**: Data chunks in the 'movi' LIST are supposed to be properly tagged and aligned to two-byte boundaries like any chunk, but since their data is pointed to by the index, it is possible to totally scramble the headers in that chunk and still have a playable file.
- **Bad RIFF size**: Some AVI files don't have the correct size in the top-level RIFF chunk.
- **Bad header sizes**: When programs crash, they sometimes leave an AVI file that has mostly valid headers and data, except that the sizes on some of the LIST chunks are incorrect. For this reason VirtualDub doesn't validate LIST chunk sizes. This means that the hierarchical structure of an AVI file is lost, but fortunately the order of the LIST chunks is sufficient to decipher the file.
- **Old header fields**: Some of the header fields in AVI are no longer supported and must be ignored, despite their original meaning. For instance, dwStreamSize=0 is supposed to indicate a stream that has one chunk per sample, which permits VBR -- but in fact it is ignored for audio streams. More on this in a later article.
- **Wild headers:** A video game emulator was writing out video stream formats that were 150K-600K in size instead of the usual ~40 bytes, due to mixing up header size and frame sizes... whoops. It's fixed now (thanks, Pete!), but I had to fix VirtualDub too because it was crashing trying to Direct-stream those files. (VirtualDub was using a fixed 64K buffer to hold the output AVI header; it's now dynamic.)
- **Junk at the end of the file**: Some AVI files have garbage after the 'idx1' chunk; for this reason VirtualDub stops parsing an AVI file the minute it has seen headers, the 'movi' LIST chunk, and an index.
- **Absolute vs. relative index**: The 'idx1' chunk is supposed to point to data chunks using *relative offsets* within the LIST 'movi' chunk; however, some AVI files have *absolute file offsets* here instead. VirtualDub's parser, like that of many players, will detect and accept either. Actually, VirtualDub used to write absolute file offsets too, but I fixed that a long time ago.
- **Missing or truncated index**: This one is very common as it happens with any incomplete file. The problem here is that the offsets and sizes of the index can be recovered by scanning the whole file, which VirtualDub does when it detects a missing index, but the key frame flags that are required for seeking and decoding can't. VirtualDub recovers these by decoding the frames both in forward and reverse order and watching for artifacts; this drives some codecs nuts -- it's not exactly correct usage -- but usually it recovers the key frame information safely. If this recovery process is *not* done, then VirtualDub has to assume that only the first frame is a key frame, which makes seeking very painful -- potentially requiring every frame in the video stream to be decoded to retrieve the last frame.
- **Damaged chunks in 'movi' LIST chunk**: This one is fairly common for files that have been transferred over \*ahem\* distributed networks, due to small instances of corruption here and there, or worse, attempting to play an AVI file for which not all segments have been received. The index mostly allows such files to be played, but it still causes problems in a couple of cases. One problem is that it confounds a player that attempts to stream through the 'movi' LIST rather than using the index; I think the OS/2 player does this. A more serious problem is that it makes recovery more difficult if the index is also missing. When VirtualDub finds a problem scanning through the file it switches to "aggressive mode" and begins brute-force searching through the remainder of the file, looking for consistent chunk headers in order to detect the good parts of the streams. Unfortunately, while this recovers the valid data, it can't determine what times correspond to that data due to the lack of timestamps, leading to a loss of sync. There are probably ways I can determine approximate timings heuristically using regression algorithms similar to what I use in the capture module, based on the chunk interleave, but VirtualDub doesn't do this yet.

In case it's not clear yet, VirtualDub shouldn't be used to determine that an AVI file is valid, because in the interests of compatibility and recovery it allows a number of violations. It also doesn't support a few of the lesser-used parts of the file format, most notably streams with a non-zero start time and in-stream palette changes. However, I've tried to make the parser accept most damaged AVI files and flag warnings for files that it should but can't support, to improve the usefulness of the program.

By the way... what are OpenDML AVI files?

Earlier, I said that chunks are tagged with a four-byte length. This limits the size of any chunk to ~4GB (4,294,967,295 bytes), and in fact, the practical limit is a lot lower due to compatibility concerns, around 1-2GB. The index also has the same limitation and this limits the size of standard AVI files to 2GB. A group called the *OpenDML AVI M-JPEG File Format Subcommittee* devised a semi-backwards-compatible way to extend this limit, by appending additional structure to a standard AVI file. The result is that legacy applications *still* can't read beyond 2GB, but the rest of the data is appended after the standard AVI and pointed to by a new type of two-level index. VirtualDub calls this the **AVI2** format; by default it writes standard AVI files until it hits 2GB, at which point it switches to the new format.

Finally, there is one major feature of common AVI files that I haven't mentioned yet: VBR audio. In particular, I mean VBR MP3 audio. For various reasons VBR audio both is and isn't supported in the file format, and the way that it is implemented in practice is also both supported and not supported. In a future post I'll go into the technical details of how VBR MP3 audio is popularly implemented and the reasons for VirtualDub's behavior with it. I already wrote on this a long time ago, but it's a common enough question that the answer bears repeating.

35 comments \| Nov 11, 2004 at 00:21 \| default

# Comments

This blog was originally open for comments when this entry was first posted, but was later closed and then removed due to spam and after a migration away from the original blog software. Unfortunately, it would have been a lot of work to reformat the comments to republish them. The author thanks everyone who posted comments and added to the discussion.
