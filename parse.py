import pysrt
import requests
import re
from bs4 import BeautifulSoup
import os

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    
def pad(strings):#"strings" contain 3 strings seen as one column seperated by "|" in terminal
    lengths=[2*len(strings[0]),len(strings[1]),len(strings[2])]#japanese/chinese chars are multiplied by 2
    max_len=max(lengths)
    for i in range(len(lengths)):
        if lengths[i] < max_len:
            diff_len = max_len-lengths[i]
            append_spaces=(int)(diff_len/2)
            #below I add spaces so that they are alligned, this works in terminal, 
            #not in video player with loaded srt
            strings[i] = " "*append_spaces + strings[i] + " "*append_spaces + " "*(diff_len%2)
    return strings
    
def parse_srt():
    all_kana=[]      
    all_kana_kanji=[]
    all_defs=[]
    subs=None
    while subs is None:
        try:
            input_file = input("Enter input filename (with .srt): ")
            subs = pysrt.open(input_file)
        except:
            print("Wrong filename")

    for sub_index in range(len(subs)):
        clearConsole()
        print("Processing: " + str(sub_index) + " of " + str(len(subs)))
        r = requests.get("https://ichi.moe/cl/qr/?q=" + subs[sub_index].text + "&r=hb")
        divs_ids = re.findall("g-\d-0-\d", r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        divs=[]
        kana=[]
        kana_kanji=[]
        defs=[]
        #find divs
        for x in divs_ids:
            divs += soup.find("div", {"id": x})

        #find pronunciation in every div    
        for x in divs:
            try:
                y = re.search(r'<em>(.*?)</em>', str(x)).group(1)
                kana.append(y)
            except:
                pass  
                
        #find kana,kanji in every in div
        for x in divs:
            try:
                y = re.findall(r'<dt>(.*?)</dt>', str(x))
                modified_kana_kanji=[]
                for z in y:
                    z = re.sub(r'\d. ','',z) #remove "1. ", "2. " etc.
                    #z = z.split(" ", 1)[0] #remove from kanji to kana in brackets
                    modified_kana_kanji.append(z)
                kana_kanji.append(modified_kana_kanji)
            except:
                pass
        kana_kanji = list(filter(None,kana_kanji))

        #find definitions in every div
        for x in divs:
            try:
                y = re.findall(r'<dd>(.*?)</dd>', str(x))
                y = list(filter(None,y))
                grouped_defs=[]
                for z in y:
                    descriptions = re.findall(r'<span class="gloss-desc">(.*?)</span>', str(z))#distinct between definitions
                    splitted=[]
                    for description in descriptions:
                        splitted.append(#split descriptions
                        (description.split("; ")))
                    if splitted:
                        grouped_defs.append(splitted)
                    else:
                        grouped_defs.append(" ")
                defs.append(grouped_defs)
            except:
                pass
        defs = list(filter(None,defs))
        
        all_kana.append(kana)   
        all_kana_kanji.append(kana_kanji)
        all_defs.append(defs)
    return all_kana, all_kana_kanji, all_defs, len(subs), subs