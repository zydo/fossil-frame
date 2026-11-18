> **Snapshot** of <https://forum.makemkv.com/forum/viewtopic.php?t=16629>
> Retrieved 2026-11-17; main content converted to Markdown.
> Copyright belongs to the original authors and publisher. This copy is kept
> only as a reference backup and is **not** covered by this repository's MIT license.

---

## [Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?t=16629)

Please post here for issues related to **Blu-ray** discs\

[Post Reply ](https://forum.makemkv.com/forum/posting.php?mode=reply&t=16629 "Post a reply")

- [Print view](https://forum.makemkv.com/forum/viewtopic.php?t=16629&view=print "Print view")

12 posts • Page **1** of **1**

[Scenario](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=21589)

**Posts:** 5

**Joined:** Mon Jul 31, 2017 1:26 am

### [Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?p=57508#p57508)

- [Quote](https://forum.makemkv.com/forum/posting.php?mode=quote&p=57508 "Reply with quote")

[Post](https://forum.makemkv.com/forum/viewtopic.php?p=57508#p57508 "Post") by **[Scenario](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=21589)** » Wed Sep 20, 2017 3:50 pm

[http://www.makemkv.com/errors/read/](http://www.makemkv.com/errors/read/) says:\

> The ONLY reason for this error is inability of the drive to read the data from the disc. This is caused by a damaged disc, failing drive, or both. The error comes from the drive before MakeMKV has an opportunity to look at the data. Nothing else can cause this error - no protection, no software issue - only physical disc or drive damage.

This is a false and misleading claim that can cause users to needlessly replace discs or drives only to find that the error still occurs within MakeMKV.\
\
While physical damage is a obvious cause, these errors more commonly occur due to data mastering errors on otherwise undamaged media. Sometimes those errors repeat across discs and sometimes they don't. Sometimes they occur in the same spot and sometimes they don't. But in almost all cases short of visible, physical damage, these discs will *play* just fine. They just won't *rip*.\
\
Most playback software is able to handle these errors, while MakeMKV is not. MakeMKV *could* handle these errors by interpolating the data or skipping the data across the tiny sections of media that have such data errors. And that omission is MakeMKV's fault — not the user's fault or the disc's fault or the device's fault.\
\
So before MakeMKV exits Beta and can command a \$50 price tag, I would encourage its maker(s) to stop treating data errors as fatal and come up with a graceful solution for dealing with imperfect data.

[ Top](#top "Top")

[Woodstock](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=8764)

**Posts:** 11026

**Joined:** Sun Jul 24, 2011 11:21 pm

### [Re: Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?p=57512#p57512)

- [Quote](https://forum.makemkv.com/forum/posting.php?mode=quote&p=57512 "Reply with quote")

[Post](https://forum.makemkv.com/forum/viewtopic.php?p=57512#p57512 "Post") by **[Woodstock](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=8764)** » Wed Sep 20, 2017 5:46 pm

Playback software does not "fix" read errors. It ignores them, and skips over the damaged section. If it is just a sector or two that is an issue, you MIGHT hear a glitch in the audio, or see a bit of tearing in the video. If it is several sectors long, the software will try reading until it finds the next valid section, or it might give up and take you back to a menu. If it was not reading far enough ahead, your playback will stop while it decides what to do.\
\
The objective of MakeMKV when ripping is to get a bit-perfect copy of the video and audio. It is necessary if you're going to later process that file with other software - the invalid data will cause decoding errors, which are generally interpreted as "end of file". If you want to "skip" errors, there is software out there that will allow you to do it (Linux ships with the program "dd", which has an option to replace errors with the same number of zero bytes), but the read of that file will fail later, due to invalid data.\
\
As for the error message, what is false about what Mike wrote? The operating system reported that the drive was unable to read the disk. So, either there is a problem with the disk, or a problem with the drive. What other component are you saying is to blame? Maybe the operating system? What other solution are you suggesting?\
\
A dirty disk (most common problem) is a damaged disk that just happens to be easily repairable. A scratched disk is less-easily repaired. A manufacturing defect cannot be fixed by the consumer, except by having it replaced by a disk that isn't from the same batch that had the defect.\
\
Drives can have issues when it comes to switching to layer 2 (a problem that occurs at 4.7GB on DVDs, 25GB on BD) if their laser is out of alignment or the lens is damaged. They'll read many disks without issue, but fail if the movie is too big. Drives can have issues with power, which only show up when the drive is accelerated to something near maximum speed; Those issues will "move around" depending on system load, and are more likely to occur on USB-powered drives.\
\
So, again, what is misleading about Mike's statement, other than that you do not believe it?

[MakeMKV Frequently Asked Questions](https://makemkv.com/forum/viewtopic.php?f=1&t=24388)\
[FAQ about BETA and PERMANENT keys.](https://forum.makemkv.com/forum/viewtopic.php?f=1&t=20579)\
How to aid in finding the answer to your problem: [Activating Debug Logging](https://www.makemkv.com/faq/item/8)

[ Top](#top "Top")

[MagmaiKH](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=21998)

**Posts:** 11

**Joined:** Sun Sep 24, 2017 9:57 am

### [Re: Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?p=57605#p57605)

- [Quote](https://forum.makemkv.com/forum/posting.php?mode=quote&p=57605 "Reply with quote")

[Post](https://forum.makemkv.com/forum/viewtopic.php?p=57605#p57605 "Post") by **[MagmaiKH](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=21998)** » Fri Sep 29, 2017 3:34 am

\> So, either there is a problem with the disk, or a problem with the drive.\
\
That's the problem. This is not generally true.\
The third possibility is that an error was introduced at mastering; possibility even deliberately as is the case with Play Station disc.\
They use specialized firmware to deliberate write incorrect ECC codes to the disc.\
\
While I agree that the vast majority of cases are likely actual disc read errors this is a well known technique to thwart ripping.\
(I have no perspective on how wide-spread its use is with Bluray movies but it is ubiquitous for Play Station titles.)\
\
I don't know what the old software did differently but there were special ripping programs for Play Station disc that would read the disc at a lower level.\
I presume they then did the ECC correction in software and they would retry the read some number of times and would treat a repeated ECC failure as a warning not a fatal error.

[ Top](#top "Top")

[Woodstock](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=8764)

**Posts:** 11026

**Joined:** Sun Jul 24, 2011 11:21 pm

### [Re: Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?p=57609#p57609)

- [Quote](https://forum.makemkv.com/forum/posting.php?mode=quote&p=57609 "Reply with quote")

[Post](https://forum.makemkv.com/forum/viewtopic.php?p=57609#p57609 "Post") by **[Woodstock](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=8764)** » Fri Sep 29, 2017 12:40 pm

> That's the problem. This is not generally true.\
> The third possibility is that an error was introduced at mastering; possibility even deliberately as is the case with Play Station disc.\
> They use specialized firmware to deliberate write incorrect ECC codes to the disc.

So, an error in mastering the disk, either deliberate or accidental, is NOT a problem with the disk?\
\
I'm having a bit of a problem with that logic.\
\
But I see your point, when dealing with program/data disks that are deliberately zapped with hard errors that, if not present, mean the disk is fake. That has been around for as long as CDs were used with computers. And Digital Video Disks (the original meaning of DVD) were defined with areas that normal software would expect errors.\
\
That would be a factor if you were trying to duplicate the disk, which is not what MakeMKV is trying to do, and those areas would not be mapped into directory or video tracks.

[MakeMKV Frequently Asked Questions](https://makemkv.com/forum/viewtopic.php?f=1&t=24388)\
[FAQ about BETA and PERMANENT keys.](https://forum.makemkv.com/forum/viewtopic.php?f=1&t=20579)\
How to aid in finding the answer to your problem: [Activating Debug Logging](https://www.makemkv.com/faq/item/8)

[ Top](#top "Top")

[Ultragod](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=30156)

**Posts:** 1

**Joined:** Thu Nov 07, 2019 12:27 am

### [Re: Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?p=80691#p80691)

- [Quote](https://forum.makemkv.com/forum/posting.php?mode=quote&p=80691 "Reply with quote")

[Post](https://forum.makemkv.com/forum/viewtopic.php?p=80691#p80691 "Post") by **[Ultragod](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=30156)** » Thu Nov 07, 2019 2:59 pm

Yes exactly ~ surely MOST of the so-called 'read errors' are really FAKE ones PURPOSELY introduced as 'copy protection' on the discs that won't rip with MakeMKV. Out of a batch of all perfect looking discs, about half of them won't complete a rip with MakeMKV. It really NEEDS fault tolerance if I am ever going to consider buying it. Other programs like Amerisoft, Tipard, & DVD Fab variants have options for that, as well as CD stuff like Exact Audio Copy with 'Accurate Rip', can not only ignore errors but try to repair them at user option (not just 'fail' and 'give up'). Making lame excuses like 'it's the user's fault' or 'the disc or drive fault' is lame & lazy. If programs like 'Unstopable Copier' can even pass errors on regular data CDs (which are more strict than music ones yes, in terms of needing 'good CRC' & stuff?) then it's not a matter of whether we 'should' have this functionality. We MUST have it. I'm not even going to attempt to rip a series of 30+ discs when I know for a FACT that MakeMKV is such an UNRELIABLE program (because it fails to rip half the time) that it will just be a frustrating complete waste of my time to even try.\
\
Copy protection INCLUDES things like 'bad pointers' and other PURPOSELY IMPLANTED ERRORS, so MAKE THE PROGRAM CAPABLE OF IGNORING THOSE ERRORS AND SKIPPING PAST THEM!!! Jeez ~ it's not rocket science =)) If or when this happens, let me know by mailing me at 'balkanguy2 at live dot com' so I can buy this thing. Otherwise, no chance. Put a check box (or various ones for different levels of 'ignoring') so we can select what kind of 'bulletproof' ripping we want. No, I don't care if the video ends up with some dropped frames here & there = no big deal!! Same as a CD with a little dropout here or there = who cares! At least it rips. With CDs the number of them with errors is more like 80% (literally), so if those rippers were so 'picky' as these crazy overly strict MakeMKV fail train programs, nobody would be able to rip audio collections. Give me a break! =)

[ Top](#top "Top")

[Woodstock](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=8764)

**Posts:** 11026

**Joined:** Sun Jul 24, 2011 11:21 pm

### [Re: Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?p=80705#p80705)

- [Quote](https://forum.makemkv.com/forum/posting.php?mode=quote&p=80705 "Reply with quote")

[Post](https://forum.makemkv.com/forum/viewtopic.php?p=80705#p80705 "Post") by **[Woodstock](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=8764)** » Thu Nov 07, 2019 6:24 pm

You appear to be under the impression that MakeMKV is part of a conspiracy to protect disks.\
\
There are programs out there that can be told to ignore errors. On Linux, for example, you can use the 'dd' command, and tell it to replace unreadable sectors with zeros. Then, if you collect enough examples of the disk, with errors in different places, you can construct an ISO that doesn't have errors. This might not be possible if the "bad sectors" are actually part of the disk pressing, as copy protection.\
\
Errors are errors. If you're ripping a disk, and the operating system says the drive cannot read the disk, what you get back can (and often is) garbage. Playback software will stutter (at best) when hitting the bad data. The DVD players I've tried will skip over bad data when playing from a physical media, but do "bad things" (like crash or stop) when playing back a FILE containing the same bad data.\
\
If you read this board, rather than simply trying to plant a reason for you not buying the program, you will find that most "bad disk" scenarios really do turn out to be bad disks. That disk YOU can't read, others have read just fine, because their copies weren't dirty/damaged like yours. I've seen people claim "new copy protection that MakeMKV cannot handle" on disks I've personally ripped with MakeMKV.\
\
So, if your goal is to get a version of MakeMKV that will rip your crappy disks, I don't think Mike is going to go for it. You've already listed off several programs that do what you want MakeMKV to do... Why aren't you using them instead?

[MakeMKV Frequently Asked Questions](https://makemkv.com/forum/viewtopic.php?f=1&t=24388)\
[FAQ about BETA and PERMANENT keys.](https://forum.makemkv.com/forum/viewtopic.php?f=1&t=20579)\
How to aid in finding the answer to your problem: [Activating Debug Logging](https://www.makemkv.com/faq/item/8)

[ Top](#top "Top")

[Grauhaar](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=19582)

**Posts:** 566

**Joined:** Thu Sep 15, 2016 3:46 pm

### [Re: Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?p=80708#p80708)

- [Quote](https://forum.makemkv.com/forum/posting.php?mode=quote&p=80708 "Reply with quote")

[Post](https://forum.makemkv.com/forum/viewtopic.php?p=80708#p80708 "Post") by **[Grauhaar](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=19582)** » Thu Nov 07, 2019 7:02 pm

> [Ultragod](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=30156) wrote: Thu Nov 07, 2019 2:59 pm Out of a batch of all perfect looking discs, about half of them won't complete a rip with MakeMKV.

Sorry to say it, but I cannot confirm your statement. 99,9% of my ripped discs completes without any errors, the 0,01% left are bad discs and the replacement works or the rip works on an different player.

Good Luck \
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\
Useful MakeMKV links: [FAQs](https://www.makemkv.com/faq/) - [Debug Log](https://www.makemkv.com/faq/item/8) - [Buy](https://www.makemkv.com/buy/) - [Expiration of beta key](https://www.makemkv.com/forum/viewtopic.php?f=1&t=20579)\
Two Blu-ray (UHD) Drives LG LG BH16NS55 with Libredrive Firmware 1.04

[ Top](#top "Top")

[Freaky69](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=41283)

**Posts:** 20

**Joined:** Tue May 18, 2021 12:11 pm

### [Re: Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?p=108906#p108906)

- [Quote](https://forum.makemkv.com/forum/posting.php?mode=quote&p=108906 "Reply with quote")

[Post](https://forum.makemkv.com/forum/viewtopic.php?p=108906#p108906 "Post") by **[Freaky69](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=41283)** » Tue May 18, 2021 12:13 pm

Hello guys,\
\
i just ripped an UHD and at the end it says disc has been succesfully ripped but also wrote on the log that there are 2 read errors.\
What does this mean? Could the read errors be corrected or is the file corrupt?

[ Top](#top "Top")

[Woodstock](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=8764)

**Posts:** 11026

**Joined:** Sun Jul 24, 2011 11:21 pm

### [Re: Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?p=108912#p108912)

- [Quote](https://forum.makemkv.com/forum/posting.php?mode=quote&p=108912 "Reply with quote")

[Post](https://forum.makemkv.com/forum/viewtopic.php?p=108912#p108912 "Post") by **[Woodstock](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=8764)** » Tue May 18, 2021 1:48 pm

Most likely that the drive had to do retries to read part of the disk. Default is to try 5 times on errors.

[MakeMKV Frequently Asked Questions](https://makemkv.com/forum/viewtopic.php?f=1&t=24388)\
[FAQ about BETA and PERMANENT keys.](https://forum.makemkv.com/forum/viewtopic.php?f=1&t=20579)\
How to aid in finding the answer to your problem: [Activating Debug Logging](https://www.makemkv.com/faq/item/8)

[ Top](#top "Top")

[Freaky69](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=41283)

**Posts:** 20

**Joined:** Tue May 18, 2021 12:11 pm

### [Re: Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?p=108920#p108920)

- [Quote](https://forum.makemkv.com/forum/posting.php?mode=quote&p=108920 "Reply with quote")

[Post](https://forum.makemkv.com/forum/viewtopic.php?p=108920#p108920 "Post") by **[Freaky69](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=41283)** » Tue May 18, 2021 5:11 pm

Thanks so the File should be okay then?

[ Top](#top "Top")

[Woodstock](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=8764)

**Posts:** 11026

**Joined:** Sun Jul 24, 2011 11:21 pm

### [Re: Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?p=108926#p108926)

- [Quote](https://forum.makemkv.com/forum/posting.php?mode=quote&p=108926 "Reply with quote")

[Post](https://forum.makemkv.com/forum/viewtopic.php?p=108926#p108926 "Post") by **[Woodstock](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=8764)** » Tue May 18, 2021 6:25 pm

Yes, because MakeMKV will have checked it against the checksums published on the disk.

[MakeMKV Frequently Asked Questions](https://makemkv.com/forum/viewtopic.php?f=1&t=24388)\
[FAQ about BETA and PERMANENT keys.](https://forum.makemkv.com/forum/viewtopic.php?f=1&t=20579)\
How to aid in finding the answer to your problem: [Activating Debug Logging](https://www.makemkv.com/faq/item/8)

[ Top](#top "Top")

[alfeberlin](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=51794)

**Posts:** 2

**Joined:** Mon Aug 29, 2022 12:39 pm

### [Re: Misleading Claim about Read Errors](https://forum.makemkv.com/forum/viewtopic.php?p=126369#p126369)

- [Quote](https://forum.makemkv.com/forum/posting.php?mode=quote&p=126369 "Reply with quote")

[Post](https://forum.makemkv.com/forum/viewtopic.php?p=126369#p126369 "Post") by **[alfeberlin](https://forum.makemkv.com/forum/memberlist.php?mode=viewprofile&u=51794)** » Mon Aug 29, 2022 1:22 pm

Yes, there is software out there like dd which replaces unreadable data with dummy data. Since dd is agnostic of the semantics of the data it reads, the best it can do is using zero bytes to fill the gap. And these then produce files which are corrupted and cannot (normally) be processed by video software.\
\
But makemkv is very well aware of what it reads, it even attempts to convert the data into mkv files (typically, hence the name). So we are talking about video files. Video files from BRs, known codecs, etc. Makemkv should do the same as dd does on its level. It should fill gaps of unreadable disc parts with dummy data. And since it knows the context, it can insert proper dummy data for a video file.\
\
That can be black frames, silent audio, empty subtitles, etc. It can even cut the parts out and rearrange the timestamps according to the new (shorted) runtime of the video. But I understand that this is more complicated, so I don’t really expect it. Black frames, silent audio, and empty subtitles would do fine.\
\
But simply aborting at the first error is really a PITA. It forces you to have always perfectly readable mediums, which is just an idea from never-never land. Of course, many are. But to expect that you can replace *any* medium is BS. And with streaming services on the rise, mediums will be rarer and rarer in the future. The age of the existing ones will increase, and so will the hardware errors, scratches, and other signs of that age.\
\
Makemkv must be able to deal with these problems. If not today, then in the future. I’m like ultragod above: I would much prefer being able to skip past the 0.07% of bad blocks and am reluctant to pay for the software if it let’s me out in the rain each time a small scratch appears on the disc.

[ Top](#top "Top")

[Post Reply ](https://forum.makemkv.com/forum/posting.php?mode=reply&t=16629 "Post a reply")

- [Print view](https://forum.makemkv.com/forum/viewtopic.php?t=16629&view=print "Print view")

12 posts • Page **1** of **1**
