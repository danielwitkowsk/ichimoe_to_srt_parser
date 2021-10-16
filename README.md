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

# TODO:
- option to choose particular translation from many (now it takes the first one available)
- option to exclude translation and romanization of choosen kana (or kanji, if needed)
- figure out how to create output that, after being used in video player, will be alligned vertically (as seen in terminal, second picture)
