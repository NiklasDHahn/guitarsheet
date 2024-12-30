# GuitarSheet
Generate printable guitar chord sheets.

I recently started to write my own songs again, but I wanted to avoid the chaos of many loose files all flying around and showing up at random places. So I decided that I will store them digitally and defining my own standards, so that each song file will follow the same guidelines. This makes reading them at a later point much easier. I started to write my songs using a simple text file. Later I realized that I also wanted to control how the file is formated to print nicely or even visualize it using a webbrowser and jump between different sections of the song.

The result is this repo, which defines rules for song files and provides a script that can read those files and produce a pdf and html file from them.

An example can be found in this repo (`song_1.sf`). I define key-value pairs like title or author with the key and value separated by a colon (e.g. author: Niklas Hahn) and sections are introduced with square brackets (e.g. [Verse 1]). Everything is separated by new lines.

Example:
```
Title: Some Song Name  
Author: Some Artist
Date: Some date
...

[Intro]
A     Bm    C
Some  Song  Text

[Verse 1]
```

You can also define as many new sections as you want simply by putting them in the source `.sf` file as long as they have unique names. But I limited the available section names for song sections. This was simply because I needed to identify a song sections so that I could use some fixed-length font for the Chords and Text, so that the placement would not get moved around. If you want to introduce a new song section, simply add it to the `song_sections` list in the `parse` method. I for example add also the chord definitions at the top of the file like it is done at Ultimate Guitar:

```
[Chords]
A  |x-0-2-2-2-0|
C  |x-3-2-0-1-0|
```

## Install
To install you can simply get a copy of this repo:
```bash
> git clone https://github.com/NiklasDHahn/guitarsheet.git
```
(Optionally) create a virtual environment:
```bash
> python.exe -m venv .venv
```
Then you can simply install the requirements:
```bash
> pip install -r requirements.txt
```

## Run
To execute you just need to run the main script with the source file as input and an output directory. The name of the PDF and HTML files will be inferred from the song file.
```bash
> python.exe main.py song_.sf .
```