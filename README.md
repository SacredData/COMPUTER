# COMPUTER

![COMPUTER! WHAT THE FUCK!](http://originaldave77.files.wordpress.com/2014/03/picards-computer.jpg)

Go ahead. He can hear you now.

## About

I have always been really jealous that Captain Picard could just yell, "Computer!" followed by a few terse commands, and get the results he wanted back from his ship in return. So, I dug up some old work I did with Julius and made this thing that controls a modern Linux desktop with voice commands.

## What can COMPUTER do?

Currently, COMPUTER handles commands for the following applications:

* [**i3-wm**](https://github.com/i3/i3): Switch windows; switch to specific apps.
* [**copyq**](https://github.com/hluk/CopyQ): Paste the contents of your clipboard into the presently in-focus X application.
* [**deadbeef**](https://github.com/Alexey-Yakovenko/deadbeef): Play/Pause; Next track; Last track.
* [**talking-clock**](https://github.com/stormdragon2976/talking-clock): Have the computer speak to you the time and current weather.
* [**scrot**](https://github.com/dreamer/scrot): Take a screenshot of the X screen.
* [**fswebcam**](https://github.com/fsphil/fswebcam): Take a photo with your USB webcam.
* [**wordnet**](https://github.com/wordnet/wordnet): Select some text and have the computer speak back to you the top definitions. (Makes use of the [**espeak**](https://github.com/eeejay/espeak) CLI application to vocalize the definitions.)

More integrations are on the way, I promise!

## Dependencies

You'll need to install Julius, or you may prefer to use the Julius binary included in the repo. It should work on most standard x86_64 systems.

The audio feedback is delivered via ALSA.

Of course, if you want to make use of all available voice commands, you'll need to install the apps listed above. ;)

## Setup

First, clone the repo.

Next, you may need to get some packages from pip:

`pip2 install pyjulius pyyaml`

While in the top-level directory of the repo, perform the following commands **in order**:

```
./julius -input mic -C Sample.jconf -module
python2 computer.py
```

## I Wanna Say Stuff!

OK. Once everything is up and running, try these phrases out:

*"Computer: say time"*

*"Computer: define selection"* (Highlight text before saying this command.)

*"Computer: start music"* (Open deadbeef first.)

*"Computer: switch to window two"*

## Custom Grammars and Vocabulary

This is an area that I need to improve upon. Currently, it is a bit of an endeavor to add your own custom voice commands, but it _can_ be done.

#### Changing the vocabulary

COMPUTER's vocabulary can be found in `grammar/sample.voca`. It should look something like this:

```
....
% APPS
INTERNET   ih n t er n eh t
BROWSER    b r aw z er        
SUBLIME    s ah b l ay m

% GENERAL
WINDOW     w ih n d ow

% DESCRIPTOR
ZERO       z iy r ow
ONE        w ah n
TWO        t uw
THREE      th r iy
FOUR       f ao r
....
```

A `%` at the front of the line indicates a vocab CLASS. You should add words where they make the most sense, categorically. You can also add your own classes, but this means that you'll also need to change COMPUTER's grammar file. Only mess with this file if you kinda know what you're doing!

You may use the included dictionary (`grammar/VoxForgeDict.txt`) to find the correct phonetic representations of the words you're adding to the vocabulary file.

Once you've made your modifications, run the perl script within the grammar/ directory like so:

`perl mkdfa.pl sample`

#### Configuring your new vocabulary items

Once you have successfully built the new grammar data for Julius, you have to modify the `magic.py` python2 file and the `config.yaml` included in the top level of the COMPUTER repo. This part should be self-explanitory.
