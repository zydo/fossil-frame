> **Snapshot** of <https://www.forasoft.com/learn/audio-for-video/articles-audio/pcr-mpeg-ts-program-clock-reference>
> Retrieved 2026-11-17; main content converted to Markdown.
> Copyright belongs to the original authors and publisher. This copy is kept
> only as a reference backup and is **not** covered by this repository's MIT license.

---

# PCR in MPEG-TS: Program Clock Reference, PID and Jitter

By

Nikolay Sapunov

·

Published

June 7, 2026

·

21

min read

TL;DR

A transport stream carries thousands of audio and video frames per second, but none of their timestamps mean anything until the player knows what clock they were measured against. The program clock reference, called PCR, is that clock: a periodic snapshot of the encoder's 27 MHz master clock, inserted into the stream so the decoder can rebuild the same clock locally and replay every frame at the right instant. It ticks at 27 million times per second, is stored as a 42-bit number split into a 90 kHz base and a finer 27 MHz remainder, must arrive at least every 100 milliseconds with an accuracy of ±500 nanoseconds, and a decoder uses a feedback loop to lock its own clock to it. Get the PCR right and a broadcast plays smoothly for days; get it jittery or late and you see stutter, buffer overflows, and audio that slowly drifts away from the picture.

Updated October 2026: corrected the DVB PCR interval (ETSI TR 101 290 tests 100 ms, the old 40 ms limit was dropped in 2005), added the TR 101 290 PCR error codes and the PCR settings in FFmpeg 9.0 and GStreamer 1.28, moved references to ISO/IEC 13818-1:2025 and ITU-T H.222.0 (04/2025).

## Why this matters

**The program clock reference (PCR) is a 42-bit sample of the encoder's 27 MHz system clock, written into the adaptation field of MPEG-TS packets on the PID that the program map table names as PCR_PID, at least every 100 ms.** The decoder uses those samples to rebuild the encoder's clock, and only then can it read the PTS and DTS of every frame. In one line: the PCR is the clock the decoder rebuilds so every frame plays on time. The rest of this article is how the number is built, how often it must arrive, how a decoder locks to it, and how to read the PCR lines of a stream analyzer report.

If you build anything that ingests, processes, or plays a transport stream — an OTT backend, an IPTV set-top app, a broadcast contribution link, an ad-insertion server — the PCR is the single value that decides whether playback is smooth or broken. A product manager needs to know the PCR exists so they understand why "just remux it" can silently destroy timing, and why broadcast engineers obsess over a number most file formats never expose. An engineer needs to know exactly how the PCR is encoded, how often it must appear, and how tightly it must hold, so they can read a stream analyzer report and tell a real fault from noise. This article gives both readers one model: the PCR is the heartbeat the whole broadcast clock is built on, and every PTS and DTS is meaningless without it.

------------------------------------------------------------------------

## The problem PCR solves: timestamps need a clock to be read against

Start with a fact that surprises people who learned timing on MP4 files. In a transport stream, the presentation timestamp (the PTS, the number that says "show this frame now") is not enough on its own. A PTS of 90,000 means "ninety thousand ticks after the clock's zero point" — but the decoder has no clock yet. It just received a packet over a satellite link or a cable feed; it has no idea what "now" is on the sender's timeline. A timestamp is a reading on a clock, and the decoder is missing the clock.

This is the gap the program clock reference fills. The encoder runs a master clock. Every so often it writes down the current reading of that clock and inserts it into the stream as a PCR. The decoder reads those readings, rebuilds a copy of the encoder's clock locally, and only then can it interpret the PTS and DTS values on every frame. The PCR is the shared reference; the PTS and DTS are positions measured against it. We covered how PTS and DTS work in [PTS, DTS, and the Elementary Stream Timestamp](https://www.forasoft.com/learn/audio-for-video/articles-audio/pts-dts-elementary-stream-timestamps) — this article is the clock those two timestamps are read against.

Think of it like a clock on a factory wall. The workers (the PTS and DTS values) all say things like "ship this order at 3:00" and "start that batch at 3:05." Those instructions are useless to a new worker who has no watch. The wall clock is the PCR: the shared reference everyone sets their own watch to. Without it, every "3:00" is just a number with no meaning.

 *Figure 1. Why the PCR exists. PTS and DTS values are positions on a clock; the PCR is the clock itself, sent periodically so the decoder can rebuild it and read every other timestamp.*

------------------------------------------------------------------------

## The 27 MHz master clock

Every program in a transport stream is timed by a master clock, and the standard fixes its rate. The clock ticks **27,000,000 times per second** — 27 MHz. Every timing value in the stream descends from this one clock. The familiar 90 kHz clock that PTS and DTS use is not a separate clock at all; it is the 27 MHz master divided by exactly 300:

    90 kHz clock = 27,000,000 ÷ 300 = 90,000 ticks per second

So why have a 27 MHz clock at all, if PTS and DTS only need 90 kHz? Two reasons. First, the finer resolution lets the decoder lock its clock far more precisely than 90 kHz steps would allow — one 27 MHz tick is about 37 nanoseconds, against 11 microseconds for a 90 kHz tick. Second, 27 MHz was already the clock of digital studio video: it is twice the 13.5 MHz luma sampling rate of ITU-R BT.601, which was itself chosen as a common multiple of the 525-line and 625-line scanning frequencies. When MPEG-2 was designed in the early 1990s, reusing that clock let one decoder design serve both television systems. The number is a bridge between the compressed stream and the studio video world it was born into.

The clock is not allowed to wander freely. The MPEG-2 systems standard requires the encoder's 27 MHz clock to stay within a narrow band: between 27,000,000 − 810 Hz and 27,000,000 + 810 Hz. That is **±30 parts per million** (810 ÷ 27,000,000 = 0.00003). A clock allowed to drift wider than this would push the decoder's recovered clock out of range and cause the decoder's buffers to slowly fill or empty until playback breaks. Thirty parts per million is the budget; everything in the PCR machinery exists to keep the decoder inside it.

------------------------------------------------------------------------

## How the PCR number is built

The PCR is a single instant of the 27 MHz clock, but it is not stored as one plain number. It is split into two parts so that the coarse part lines up exactly with the 90 kHz PTS/DTS clock and the fine part captures the remainder. The full value is **42 data bits**, carried inside a 48-bit field (the extra 6 bits are reserved padding).

The two parts are defined by simple arithmetic on the master clock reading. Let the master clock have counted `t` ticks at 27 MHz. Then:

    PCR_base = (t ÷ 300) rounded down, then taken modulo 2^33
    PCR_ext  = t modulo 300
    PCR      = PCR_base × 300 + PCR_ext

The **base** is the reading expressed in 90 kHz units — it is the same clock domain the PTS and DTS live in, which is exactly why they can be compared directly. It is 33 bits wide, the same as a PTS. The **extension** is the leftover count of 27 MHz ticks since the last 90 kHz step, a number from 0 to 299, stored in 9 bits (9 bits hold 0–511, comfortably covering 0–299). Put the two together and you recover the full 27 MHz reading to single-tick precision.

A worked example makes the split concrete. Suppose the encoder's master clock has ticked exactly 27,000,123 times — just past the one-second mark:

    t        = 27,000,123 ticks at 27 MHz

    PCR_base = (27,000,123 ÷ 300) rounded down
             = 90,000 (remainder 123)        → the 90 kHz reading: 1.000000 s

    PCR_ext  = 27,000,123 modulo 300
             = 123                            → 123 extra 27 MHz ticks

    reassembled PCR = 90,000 × 300 + 123 = 27,000,123   ✓ exact

The base says "one second," matching the 90 kHz PTS clock perfectly. The extension adds the 123 fine ticks the base could not express. The decoder needs both halves to lock its clock tightly; a base-only reading would be accurate to only 11 microseconds, and that is not enough to keep a broadcast steady over hours.

 *Figure 2. The PCR split into a 33-bit 90 kHz base and a 9-bit 27 MHz extension. The base aligns with PTS/DTS; the extension supplies the fine resolution the decoder needs to lock its clock.*

------------------------------------------------------------------------

## Where the PCR rides, and how often

The PCR does not get its own packet type. It travels in the **adaptation field** — an optional extra header that a transport stream packet can carry ahead of its payload. A transport stream is a chain of fixed-size **188-byte packets**, each tagged with a packet identifier (a PID) that says which stream it belongs to. One PID per program is nominated as the PCR-carrier: the 13-bit `PCR_PID` field of the program map table (PMT) names it. Most encoders put the PCR on the video PID; some put it on a separate PID that carries nothing but PCRs. The value `0x1FFF` means no PCR is associated with the program, which ISO/IEC 13818-1 allows only for private streams with no clock to recover. Whenever a packet on the PCR PID carries a clock reading, it sets the PCR_flag in its adaptation field and writes the 42-bit PCR there.

How often must this happen? **Successive PCRs for a program must arrive no more than 100 milliseconds apart** (ISO/IEC 13818-1). The DVB measurement guidelines test exactly that limit: in ETSI TR 101 290 V1.4.1 (2020) a `PCR_repetition_error` fires when two consecutive PCRs are more than 100 ms apart. Many older explainers, and plenty of analyzer presets, still quote 40 ms for DVB. That number was real once, but the 40 ms precondition was removed from the DVB guidelines (ETSI TS 101 154) in 2005, and TR 101 290 now notes it only as the former recommendation. In practice, encoders insert PCRs far more often than 100 ms: FFmpeg defaults to 20 ms for constant-bitrate output and GStreamer to 40 ms, and many operators keep 40 ms as a house limit. The reason is simple. The decoder's clock-recovery loop corrects itself only when a fresh PCR arrives, so more frequent PCRs give a tighter recovered clock. Too few and the decoder's clock drifts between readings; too many and you spend bandwidth on timing overhead. Twenty to forty milliseconds is where most real streams sit, with 100 ms as the hard ceiling.

This is the first common mistake worth naming. When a tool re-multiplexes or re-times a transport stream — splicing in an advertisement, changing the bitrate, repackaging for a different distribution path — it must **re-stamp the PCRs to match the new packet positions.** The PCR's whole job is to say "this is the clock reading at the moment this packet leaves," so if the packet's position in time changes and the PCR does not, the value is now a lie. A surprising share of broadcast playout faults trace to a remux step that moved packets around but copied the old PCR values verbatim.

------------------------------------------------------------------------

## How the decoder rebuilds the clock

The decoder arrives with a free-running 27 MHz oscillator that is close to 27 MHz but not exact — every crystal is a little fast or a little slow. Its task is to nudge that oscillator until it matches the encoder's clock as closely as the incoming PCRs reveal it. The mechanism is a **phase-locked loop**, a PLL: a feedback circuit that compares two clocks and steers one toward the other.

The loop runs a simple cycle. When a PCR arrives, the decoder reads the encoder's clock value from it and compares it to its own local clock reading at that instant. If the local clock is ahead, the oscillator is running fast and the loop slows it slightly; if behind, the loop speeds it up. Each PCR is one correction. Over many PCRs the local clock converges on the encoder's clock and then tracks it, staying locked as long as fresh PCRs keep arriving. This recovered clock is the decoder's **system time clock**, the STC. Every PTS and DTS in the stream is read against this recovered STC: when the STC reaches a frame's PTS, that frame is presented.

The chain is worth stating plainly because it is the heart of the whole system. The encoder's master clock generates the PCRs. The PCRs let the decoder rebuild the same clock as its STC. The STC is what the PTS and DTS are compared against. Break the first link — jittery, late, or wrong PCRs — and every timestamp downstream becomes unreliable, even if the PTS and DTS values themselves are perfect.

 *Figure 3. The decoder's phase-locked loop. Each PCR is one comparison; the loop steers the local 27 MHz oscillator until the recovered system time clock tracks the encoder, and every PTS/DTS is then read against that recovered clock.*

------------------------------------------------------------------------

## PCR jitter, drift, and offset: when the heartbeat goes wrong

Because the decoder trusts the PCR completely, the quality of the PCR signal decides the quality of the recovered clock. Broadcast engineers measure three distinct ways a PCR stream can misbehave. The limits come from ISO/IEC 13818-1, and the DVB measurement guidelines (ETSI TR 101 290) define how each one is measured.

**PCR accuracy, usually called jitter,** is how far each individual PCR reading lands from where a perfectly steady clock would have placed it. The MPEG-2 standard expects the inserted PCR to be accurate to within **±500 nanoseconds**. Jitter beyond that confuses the PLL: each correction the loop makes is based on a value that is slightly off, so the recovered clock wobbles instead of holding steady. At the multiplexer output the usual culprit is a remux or software muxer that writes PCR values that do not match the packets' real byte positions. Further downstream, switches and routers bunch up and stretch out packets that should arrive evenly spaced, so each PCR arrives at a different real-world moment than its value claims; TR 101 290 measures that network part separately as PCR overall jitter (PCR_OJ).

**PCR drift rate** is how fast the encoder's clock frequency itself is changing. A clock that slowly speeds up or slows down forces the decoder's PLL to chase a moving target. ISO/IEC 13818-1 caps the rate of frequency change at **75 millihertz per second** (about 2.77 parts per billion per second), and TR 101 290 measures it as the PCR drift rate (PCR_DR) — a deliberately tiny number, because a clock that drifts faster than this will eventually push the decoder out of its ±30 ppm tolerance band and break playback.

**PCR frequency offset** is a fixed error: the encoder's clock simply running at, say, 27,000,400 Hz instead of 27,000,000. As long as the offset stays inside the ±810 Hz (±30 ppm) window the standard allows, the decoder can lock to it. Push past that window and the decoder cannot follow, and its buffers begin the slow slide toward overflow or underflow.

The visible symptoms follow directly from the cause. A buffer that slowly fills because the decoder clock runs slower than the stream means the decoder eventually has to drop a frame to catch up — a periodic hitch. A buffer that slowly empties means the decoder runs dry and freezes for a moment. The most insidious fault sits right next to the PCR: audio that drifts a few milliseconds away from the picture over many minutes, never enough to alarm in a quick check, plainly wrong by the end of a long program. Because audio and video PTS are read against the same recovered clock, a PCR offset on its own moves both together. Steady lip-sync drift means some clock in the chain is not locked to the PCR: at the encoder, an audio sample clock not derived from the 27 MHz system clock; at the decoder, an audio output clock that is not slaved to the recovered STC. When a viewer reports lip-sync that "gets worse the longer I watch," that clock chain, the PCR and every clock that should follow it, is the first place an experienced engineer looks. For what counts as perceptible drift, see [What "In Sync" Means: ITU-R BT.1359, Lip-Sync Windows, Perceptibility](https://www.forasoft.com/learn/audio-for-video/articles-audio/lip-sync-itu-r-bt-1359-tolerance-windows).

| Defect | What it is | Standard limit | Typical symptom |
|:---|:---|:---|:---|
| **PCR accuracy / jitter** | Each PCR lands off its ideal time | ±500 ns (MPEG-2) | Wobbly clock; intermittent micro-stutter |
| **PCR drift rate** | Encoder clock frequency changing over time | ≤ 75 mHz/s (ISO/IEC 13818-1; PCR_DR in TR 101 290) | PLL keeps chasing; buffer creep, and slow lip-sync drift where the audio clock is not slaved to the STC |
| **PCR frequency offset** | Encoder clock at a fixed wrong rate | Within ±810 Hz / ±30 ppm | Buffer slowly fills or empties; periodic frame drop or freeze |
| **PCR interval too long** | PCRs arrive too far apart | ≤ 100 ms (MPEG-2 and TR 101 290); 20–40 ms in practice | Loose, drifting recovered clock between readings |

*Table 1. The four ways a PCR stream goes wrong, the limit each one is held to, and what a viewer sees. A stream analyzer reports all four; the limits come from ISO/IEC 13818-1 and ETSI TR 101 290.*

------------------------------------------------------------------------

## PCR errors in a TR 101 290 report: what each one means

**A TR 101 290 analyzer reports PCR problems as three Priority 2 errors: 2.3a PCR_repetition_error (two PCRs more than 100 ms apart), 2.3b PCR_discontinuity_indicator_error (the PCR jumps without the discontinuity flag set) and 2.4 PCR_accuracy_error (a PCR off by more than ±500 ns).** Older analyzers show a single 2.3 PCR_error, which is simply 2.3a or 2.3b; TR 101 290 V1.4.1 recommends the split pair for new tools. Priority 2 means "recommended for continuous or periodic monitoring": the stream still decodes, but the clock under it is suspect.

| Error (TR 101 290) | Fires when | Usual cause | First thing to check |
|:---|:---|:---|:---|
| **2.3a PCR_repetition_error** | Two consecutive PCRs on the PCR PID are more than 100 ms apart | Muxer set to a long PCR interval; VBR video with sparse packets on the PCR PID; packets dropped on the network | The muxer's PCR interval setting and whether the PCR rides on a PID that is silent for long stretches |
| **2.3b PCR_discontinuity_indicator_error** | The difference between consecutive PCRs is outside 0–100 ms and the `discontinuity_indicator` is not set | A splice, source switch or encoder restart that resets the clock without signalling it | The splicer or playout switch: it must set the discontinuity flag on the first packet of the new timebase |
| **2.4 PCR_accuracy_error** | A PCR value is not within ±500 ns of where it should be for its byte position | Remux without re-stamping; a software muxer stamping PCRs from a jittery system clock; VBR output with no null stuffing | Whether the last remux stage re-stamps PCRs, and whether the output is true CBR |

*Table 2. The PCR errors of ETSI TR 101 290 V1.4.1 (2020), current as of October 2026. Thresholds from Table 5.0b of the report; the ±500 ns accuracy limit is from ISO/IEC 13818-1, clause 2.4.2.2.*

One measurement trap is worth knowing. PCR accuracy is defined at the multiplexer output, but most analyzers sit after a network. If they measure jitter on arrival (TR 101 290 separates PCR overall jitter, PCR_OJ, from pure accuracy), an IP network that bunches packets will show PCR "errors" that the encoder never made. When accuracy errors appear only on the far side of a network, a de-jittering buffer before the decoder is the fix, not a new encoder.

------------------------------------------------------------------------

## What an MPEG-TS encoder or muxer does with the PCR

**An MPEG-TS encoder (strictly, its multiplexer) generates the PCR: it samples its 27 MHz clock as each PCR packet leaves, writes the value into the adaptation field, and controls how often that happens and whether the output is constant bitrate.** Those two settings, the PCR interval and the mux rate, decide most of the PCR quality a downstream analyzer will see. A hardware encoder hides them behind a menu; software muxers expose them directly.

    # FFmpeg 9.0 (August 2026): CBR transport stream, PCR every 20 ms
    ffmpeg -re -i input.mp4 \
      -c:v libx264 -b:v 4500k -minrate 4500k -maxrate 4500k -bufsize 4500k -x264-params nal-hrd=cbr \
      -c:a aac -b:a 128k \
      -f mpegts -muxrate 5000k -pcr_period 20 \
      "udp://239.0.0.1:1234?pkt_size=1316"

    # GStreamer 1.28: mpegtsmux pcr-interval is in 90 kHz ticks (1800 = 20 ms; default 3600 = 40 ms)
    ... ! mpegtsmux pcr-interval=1800 bitrate=5000000 ! udpsink host=239.0.0.1 port=1234

In FFmpeg's mpegts muxer, `-pcr_period` is in milliseconds; left at its default, FFmpeg picks 20 ms for CBR streams and, for VBR streams, the largest multiple of the frame duration under 100 ms. `-muxrate` turns on constant-bitrate output by padding with null packets, which keeps PCR spacing even. In GStreamer, `mpegtsmux` counts `pcr-interval` in 90 kHz ticks with a default of 3600 (40 ms), and a non-zero `bitrate` pads to CBR the same way. Whichever tool you use, the practical checks when you pick or configure an MPEG-TS encoder are the same:

- **Configurable PCR interval**, with 20–40 ms available and 100 ms never exceeded.
- **True CBR output with null stuffing** for broadcast, IPTV multicast and any feed that goes through a re-multiplexer.
- **A stated PCR accuracy** inside ±500 ns at the output, and PCRs re-stamped after any internal remux.
- **A clean TR 101 290 Priority 1 and 2 report** on your own analyzer, measured right at the encoder output before you blame the network.

------------------------------------------------------------------------

## Why MPEG-TS — and therefore PCR — is still everywhere

It is fair to ask why a clock model designed in the early 1990s for satellite and cable still runs so much of the video world in 2026, when newer container and transport designs exist. The answer is that the transport stream was built for hostile, one-way channels, and that design still has no equal where the link is unreliable and there is no back-channel to ask for a retransmission.

A transport stream is a chain of small, fixed **188-byte packets**, each independently decodable and each able to carry its own timing. If a satellite hiccup or a noisy cable corrupts one packet, the rest of the stream is unaffected — the decoder resynchronizes on the next packet's sync byte and carries on. Forward error correction is layered on top (DVB adds 16 bytes of correction per packet, ATSC adds 20), so many corrupted packets are repaired before the decoder ever sees them. This resilience is exactly what broadcast and professional **contribution** links — the feeds that carry live content from a venue back to a studio — need, and it is why MPEG-TS, with the PCR at its core, remains the default there. File formats like MP4 optimize for storage and random access on reliable media; the transport stream optimizes for surviving a bad channel in real time. Different jobs, different designs. The container details across both worlds are covered in [Audio in Containers: How MP4, MKV, fMP4, MPEG-TS Carry Audio](https://www.forasoft.com/learn/audio-for-video/articles-audio/audio-in-containers-mp4-mkv-fmp4-mpegts).

There is one more reason the PCR endures: HLS, the streaming protocol that delivers a large share of internet video, began by chopping media into short MPEG-TS segments, each one a miniature transport stream with its own PCR. That path is still open but narrowing. Apple's HLS authoring specification (last revised June 2025) still allows H.264 in either MPEG-TS or fragmented MP4, but requires fMP4 for HEVC and AV1, and for transport-stream segments it requires that continuity counters and timestamps run sequentially across segments. A large installed base of TS-segment HLS is still in service, and every one of those segments carries the same 27 MHz clock model this article describes; where it breaks in practice is covered in [Lip-Sync in HLS and DASH: Where It Usually Goes Wrong](https://www.forasoft.com/learn/audio-for-video/articles-audio/lip-sync-in-hls-dash-where-it-goes-wrong). Inside the studio the picture is different: uncompressed IP production on SMPTE ST 2110 does not use the PCR at all and times every essence from PTP instead, which is why a contribution chain often converts between the two clock models at the edge (see [live audio contribution with AES67 and SMPTE 2110](https://www.forasoft.com/learn/audio-for-video/articles-audio/live-audio-contribution-aes67-smpte-2110)).

------------------------------------------------------------------------

## A worked example: diagnosing a slow drift

Put the pieces together with a realistic fault. A monitoring station reports that a channel's audio is 40 milliseconds behind the video after two hours, though it started in sync. The PTS and DTS values look clean. Where is the bug?

    Symptom    : audio 40 ms late after 2 hours; in sync at the start
    Drift rate : 40 ms ÷ 2 hours = 40 ms ÷ 7,200 s ≈ 5.6 microseconds per second

    As a clock-frequency error:
       5.6 µs/s ÷ 1 second = 5.6 ppm of clock offset

    Within the ±30 ppm allowed? Yes — so the decoder stays locked,
       but a 5.6 ppm offset is enough to accumulate 40 ms over 2 hours.

The drift is small enough that the decoder never loses lock and never drops a frame, which is exactly why it passed a quick check. But a steady offset of a few parts per million, accumulating second after second, is the classic signature of **two clocks that are not locked together**. Either the encoder stamps audio from a sample clock that is not derived from its 27 MHz system clock, or the decoder plays audio from a local output clock that is not slaved to the recovered STC, so a small PCR frequency offset that the video path follows is not followed by the audio path. The fix is not in the PTS or DTS values; it is in the clock locking at the encoder, or in slaving the decoder's audio output to the STC (or correcting the drift by resampling). The method is the lesson: convert the observed drift into a clock-frequency error, check it against the ±30 ppm budget, and you immediately know whether you are chasing a lock failure or a slow accumulation. That single calculation points to the right half of the pipeline.

------------------------------------------------------------------------

## Frequently asked questions

### What is PCR in MPEG-TS?

PCR (program clock reference) is a 42-bit sample of the encoder's 27 MHz system clock, carried in the adaptation field of transport stream packets. The decoder locks its own clock to these samples so it can present every frame at its PTS.

### What is the PCR PID?

The PCR PID is the packet identifier whose packets carry the PCR for a program. It is named in the 13-bit PCR_PID field of the program map table; it is usually the video PID, and 0x1FFF means the program has no PCR.

### How often must PCR be sent?

At least every 100 ms (ISO/IEC 13818-1), and ETSI TR 101 290 flags a PCR_repetition_error above that. Real encoders send PCRs every 20–40 ms; the old 40 ms DVB limit was dropped in 2005.

### What is PCR jitter?

PCR jitter is how far PCR values, or their arrival times, sit from where a perfectly steady 27 MHz clock would put them. The standard allows ±500 ns at the multiplexer output; network jitter on top of that shows up in analyzers as PCR overall jitter.

### What does PCR_accuracy_error mean?

PCR_accuracy_error (TR 101 290 check 2.4) means a PCR value is more than ±500 ns off for its position in the stream. The usual cause is a remux step that moved packets without re-stamping their PCRs.

### What is the difference between PCR and PTS?

The PCR is the clock; the PTS is a time on that clock. The PCR lets the decoder rebuild the encoder's 27 MHz clock, and each PTS (in 90 kHz units, 27 MHz ÷ 300) says when a frame is shown against it.

### Does HLS use PCR?

Only HLS with MPEG-TS segments does: each .ts segment is a small transport stream with its own PCRs. HLS with fragmented MP4 segments has no PCR and times media from the track fragment decode time instead.

[↓ Free download: PCR Reference CardOne page: the 27 MHz clock math, the 33-bit base and 9-bit extension encoding, the PCR = base × 300 + ext formula, and the four PCR jitter, drift, offset and interval limits with their standard values.](https://www.forasoft.com/learn/downloads/pcr-reference-card)

------------------------------------------------------------------------
