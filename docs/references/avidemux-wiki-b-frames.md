> **Snapshot** of <https://www.avidemux.org/admWiki/doku.php?id=using%3Ab-frames>
> Retrieved 2026-11-17; main content converted to Markdown.
> Copyright belongs to the original authors and publisher. This copy is kept
> only as a reference backup and is **not** covered by this repository's MIT license.

---

### Table of Contents

- [B-frames](#b-frames)
  - [The problem](#the_problem)
  - [The MPEG way (the right way)](#the_mpeg_way_the_right_way)
  - [DivX (and Xvid) way](#divx_and_xvid_way)
  - [The problem, part 2](#the_problem_part_2)
  - [The solution](#the_solution)
  - [See also](#see_also)

# B-frames

This chapter is an introduction to B-frame handling. If you are familiar with the concepts you can safely skip it.

Video frames can be divided among 3 types:

1.  **[I-Frame](https://www.avidemux.org/admWiki/doku.php?id=using:i-frames "using:i-frames"):** Intra frame, also called keyframe. They have no reference frame and can be decoded on their own. They can be thought of as a JPEG image.
2.  **P-Frame:** Predicted frame. They are deduced from the previous frame (I or P) and cannot be built if the decoder has not decoded the previous frames.
3.  **B-Frame:** They are decoded from the previous and next I-P frames.

B-frames are interesting for two facts. First, they have a slightly better prediction. And second and more important, they do not impact the quality of following frames, so they can be encoded with lower quality without degrading the whole sequence.

Since B-frames depend on both past and future picture, the decoder has to be fed with future I-P frames before being able to decode them. There comes the PTS/DTS logic.

Presentation Time Stamp is the presentation time, it could be thought of as display frame number. It is the order you will see the decoded frames. The DTS is the Decoder Time Stamp, i.e. the decoding frame number.

Assume if you have a short video like this:

I-0 B-1 B-2 P-3

B-1 and B-2 depends on both I-0 and P-3. The corresponding DTS order would be:

I-0 P-3 B-1 B-2

To keep things simple, the file is encoded with DTS order.

## The problem

The problem is that to keep showing the video in the right order, the codec has to do things to pop out the frames in the correct order and sequentially (i.e. one frame in, one frame out).

## The MPEG way (the right way)

The usual way to do this is that the codec delays decoding for 3 frames. Like that, it always has the two reference frames to decode frames.

In 0 3 1 2 . .

Out - - - 0 1 2 3 . .

This is perfectly legit for a player as the delay is known when creating the file and thus compensated (i.e. the audio stays in sync).

## DivX (and Xvid) way

To be able to use the PTS/DTS with application not used to deal with such streams, DivX codec (and Xvid when in compatibility mode) uses a different trick.

They use a variant of PB frames and pack several frames in one. So the application thinks it is only one frame and the codec hides all this internally.

If we take the previous example, DivX would create a file like this, the () means one frame in the file:

In (0 3 1 2) - - - . . .

Out 0 1 2 3 ....

Null frames are inserted where frames were packed. The codec knows that if it receives null frame after a pack of frames, it should pop out frames from the pack.

From a coder point of view, it is interesting as it does not introduce a delay between in and out, and AVI files do not have the PTS/DTS field to hint the decoder/player.

## The problem, part 2

This behaviour collides with Avidemux aim: to provide frame accuracy.

In the MPEG way, there is a delay between what's fed to the codec and what's out. It is not acceptable as you would never know which actual frame your are looking at.

The DivX/Xvid way is tricky because frames 2, 3, 4 are seen a null frame and we cannot cut such a stream with frame accuracy.

## The solution

Avidemux handles the PTS/DTS logic itself and forces the codec to popout the frames immediately. The editor part of Avidemux knows the DTS/PTS order of the frames and feeds the decoder correctly. You have frame accuracy and B-frames.

The problem is that DivX and Xvid hide the frame type by packing them, so the editor cannot deal with that for now.

From Avidemux 2.0.24 and afterward, the packed bitstream is automatically unpacked upon loading. But only for AVI/OpenDML. If the source is an OGM file, first save it as an AVI and reload.

## See also

[I-frames](https://www.avidemux.org/admWiki/doku.php?id=using:i-frames "using:i-frames") – a discussion of I-frames and their role in digital video.
