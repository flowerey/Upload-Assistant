# flower's Upload Assistant

Thanks to @Audionut for the special shout out! Without him, this fork wouldn't exist at all!

Fork of [wastaken's Upload Assistant (desc branch)](https://github.com/wastaken7/Upload-Assistant), with updates from the main repo and my own custom changes.

Clone this repo, install dependencies, and run python config-generator.py. It should be working.

Currently I don't have any plans for adding back Docker support and no plans for a stable release too. Use locally if possible.

## TODOs

* Fix --description, for while, use the automatic description grabber
* Maybe make the signature modifiable?
* Support for TurkSeed, seems hard due to their naming schema

## Features

* Support for custom signatures (see example-config.py)
* Improved UNIT3D description handling
* Customizable timeout for every tracker
* Update mkbrr
* Adds support for RHD
* Fix LDU timeout error

For a complete list of all changes, see [here](https://github.com/Audionut/Upload-Assistant/compare/master...flowerey:Upload-Assistant:main).

## Supported Trackers

| Name              | Acronym | Name                   | Acronym |
| ----------------- | :-----: | ---------------------- | :-----: |
| Aither            |  AITHER | Alpharatio             |    AR   |
| AmigosShareClub   |   ASC   | AnimeLovers            |    AL   |
| Anthelion         |   ANT   | AsianCinema            |   ACM   |
| AvistaZ           |    AZ   | Beyond-HD              |   BHD   |
| BitHDTV           |  BHDTV  | Blutopia               |   BLU   |
| BrasilJapão-Share |   BJS   | BrasilTracker          |    BT   |
| CapybaraBR        |   CBR   | Cinematik              |   TIK   |
| CinemaZ           |    CZ   | DarkPeers              |    DP   |
| DigitalCore       |    DC   | Emuwarez               |   EMUW  |
| FearNoPeer        |   FNP   | FileList               |    FL   |
| Friki             |  FRIKI  | FunFile                |    FF   |
| GreatPosterWall   |   GPW   | hawke-uno              |   HUNO  |
| HDBits            |   HDB   | HD-Space               |   HDS   |
| HD-Torrents       |   HDT   | HomieHelpDesk          |   HHD   |
| InfinityHD        |   IHD   | ImmortalSeed           |    IS   |
| ItaTorrents       |   ITT   | LastDigitalUnderground |   LDU   |
| Lat-Team          |    LT   | Locadora               |   LCD   |
| LST               |   LST   | MoreThanTV             |   MTV   |
| Nebulance         |   NBL   | OldToonsWorld          |   OTW   |
| OnlyEncodes+      |    OE   | PassThePopcorn         |   PTP   |
| PolishTorrent     |   PTT   | Portugas               |    PT   |
| PTerClub          |   PTER  | PrivateHD              |   PHD   |
| PTSKIT            |   PTS   | Racing4Everyone        |   R4E   |
| Rastastugan       |   RAS   | ReelFLiX               |    RF   |
| RetroFlix         |   RTF   | RocketHD               |   RHD   |
| Samaritano        |   SAM   | seedpool               |    SP   |
| ShareIsland       |   SHRI  | SkipTheCommericals     |   STC   |
| SpeedApp          |   SPD   | Swarmazon              |    SN   |
| TorrentHR         |   THR   | Torrenteros            |   TTR   |
| TorrentLeech      |    TL   | ToTheGlory             |   TTG   |
| TVChaosUK         |   TVC   | ULCX                   |   ULCX  |
| UTOPIA            |   UTP   | YOiNKED                |  YOINK  |
| YUSCENE           |   YUS   |

## License

This project is a fork of Audionut/Upload-Assistant, which is distributed under its original license. My contributions, however, are released under the Unlicense.

In practical terms, you are free to copy, modify, distribute, and use my changes in any way you wish—**no attribution required**.

Though he licensed the actual under his ["suspicious"](https://github.com/Audionut/Upload-Assistant/blob/master/LICENSE) license, it doesn't apply to this fork. So go ahead.
