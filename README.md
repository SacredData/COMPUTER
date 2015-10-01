# COMPUTER

![COMPUTER! WHAT THE FUCK!](http://originaldave77.files.wordpress.com/2014/03/picards-computer.jpg)

Go ahead. He can hear you now.

## About

I have always been really jealous that Captain Picard could just yell, "Computer!" followed by a few terse commands, and get the results he wanted back from his ship in return. So, I dug up some old work I did with Julius and made this thing that controls a modern Linux desktop with voice commands.

## What can COMPUTER do?

Currently, COMPUTER handles commands for the following applications:

* **i3-wm**: Switch windows; switch to specific apps.
* **copyq**: Paste the contents of your clipboard into the presently in-focus X application.
* **deadbeef**: Play/Pause; Next track; Last track.
* **talking-clock**: Have the computer speak to you the time and current weather.
* **scrot**: Take a screenshot of the X screen.
* **fswebcam**: Take a photo with your USB webcam.
* **wordnet**: Select some text and have the computer speak back to you the top definitions. (Makes use of the **espeak** CLI application to vocalize the definitions.)

More integrations are on the way, I promise!

## Dependencies

You'll need to install Julius, or you may prefer to use the Julius binary included in the repo. It should work on most standard x86_64 systems.

The audio feedback is delivered via ALSA.

Of course, if you want to make use of all available voice commands, you'll need to install the apps listed above. ;)

## I Wanna Say Stuff!

OK. Once everything is up and running, try these phrases out:

*"Computer: say time"*

*"Computer: define selection"* (Highlight text before saying this command.)

*"Computer: start music"* (Open deadbeef first.)

*"Computer: switch to window two"*
