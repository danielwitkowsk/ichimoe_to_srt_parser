## ichimoe_to_srt_parser

Basic python webscraper that takes as an input .srt file and outputs .srt file with it's original content in the first line, traditional hepburn in the second, and english translation of seperate parts of the sentence in the third. For every caption a request is send to ichi.moe . 
Example caption input:

![image](https://user-images.githubusercontent.com/79915906/137600457-3c972811-cbad-41fc-9610-11b5422987e2.png)

Example output for this caption:

![image](https://user-images.githubusercontent.com/79915906/137600485-98c08b87-2df6-46e3-bf68-4881196bad46.png)

# Usage:

- install python and all necessary libraries:

`pip install pysrt`

`pip install requests`

`pip install re`

`pip install bs4`

- command:

`python script.py input_filename.srt output_filename.srt` 

# Subtitles aren't alligned vertically in your media player?
That's because kanji,kana symbols and normal characters have diffrent width sizes, and are fully dependent on the type of font you're using. Monospaced fonts seem to be the solution, and the only one that I found warking was "unifont_jp-14.0.01.ttf" from [here](http://unifoundry.com/unifont/index.html).

And [here](https://www.youtube.com/watch?v=c7eovFM-Bos) is how you can install font in VLC.

Unfortunately .srt is too basic of a file format to use custom font (in many cases).

# TODO:
- option to choose particular translation from many (now it takes the first one available)
- option to exclude translation and romanization of choosen kana (or kanji, if needed)

