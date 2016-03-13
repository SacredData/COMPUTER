# COMPUTER

![COMPUTER! WHAT THE FUCK!](http://originaldave77.files.wordpress.com/2014/03/picards-computer.jpg)

## About

COMPUTER is a Python 2 program that enables users to control their modern Linux workstations with easy voice commands. Using the Julius continuous speech recognition decoder, users may effortlessly extend the COMPUTER command vocabulary, customize outcomes, and even integrate new applications. (COMPUTER also has limited voice feedback and response capabilities; additional features of this nature are currently under development.)

Once up and running, using COMPUTER is pretty routine. Address your new software servant by eliciting the voice command, *"Computer"*. Then, complete your sentence with whatever whimsical computing desires you conjure up. See the example voice commands below.

### Credits

COMPUTER would not be possible without the work of Antoine Bertin, author of the [pyjulius](https://github.com/Diaoul/pyjulius) Python 2 module.

## What can COMPUTER do?

Currently, COMPUTER handles commands for the following applications:

* [**i3-wm**](https://github.com/i3/i3): Switch windows; switch to specific apps.
* [**copyq**](https://github.com/hluk/CopyQ): Paste the contents of your clipboard into the presently in-focus X application.
* [**ncmpcpp**](http://rybczak.net/ncmpcpp/) - COMING SOON: Play/Pause; Next track; Last track.
* [**talking-clock**](https://github.com/stormdragon2976/talking-clock): Have the computer speak to you the time and current weather.
* [**scrot**](https://github.com/dreamer/scrot): Take a screenshot of the X screen.
* [**fswebcam**](https://github.com/fsphil/fswebcam): Take a photo with your USB webcam.
* [**wordnet**](https://github.com/wordnet/wordnet): Select some text and have the computer speak back to you the top definitions. (Makes use of the [**espeak**](https://github.com/eeejay/espeak) CLI application to vocalize the definitions.)

More integrations are on the way, I promise!

## Dependencies

**This is a Python 2 program.** I don't know what kind of madness will happen if you try to run this with Python 3. My guess is that nothing will work.

You'll need to install Julius, or you may prefer to use the Julius binary included in the repo. It should work on most standard x86\_64 systems.

Of course, if you want to make use of all available voice commands, you'll need to install the apps listed above. ;)

I've designed COMPUTER to use default audio devices and subdevices as configured by the OS, hopefully enabling most properly-setup machines to get started right away. However, the audio feedback is delivered via ALSA, and trust me when I say that your ALSA config will be tested to its limits when working with COMPUTER. If audio input doesn't work, check out your ALSA config file at `~/.asoundrc`. Make sure that you've made the proper audio input the ALSA default. I can't help you with your asoundrc file, because frankly, it's a miracle of Science that my own config works at all. But I've included my asoundrc as an example in this repo. Hopefully it will help!

## Setup

First, clone the repo.

Next, you may need to get some packages from pip:

`pip2 install pyjulius pyyaml`

Next, simply execute `./start_computer`. Once you do this, COMPUTER should be ready to go.

## I Wanna Say Stuff!

OK. Once everything is up and running, try these phrases out:

*"Computer: say time"* - Says the time to you via talking-clock.

*"Computer: define selection"* (Highlight an English word before saying this command.) - Speaks top definition results from wordnet back to you.

*"Computer: start music"* - Plays first track in Deadbeef. (ncmpcpp support coming soon!)

*"Computer: switch to three"* - Move to 3rd desktop in i3

Please note, however, that these commands are tuned to my particular accent of English (think: Jew from New York City.) If your dialect of English is too different from mine (think: Dirty South, USA and Cockney, UK) you may need to revise the `sample.voca` file. Calfironia folks, on the other hand, will probably be fine without any modifications.

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
