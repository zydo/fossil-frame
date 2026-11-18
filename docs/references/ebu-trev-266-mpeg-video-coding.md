> **Snapshot** of <https://tech.ebu.ch/docs/techreview/trev_266-ely.pdf>
> Retrieved 2026-11-17; main content converted to Markdown.
> Copyright belongs to the original authors and publisher. This copy is kept
> only as a reference backup and is **not** covered by this repository's MIT license.
> Converted from PDF with pdftotext; layout, figures and equations are approximate.

---

```text
MPEG video coding
A simple introduction
Dr. S.R. Ely (BBC)

                                                                                                The core element of all DVB
                                                                                                systems is the MPEG-2 vision
                                         1.    Introduction                                     coding standard, which is based
                                The Moving Pictures Expert Group (MPEG)                         upon a flexible toolkit of techniques
                                started in 1988 as Working Group 11, Sub-                       for bit-rate reduction.
                                committee 29, of ISO/IEC JTC11 with the aim of
                                                                                                The MPEG-2 specification only
                                defining the standards for digital compression of
                                video and audio signals. It took as its basis the               defines the bit-stream syntax and
                                ITU-T2 standard for video-conferencing and                      decoding process. The coding
                                video-telephony [1], together with that of the Joint            process is not specified, which
                                Photographic Experts Group (JPEG) which had                     means that compatible improve-
                                initially been developed for compressing still                  ments in the picture quality will
                                images such as electronic photography [2].                      continue to be possible.
                                The first goal of MPEG was to define a video                    In this article, the author provides a
                                coding algorithm for digital storage media, in                  simple introduction to the techni-
                                particular CD-ROM. The resulting standard was                   calities of the MPEG-2 video coding
                                published in 1993 as ISO/IEC 11172 [3] and com-                 standard.
                                prises three parts, covering the systems aspects
                                (multiplexing and synchronization), video coding
                                and audio coding. This standard has been applied
                                                                                              In 1990, MPEG began work on a second standard
                                in the CD-i system to provide full motion video
                                                                                              which would be capable of coding interlaced
                                playback from CD, and is widely used in PC
                                                                                              pictures directly, originally to support high-quality
                                applications for which a range of hardware and
                                                                                              applications at bit-rates in the range of about 5 to
                                software coders and decoders are available.
                                                                                              10 Mbit/s. MPEG-2 now also supports high-
                                                                                              definition formats at bit-rates in the range of about
                                MPEG-1 is restricted to non-interlaced video for-
                                                                                              15 to 30 Mbit/s. The MPEG-2 standard was first
                                mats and is primarily intended to support video
                                                                                              published in 1994 as ISO/IEC 13818, again com-
                                coding at bit-rates up to about 1.5 Mbit/s.
                                                                                              prising three parts – systems, video and audio. A
                                                                                              second version of the standard was published in
                                1.   Joint Technical Committee No. 1 of the International     1995 [4].
                                     Organisation for Standardisation and the International
                                     Electrotechnical Commission.                             It is important to note that the MPEG standards
Original language: English
                                2.   International Telecommunication Union                    specify only the syntax and semantics of the bit-
Manuscript received 30/11/95.        – Telecommunication Standardization Bureau.              streams and the decoding process. They do not

12                                                                                                            EBU Technical Review Winter 1995
                                                                                                                                            Ely
specify the coding process: this is left mainly to the      – the limit of temporal resolution (i.e. the abil-
discretion of the coder designers, thus giving scope          ity of the eye to track fast-moving images).
for improvement as coding techniques are refined              Temporal resolution means, for example,
and new techniques are developed.                             that a change of picture (a shot-change)
                                                              masks the fine detail on either side of the
                                                              change.
        2.   Video coding principles
If we take a studio-quality 625-line component
                                                                 3.   MPEG video compression
picture and digitize it according to ITU Recom-                       toolkit
mendations BT.601 [5] and BT.656 [6] (i.e. if we         Sample-rate reduction is a very effective method
use 4:2:2 sampling as shown in Fig. 1), a bit-           of reducing the bit-rate but, of course, it introduces
stream of 216 Mbit/s is used to convey the lumi-         irreversible loss of resolution. For very low bit-
nance and the two chrominance components. For            rate applications (e.g. in MPEG-1), alternate fields
bandwidth-restricted media – such as terrestrial or      are discarded and the horizontal sampling-rate is
satellite channels – a method is required to reduce      reduced to around 360 pixels-per-line (giving
the bit-rate needed to represent the digitized           about 3.3 MHz resolution). The sample rate for
picture.                                                 the chrominance is half that of the luminance, both
                                                         horizontally and vertically. In this way, the bit-rate
A video bit-rate reduction (compression) system          can be reduced to less than one fifth that of a con-
operates by removing the redundant and less-             ventional definition (4:2:2) sampled signal.
important information from the signal prior to
transmission, and by reconstructing an approxima-        For “broadcast quality” at bit-rates in the range 3
tion of the image from the remaining information         to 10 Mbit/s, horizontal sample-rate reduction is
at the decoder. In video signals, three distinct         not advisable for the luminance or chrominance
kinds of redundancy can be identified:                   signals, nor is temporal sub-sampling. However,
                                                         for distribution and broadcast applications, suffi-
1) Spatial and temporal redundancy                       cient chrominance resolution can be provided if
                                                         the sampling frequency of the vertical chromi-
   Here, use is made of the fact that the pixel values
                                                         nance is halved. Thus, for most MPEG-2 coding
   are not independent but are correlated with their
                                                         applications, 4:2:0 sampling is likely to be used
   neighbours, both within the same frame and
                                                         rather than 4:2:2. However, 4:2:2 and 4:4:4 sam-
   across frames. So, to some extent, the value of
                                                         pling are also supported by MPEG-2. It may be of
   a pixel is predictable, given the values of the
                                                         interest to note that a conventional delay-line PAL                    Figure 1
   neighbouring pixels.
                                                         decoder effectively yields the same vertical sub-               4:2:2 sampling.

2) Entropy redundancy
   For any non-random digitized signal, some
                                                                                                              13.5 MHz
   code values occur more frequently than others.                                           5.75 MHz                     8 bits
   This can be exploited by coding the more-
   frequently occurring values with shorter codes            R                                                    ADC             Y
   than the rarer ones. This same principle has
   long been exploited in Morse code where the                                                                6.75 MHz
   most common letters in English, “E” and “T”,                          RGB
                                                                                            2.75 MHz                     8 bits
   are represented by one dot and one dash, res-                          to                                      ADC
                                                             G                                                                    CB
   pectively, whereas the rarest letters, “X”, “Y”                       YUV
                                                                         matrix
   and “Z”, are each represented by a total of four
   dots and dashes.                                                                                           6.75 MHz
                                                                                            2.75 MHz                     8 bits

3) Psycho-visual redundancy                                  B                                                    ADC             CR

   This form of redundancy results from the way
   the eye and the brain work. In audio, we are
   familiar with the limited frequency response of                                          Y  8  13.5  108
   the ear: in video, we have to consider two limits:                                      C B  8  6.75  54
                                                                                           C R  8  6.75  54
   – the limit of spatial resolution (i.e. the fine
     detail which the eye can resolve);                                                                Total  216 Mbits

EBU Technical Review Winter 1995                                                                                                       13
Ely
                                  sampling of the chrominance signals as does 4:2:0       of a different DCT “basis” function to the original
                                  sampling.                                               image block. The lowest frequency basis function
                                                                                          (top-left in Fig. 3) is called the DC coefficient and
                                  Apart from sample-rate reduction, the MPEG tool-        may be thought of as representing the average
                                  kit includes two different kinds of tools to exploit    brightness of the block.
                                  redundancy in images:
                                                                                          The DCT does not directly reduce the number of
                                  1) Discrete Cosine Transform (DCT)                      bits required to represent the block. In fact, for an
                                      The purpose of using this orthogonal transform      8 x 8 image block of 8-bit pixels, the DCT pro-
                                      – which is similar to the Discrete Fourier Trans-   duces an 8 x 8 block of at least 11-bit DCT co-
                                      form (DFT) – is to assist the processing which      efficients, to allow for reversibility! The reduction
                                      removes spatial redundancy, by concentrating        in the number of bits follows from the fact that, for
                                      the signal energy into relatively few coeffi-       typical blocks of natural images, the distribution of
                                      cients.                                             coefficients is non-uniform – the transform tends
                                                                                          to concentrate the energy into the low-frequency
                                  2) Motion-compensated interframe                        coefficients, and many of the other coefficients are
                                     prediction                                           near zero. The bit-rate reduction is achieved by not
                                                                                          transmitting the near-zero coefficients, and by
                                      This tool is used to remove temporal redun-         quantizing and coding the remaining coefficients
                                      dancy. It is based on techniques similar to the     as described below. The distribution of the non-
                                      well-known differential pulse-code modulation       uniform coefficients is a result of the spatial redun-
                                      (DPCM) principle.                                   dancy present in the original image block.

                                         3.1.   Discrete cosine transform                 Many different forms of transformation have been
                                                                                          investigated for bit-rate reduction. The best trans-
                                  The luminance signal of a 4:2:0-sampled digitized       forms are those which tend to concentrate the ener-
                                  625-line picture comprises about 704 pixels hori-       gy of a picture block into a few coefficients. The
                                  zontally and about 576 lines vertically (see Fig. 2).   DCT is one of the best transforms in this respect
                                  In MPEG coding, spatial redundancy is removed           and has the advantage that the DCT and its inverse
                                  by processing the digitized signals in 2-D blocks of    are easy to implement in digital processing. The
                                  8 pixels by 8 lines (taken from either one field or     choice of an 8 x 8 block-size is a trade-off between
                                  two, depending on the mode of operation).               the need to use a large picture area for the trans-
                                                                                          form, so the energy compaction described above is
                                  As Fig. 3 illustrates, the DCT transform is a revers-   most efficient, and the fact that the content and
                                  ible process which maps between the normal 2-D          movement of the picture varies spatially, which
                                  presentation of the image and one which repre-          would tend to support a smaller block-size. A large
                                  sents the same information in what may be thought       block-size would also emphasize variations from
                                  of as the frequency domain. Each coefficient in the     block-to-block in the decoded picture; it would
                                  8 x 8 DCT domain block indicates the contribution       also emphasize the effects of “windowing” by the
                                                                                          block structure.

                         88 blocks
                                                                                                3.2.   Coefficient quantization

                         704 pixels                                                       After a block has been transformed, the transform
                                                                                          coefficients are quantized. Different quantization

 72 blocks
                                                                                          is applied to each coefficient depending on the
                                                                                          spatial frequency within the block that it repre-
             576 lines
                                                                                          sents. The objective is to minimize the number of
                                                                       8                  bits which must be transmitted to the decoder, so
                                                                                          that it can perform the inverse transform and re-
                                                                                          construct the image: reduced quantization accura-
                                                                                          cy reduces the number of bits which need to be
                                                                                          transmitted to represent a given DCT coefficient,
                                                        8                                 but increases the possible quantization error for
                                                                                          that coefficient. Note that the quantization noise
                                                                                          introduced by the coder is not reversible in the
Figure 2                                                                                  decoder, so the coding and decoding process is
Block-based DCT.                                                                          “lossy”.

14                                                                                                         EBU Technical Review Winter 1995
                                                                                                                                         Ely
                                          d.c. coefficient
                                                                            Horizontal                       Increasing cycles per
                   8                                                       frequencies                       picture width

                                                        Vertical
                                    DCT
  8                                                                                                          8
                                                      frequencies
                                     IDCT                                                                                                           Figure 3
                                                                                                                                        DCT transform pairs.

                                                                                8
                                               Increasing cycles
                                               per picture height

More quantization error can be tolerated in the                     tern, which is preferable for pictures without a
high-frequency coefficients, because HF noise is                    strong vertical structure, there is no bias and the
less visible than LF quantization noise. Also,                      scan proceeds diagonally from top left to bottom
quantization noise is less visible in the chromi-                   right, as illustrated in Fig. 4. The coder indicates
nance components than in the luminance compo-                       its choice of scan pattern to the decoder.
nent. MPEG uses weighting matrices to define the
relative accuracy of the quantization of the differ-                The strings of coefficients produced by the zigzag
ent coefficients. Different weighting matrices can                  scanning are coded by counting the number of zero
be used for different frames, depending on the pre-                 coefficients preceding a non-zero coefficient, i.e.
diction mode used.                                                  run-length coded. The run-length value, and the                  Figure 4
                                                                    value of the non-zero coefficient which the run of      Scanning of DCT
The weighted coefficients are then passed through                   zero coefficients precedes, are then combined and         blocks and run-
a fixed quantization law, which is usually a linear                 coded using a variable-length code (VLC). The          length coding with
law. However, for some prediction modes there is                    VLC exploits the fact that short runs of zeros are variable-length codes
                                                                    more likely than long ones, and small coefficients      (Entropy coding).
an increased threshold level (i.e. a dead-zone)
around zero. The effect of this threshold is to max-
imize the number of coefficients which are quan-                         d.c. coefficient
tized to zero: in practice, it is found that small devi-
ations around zero are usually caused by noise in
the signal, so suppressing these values actually                                                                       Horizontal frequencies
“improves” the subjective picture quality.

Quantization noise is more visible in some blocks
than in others; for example, in blocks which con-
tain a high-contrast edge between two plain areas.
In such blocks, the quantization parameters can be

                                                                                      Vertical frequencies
modified to limit the maximum quantization error,
particularly in the high-frequency coefficients.

      3.3.    Zigzag coefficient scanning,
              run-length coding, and
              variable-length coding

After quantization, the 8 x 8 blocks of DCT co-
efficients are scanned in a zigzag pattern (see
Fig. 4) to turn the 2-D array into a serial string of
quantized coefficients. Two scan patterns are de-
fined. The first is usually preferable for picture
material which has strong vertical frequency com-
ponents due to, perhaps, the interlace picture struc-                Note 1:   Zigzag scanning.
ture. In this scan pattern, there is a bias to scan                  Note 2:   Run/amplitude coding: the run of zeros and the amplitude of the DCT
vertical coefficients first. In the second scan pat-                           coefficient are given one Variable Length Code (VLC) (Huffman Code).

EBU Technical Review Winter 1995                                                                                                                          15
Ely
                                                                             Buffer occupancy control

Y, CR or CB   Line-scan
                                                                                        Run-
                  to                                                  Zigzag
                                   DCT          Quantization                           length           VLC            Buffer
              block-scan                                               scan             code                                      Output
              conversion

Figure 5                   are more likely than large ones. The VLC allocates         complexity of the picture information and the
Basic DCT coder.           codes which have different lengths, depending              amount and type of motion in the picture. To pro-
                           upon the expected frequency of occurrence of each          duce the constant bit-rate needed for transmission
                           zero-run-length / non-zero coefficient value com-          over a fixed bit-rate system, a buffer is needed to
                           bination. Common combinations use short code               smooth out the variations in bit-rate. To prevent
                           words; less common combinations use long code              overflow or underflow of this buffer, its occupancy
                           words. All other combinations are coded by the             is monitored and feedback is applied to the coding
                           combination of an escape code and two fixed-               processes to control the input to the buffer. The
                           length codes, one 6-bit word to indicate the run           DCT quantization process is often used to provide
                           length, and one 12-bit word to indicate the co-            direct control of the input to the buffer: as the
                           efficient value.                                           buffer becomes full, the quantizer is made coarser
                                                                                      to reduce the number of bits used to code each DCT
                           One VLC code table is used in most circumstances.          coefficient: as the buffer empties, the DCT quanti-
                           However, a second VLC code table is used for               zation is made finer. Other means of controlling
                           some special pictures. The DC coefficient is               the buffer occupancy may be used as well as, or
                           treated differently in some modes. However, all            instead of, the control of DCT coefficient quanti-
                           the VLCs are designed such that no complete code-          zation.
                           word is the prefix of any other codeword: they are
                           similar to the well-known Huffman code. Thus the           Fig. 5 shows a block diagram of a basic DCT codec
                           decoder can identify where one variable-length             with, in this example, the buffer occupancy con-
                           codeword ends and another starts, when operating           trolled by feedback to the DCT coefficient quanti-
                           within the correct codebook. No VLC or combina-            zation.
                           tion of codes is allowed to produce a sequence of
                           23 contiguous zeros – this particular sequence is          It is important to note that the final bit-rate at the
                           used for synchronization purposes.                         output of an MPEG video encoder can be freely
                                                                                      varied: if the output bit-rate is reduced, the buffer
                           DC coefficients in blocks contained within intra           will empty more slowly and the coder will auto-
                           macroblocks (see Section 3.7.) are differentially          matically compensate by, for example, making the
                           encoded before variable-length coding.                     DCT coefficient quantization coarser. But, of
                                                                                      course, reducing the output bit-rate reduces the
                                3.4.       Buffering and feedback                     quality of the decoded pictures. There is no need
                                                                                      to lock input sampling rates to channel bit-rates, or
                           The DCT coefficient quantization, the run-length           vice-versa.
Figure 6                   coding and the variable-length coding processes
Basic DPCM coder.          produce a varying bit-rate which depends upon the                3.5.    Reduction of temporal
                                                                                                    redundancy: interframe
                                                                                                    prediction

 Input                                                         Quantized              In order to exploit the fact that pictures often
                              Quantizer                        prediction error       change little from one frame to the next, MPEG
     +ve                                                       to channel             includes temporal prediction modes: that is, we
               –ve
                                                                                      attempt to predict one frame to be coded from a
                                                                                      previous “reference” frame.

                                                                                      Fig. 6 illustrates a basic differential pulse code
                                                   Locally-decoded                    modulation (DPCM) coder in which we quantize
                                                   output                             and transmit only the differences between the input
                               Predictor
                                                                                      and a prediction based on the previous locally-
                                                                                      decoded output. Note that the prediction cannot be

16                                                                                                      EBU Technical Review Winter 1995
                                                                                                                                      Ely
                        Prediction
   Input                  error
                                      DCT              Quantizer                          DCT of
    +ve                                                                                   prediction error

                  –ve

                                                                        Inverse
                                                                          DCT

                                                                                                                                Figure 7
                                                                                                                     DCT with interframe
                                                                                                                       prediction coder.

                                         Frame
                                         delay

based on previous source pictures, because the pre-     One method of determining the motion that has
diction has to be repeatable in the decoder (where      occurred between the block being coded and the
the source pictures are not available). Consequent-     reference frame is a “block-matching” search in
ly, the coder contains a local decoder which recon-     which a large number of trial offsets are tested in
structs pictures exactly as they would be in the        the coder (see Fig. 9).
actual decoder. The locally-decoded output then
forms the input to the predictor. In interframe pre-    The “best” offset is selected on the basis of a mea-                     Figure 8
diction, samples from one frame are used in the         surement of the minimum error between the block             Motion-compensated
prediction of samples in other “reference” frames.      being coded and the prediction. Since MPEG de-              interframe predictiom

In MPEG coding, we combine interframe predic-
tion (which reduces temporal redundancy) with                                                Frame n–1 (previous)
the DCT and variable-length coding tools that
were described in Section 3.3. (which reduce spa-
tial redundancy), as shown in Fig. 7. The coder
subtracts the prediction from the input to form a
prediction-error picture. The prediction error is                                                   Non-motion-
                                                                   Macroblock                      compensated
transformed with the DCT, the coefficients are                     vector offset                     prediction
quantized, and these quantized values are coded
using a VLC.
                                                                                                                         Frame n (current)
The simplest interframe prediction is to predict a
block of samples from the co-sited (i.e. the same
spatial position) block in the reference frame. In
this case the “predictor” would comprise simply a
delay of exactly one frame, as shown in Fig. 7.
This makes a good prediction for stationary re-
gions of the image but is poor in moving areas.                                                      16
                                                         Macroblock used for
                                                         motion-compensated                                  16
      3.6.   Motion-compensated                               prediction
             interframe prediction

A more sophisticated prediction method, known as
motion-compensated interframe prediction, off-                                                                        Macroblock grid
sets any translational motion which has occurred
between the block being coded and the reference
                                                                                   Position of macroblock
frame, and uses a shifted block from the reference                                   in previous frame
frame as the prediction (see Fig. 8).

EBU Technical Review Winter 1995                                                                                                        17
Ely
                                                                                           ent from frame to frame. However, increasing the
         Search block                                     Search area                      size of the search area greatly increases the proces-
                                                                                           sing needed to find the best match: various tech-

ÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂ
         (macroblock)
                                                                                           niques such as hierarchical block matching are

ÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂ                                                                        used to try to overcome this dilemma.

ÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂ                                                                        Bi-directional prediction (see Fig. 10) consists of

ÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂ                                                                        forming a prediction from both the previous frame

ÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂ                                                                        and the following frame, by a linear combination

ÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂ
                                                                                           of these, shifted according to suitable motion esti-
                                                                                           mates.

ÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂÂ                                                                        Bi-directional prediction is particularly useful
                                                                                           where motion uncovers areas of detail. However,
     Search block is reference                    Search block moved around
                                                 search area to find best match            to enable backward prediction from a future frame,
                                                                                           the coder re-orders the pictures so that they are
                                                                                           transmitted in a different order from that in which
Figure 9                 fines only the decoding process, not the coder, the               they are displayed. This process, and the process
Principle of             choice of motion measurement algorithm is left to                 of re-ordering to the correct display sequence in
block-matching           the designer of the coder and is an area where con-               the decoder, introduces considerable end-to-end
motion.                  siderable difference in performance occurs be-                    processing delay which may be a problem in some
                         tween different algorithms and different imple-                   applications. To overcome this, MPEG defines a
                         mentations. A major requirement is to have a                      profile (see Section 4) which does not use bi-
                         search area large enough to cover any motion pres-                directional prediction.

                                                                 Frame n–1 (previous)

                                 Macroblock
                                 vector offset                            Intra
                                                                        prediction

                                                                                             Frame n (current)

                                                                                        Position of macroblock
                                                                                             in frame n+1

                                      Bi-directional                                                                 Frame n+1 (next)
                                       prediction

                                                       Position of macroblock
                                                            in frame n–1
                                                                                                             Macroblock
                                                                                                             vector offset

Figure 10
Motion-compensated
bi-directional
prediction.

18                                                                                                          EBU Technical Review Winter 1995
                                                                                                                                          Ely
                              Prediction
        Input                   error
                                             DCT          Quantizer                       DCT of
         +ve                                                                              prediction error

                        –ve

                                                                       Inverse
                                                                         DCT

                                                                                                                        Figure 11
                                                                                                             Motion-compensated
                                                                                                             interframe prediction
                                                                                                                            DCT.
                  Variable
                   delay

                                                       Fixed
                                                       delay

                                 Motion
                              compensation         Displacement
                                  unit             vectors

Whereas the basic coding unit for spatial redun-       prediction. For example, a macroblock may be
dancy reduction in MPEG is based on an 8 x 8           “forward predicted” from a past picture, “back-
block, motion-compensation is usually based on a       ward predicted” from a future picture, or “inter-
16 pixel by 16 line macroblock. The size of the        polated” by averaging a forward and backward
macroblock is a trade-off between the need to          prediction. Another option is to make a zero-
minimize the bit-rate required to transmit the mo-     value prediction, such that the source image block
tion representation (known as motion vectors) to       rather than the prediction error-block is DCT-
the decoder, which supports the case for a large       coded. Such macroblocks are known as intra- or
macroblock size, and the need to vary the predic-      I-coded.
tion process locally within the picture content and
movement, which supports the case for a small ma-      Although no prediction information is needed for
croblock size.                                         intra-macroblocks, they can carry motion vector
                                                       information. In normal circumstances, the motion
To minimize the bit-rate needed to transmit the        vector information for an I-coded macroblock is
motion vectors, they are differentially-encoded        not used, but its function is to provide a means of
with reference to previous motion vectors. The         concealing the decoding errors when data errors in
motion vector value prediction error is then vari-     the bit-stream make it impossible to decode the
able-length coded using another VLC table.             data for that macroblock.

Fig. 11 shows a conceptual motion-compensated          Fields of a frame may be predicted separately from
inter-frame DCT coder in which, for simplicity, we     their own motion vector (field prediction coding),
illustrate implementing the process of motion-         or together using a common motion vector (frame
compensated prediction by suggesting a “variable       prediction coding). Generally, in the case of image
delay”. In practical implementations, of course,       sequences where the motion is slow, frame predic-
the motion-compensated prediction is implement-        tion coding is more efficient. However, when mo-
ed in other ways.                                      tion speed increases, field prediction coding be-
                                                       comes more efficient.
     3.7.       Prediction modes
                                                       In addition to the two basic modes of field and
In an MPEG-2 coder, the motion-compensated             frame prediction, two further modes have been de-
predictor supports many methods for generating a       fined:

EBU Technical Review Winter 1995                                                                                                19
Ely
 Decoder
    input          Input                 VLC                   Inverse                    Inverse
                   buffer               decoder               quantizer                     DCT

                                                                              Difference
                                                                                  picture            Coded        Not coded
                                               Motion
                                               vectors

                                                                                                                                 Display             Decoder
                  Previous                                                                                    Adder
                                        Motion                                      Forward                                       buffer             output
                    I or P
                                     compensation                                  prediction
                picture store
                                                                                                                 Prediction
                                                                              Interpolated
                                                          Interpolator
                                                                                prediction

                   Future                                                          Backward           No
                                        Motion
                    I or P                                                                            prediction
                                     compensation                                  prediction
                picture store

Figure 12                       1) 16 x 8 motion compensation                                        pictures (see Section 3.8) when there have been
Decoding a “B”                                                                                       no B-pictures between the P-picture and its ref-
macroblock.                       This mode uses at least two motion vectors for
                                                                                                     erence frame. In this case, a motion vector and
                                  each macroblock: one vector is used for the up-
                                                                                                     a differential-offset motion vector are trans-
                                  per 16 x 8 region and one for the lower half. (In
                                                                                                     mitted.
                                  the case of B-pictures (see Section 3.8), a total
                                  of four motion vectors are used for each macro-
                                                                                                     For field pictures, two motion vectors are
                                  block in this mode, since both the upper and the
                                                                                                     derived from this data and are used to form two
                                  lower regions may each have motion vectors
                                                                                                     predictions from two reference fields. These
                                  referring to past and future pictures.):
                                                                                                     two predictions are combined to form the final
                                                                                                     prediction.
                                  The 16 x 16 motion compensation mode is per-
                                  mitted only in field-structured pictures and is
                                  intended to allow that, in such cases, the spatial                 For frame pictures, this process is repeated for
                                  area covered by each motion vector is approxi-                     each of the two fields: each field is predicted
                                  mately equal to that of a 16 x 16 macroblock in                    separately, giving rise to a total of four field
                                  a frame structure picture.                                         predictions which are combined to form the fi-
                                                                                                     nal two predictions. Dual prime mode is used
                                                                                                     as an alternative to bi-directional prediction,
                                2) Dual prime mode
                                                                                                     where low delay is required: it avoids the frame
Figure 13                         This mode may be used in both field- and frame-                    re-ordering needed for bi-directional prediction
MPEG picture types.               structured coding but is only permitted in P-                      but achieves similar coding efficiency.

                                                I            B              B              P           B             B           P            B
                                             picture      picture        picture        picture     picture       picture     picture      picture

                   Forward prediction
                   Backward prediction

Note 1:     An intra-coded (I) picture is coded using information only from itself.
Note 2:     Predictive-coded (P) pictures are coded with reference to a previous I or P picture.
Note 3:     Bidirectionally-predictive (B) pictures are coded with reference to both the previous I or P picture and the next (future) I or P picture.

20                                                                                                                    EBU Technical Review Winter 1995
                                                                                                                                                    Ely
For each macroblock to be coded, the coder                   3) Bi-directionally-predictive pictures
chooses between these prediction modes, trying to               (B-pictures)
minimize the distortions on the decoded picture
                                                                 These use both past and future I- or P-pictures
within the constraints of the available channel bit-
                                                                 for motion compensation, and offer the highest
rate. The choice of prediction mode is transmitted
                                                                 degree of compression. As noted above, to en-
to the decoder, together with the prediction error,
                                                                 able backward prediction from a future frame,
so that it can regenerate the correct prediction.
                                                                 the coder re-orders the pictures from the natural
                                                                 display order to a “transmission” (or “bit-
Fig. 12 illustrates how a bi-directionally coded                 stream”) order so that the B-picture is trans-
macroblock (a B-macroblock) is decoded. The                      mitted after the past and future pictures which
switches illustrate the various prediction modes                 it references (see Fig. 14). This introduces a
available for such a macroblock. Note that the                   delay which depends upon the number of con-
coder has the option not to code some macro-                     secutive B-pictures.
blocks: no DCT coefficient information is trans-
mitted for those blocks and the macroblock ad-                      3.9.    Group of pictures
dress counter skips to the next coded macroblock.
The decoder output for the uncoded macroblocks               The different picture types typically occur in a re-
simply comprises the predictor output.                       peating sequence termed a Group of Pictures or
                                                             GOP. A typical GOP is illustrated in display order
                                                             in Fig. 14(a) and in transmission order in Fig.
      3.8.    Picture Types
                                                             14(b).
In MPEG-2, three “picture types” are defined (see
                                                             A regular GOP structure can be described with two
Fig. 13). The picture type defines which predic-
                                                             parameters:
tion modes may be used to code each macroblock:
                                                             – N (the number of pictures in the GOP);
1) Intra pictures (I-pictures)                               – M (the spacing of the P-pictures).
  These are coded without reference to other pic-
                                                             The GOP illustrated in Fig. 14 is described as
  tures. Moderate compression is achieved by
                                                             N = 9 and M = 3.
  reducing spatial redundancy but not temporal
  redundancy. They are important as they pro-
                                                             For a given decoded picture quality, coding – using
  vide access points in the bit-stream where de-
                                                             each picture type – produces a different number of
  coding can begin without reference to previous
                                                             bits. In a typical sequence, a coded I-picture needs
  pictures.
                                                             three times more bits than a coded P-picture, which
                                                             itself occupied 50% more bits than a coded B-
2) Predictive pictures (P-pictures)                          picture.
  These are coded using motion-compensated
  prediction from a past I- or P-picture and may                      4.    MPEG profiles and levels
  be used as a reference for further prediction. By
  reducing spatial and temporal redundancy, P-               MPEG-2 is intended to be generic, supporting a di-
  pictures offer increased compression compared              verse range of applications. Different algorithmic
  to I-pictures.                                             elements or “tools”, developed for many applica-

 Dr. Bob Ely is an R&D manager at BBC Research and Development Department, Kingswood Warren,
 Surrey, UK.
 Currently, he is working with the BBC’s Digital Broadcasting Project which aims to investigate the techni-
 cal and commercial feasibility of digital terrestrial broadcasting and to implement technical field-trials and
 demonstrations.
 After completing his PhD in computer communications systems at Daresbury Nuclear Physics Laboratory,
 Bob Ely joined BBC Research Department to work on RDS and related data transmission systems. He later
 led the BBC team which developed the Nicam digital stereo-sound-with-television system. For many years,
 he was Chairman of the EBU Specialist Group on RDS, a Vice-Chairman of Working Party R and has also
 been a member of EBU Groups on conditional access systems.

EBU Technical Review Winter 1995                                                                                     21
Ely
                        tions, have been integrated into a single bit-stream          profile suitable for low-delay applications such
                        syntax.                                                       as video conferencing.

                        To implement the full syntax in all decoders is un-      2) Main profile
                        necessarily complex, so a small number of subsets             This adds support for B-pictures which im-
                        or profiles of the full syntax have been defined.             proves the picture quality for a given bit-rate but
                        Also, within a given profile, a “level” is defined            increases the delay. Currently, most MPEG-2
                        which describes a set of constraints such as maxi-            video decoder chip-sets support main profile.
                        mum sampling density, on parameters within the
                        profile.                                                 3) SNR profile
                        The profiles defined to date fit together such that           This adds support for enhancement layers of
                        a higher profile is a superset of a lower one. A de-          DCT coefficient refinement, using signal-to-
                        coder which supports a particular profile and level           noise ratio (SNR) scalability.
                        is only required to support the corresponding sub-
                        set of the full syntax and a set of parameter            4) Spatial profile
                        constraints. To restrict the number of options                This adds support for enhancement layers carry-
                        which must be supported, only selected combina-               ing the image at different resolutions, using the
                        tions of profile and level are defined as confor-             spatial scalability tool.
                        mance points (see Table 1). These are:
                                                                                 5) High profile
                        1) Simple profile
                                                                                      This adds support for 4:2:2-sampled video.
Figure 14
                          This uses no B-frames and, hence, no backward
Example Group of          or interpolated prediction. Consequently, no           All MPEG-2 decoders will also decode MPEG-1
Pictures (GOP).           picture re-ordering is required which makes this       pictures (but not vice-versa).

     a     Display order

     B–1    B0     I1       B2     B3       P4    B5      B6     P7      B8      B9        I10    B11      B12     P13
                                                                                                                         etc ...

                                                                                                        Sequence repeats ...

                                                                      Forward prediction
                                                                      Backward prediction

     b     Transmission order

      I1   B–1     B0       P4     B2       B3    P7      B5     B6      I10     B8        B9    P13       B11     B12
                                                                                                                               etc ...

                                                    Re-ordered frames

22                                                                                                  EBU Technical Review Winter 1995
                                                                                                                                  Ely
                                          Profile and maximum total bit-rate (Mbit/s)
                 Maximum           Simple            Main               SNR            Spacial           High
                 sampling        profile (SP)     profile (MP)         profile          profile       profile (HP)
                  density                                            (scalable)       (scalable)
               (Hor/Vert/Freq)
               High level (HL)        _            MP@HL                  _                _             HP@HL
               (1920/1152/60)                      80 Mbit/s                                            100 Mbit/s
                                                                                                      + lower layers
                 High–1440            _           MP@H–14                 _           Spt@H–14         HP@H–14
               (1440/1152/60)                      60 Mbit/s                            60 Mbit/s        80 Mbit/s
                                                                                     + lower layers   + lower layers
  Level        Main level (ML)    SP@ML            MP@ML              SNR@ML               _             HP@ML
                (720/576/30)      15 Mbit/s        15 Mbit/s           15 Mbit/s                         20 Mbit/s
                                                                    + lower layers                    + lower layers
               Low level (LL)         _             MP@LL             SNR@LL               _                _
                (352/280/30)                        4 Mbit/s           4 Mbit/s
                 ISO 11172            _                _                  _                _                _                    Table 1
                 (MPEG-1)                                                                                              MPEG profiles and
                1.856 Mbit/s                                                                                                      levels.
Note 1:   All decoders shall be able to decode ISO/IEC 11172 bitstreams.
Note 2:   SP@ML decoders are required to decode MP@LL bitstreams.

          5.     Conclusions                                     [3] ISO/IEC 11172: Information technology
                                                                     coding of moving pictures and associated
MPEG has been outstandingly successful in defin-                     audio for digital storage media up to about
ing the standards for video compression coding,                      1.5 Mbit/s. Part 1: system.
serving a wide range of applications, bit-rates,
                                                                 [4] ISO/IEC      13818-2:1995: Information
qualities and services. The standards are based                      Technology – Generic coding of moving
upon a flexible toolkit of techniques of bit-rate re-                pictures and associated audio informa-
duction. The specification only defines the bit-                     tion: Video.
stream syntax and decoding process: the coding
process is not specified and the performance of a                [5] ITU-R Recommendation BT.601-3:
coder will vary depending upon, for example, the                     Encoding parameters of digital television
quality of the motion-vector measurement, and the                    for studios.
processes used for prediction mode selection.                    [6] ITU-R Recommendation BT.656-1:
                                                                     Interfaces for digital component video
The picture quality obtained through an MPEG co-                     signals in 525-line and 625-line television
dec depends strongly upon the picture content, but                   systems operating at the 4:2:2 level of
as experience with MPEG coding grows, the bit-                       Recommendation 601.
rate needed for a given picture quality is likely to
reduce.                                                        Further reading:
                                                                    Tudor, P.: MPEG-2: What it is and what it
Acknowledgements                                                    isn’t.
The author gratefully acknowledges the contribu-                    IEE Colloquium on Video Compression,
tions of his BBC colleagues Nick Wells, Phil Tu-                    January 1995.
dor and Paul Burfield in writing this article, which                Wells, N. et al.: DCT source coding and
is based on published and unpublished work by                       current implementations for HDTV.
these three MPEG video experts.                                     EBU Technical Review No. 251, Spring 1992.

                                                                    Wells, N.: Bit-rate reduction of digital tele-
                 Bibliography                                       vision for transmission: an introductory
 [1] ITU-T Standard H.261: Video codec for                          review.
     audiovisual services at P x 64 kbit/s.                         BBC R&D Department Report No. 1994/2.

 [2] ISO/IEC 10918-1: Information Technology                        Sandbank, C.P. (editor): Digital Television.
     – Digital compression and coding of                            John Wiley, Chichester, 1990.
     continuous-tone still images.                                  ISBN 0 471 92360 5.

EBU Technical Review Winter 1995                                                                                                       23
Ely
```
