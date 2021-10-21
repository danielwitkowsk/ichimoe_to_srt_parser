import sys
import parse
import os
import pysrt
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clearConsole()

def inputCheck(variable, min_val, max_val):
    print()
    while True:
        try:
            variable = int(input("Choose: "))
            if variable < min_val or variable > max_val:
                raise ValueError()
        except ValueError:
            print("Wrong value, try again")
            continue
        break
    return variable
    
def flatten(seq):
    l = []
    for elt in seq:
        t = type(elt)
        if t is tuple or t is list:
            for elt2 in flatten(elt):
                l.append(elt2)
        else:
            l.append(elt)
    return l
    
def pad(strings):#"strings" contain 3 strings seen as one column seperated by "|" in terminal
    lengths=[2*len(strings[0])-strings[0].count(' '),len(strings[1]),len(strings[2])]#japanese/chinese chars are multiplied by 2
    max_len=max(lengths)
    for i in range(len(lengths)):
        if lengths[i] < max_len:
            diff_len = max_len-lengths[i]
            append_spaces=(int)(diff_len/2)
            strings[i] = " "*append_spaces + strings[i] + " "*append_spaces + " "*(diff_len%2)
    return strings

hepburn,kana_kanji,defs,num_of_captions,subs=parse.parse_srt()
num_of_captions=len(subs)
current_kana=[]
current_hepburn=[]
current_defs=[]
current_sub=[]

def editOne(which,id,choice,changed):
    res1,res2,res3=("|",)*3
    for i in range(len(kana_kanji)):
        if i==choice and which=="top":
            top=changed
            current_kana[id][i]=top
        else:
            top=current_kana[id][i]
            
        mid=current_hepburn[id][i]
        
        if i==choice and which=="bot":
            bot=changed
            current_defs[id][i]=bot
        else:
            bot=current_defs[id][i]
        [top,mid,bot] = pad([top,mid,bot])
        res1 += top+"|"
        res2 += mid+"|"
        res3 += bot+"|"
    current_sub[id]=(res1+"\n"+res2+"\n"+res3)
    
for index in range(num_of_captions):
    res1,res2,res3=("|",)*3
    current_kana.append([])
    current_hepburn.append([])
    current_defs.append([])
    for i in range(len(kana_kanji)):
        top=kana_kanji[index][i][0]
        mid=hepburn[index][i]
        bot=defs[index][i][0][0][0]
        current_kana[-1].append(top)
        current_hepburn[-1].append(mid)
        current_defs[-1].append(bot)
        [top,mid,bot] = pad([top,mid,bot])
        res1 += top+"|"
        res2 += mid+"|"
        res3 += bot+"|"
    current_sub.append(res1+"\n"+res2+"\n"+res3)
    
def editCaption(id):
    showOne(id)
    print()
    print("What to edit?")
    print("1. Japanese in subtitle")
    print("2. Translation in subtitle")
    print("3. Go next")
    print("4. Exit to main screen")
    choice=-1
    choice=inputCheck(choice,1,4)
    clearConsole()
    if choice==1:#japanese
        clearConsole()
        print("Choose which part of sentence to change:")
        for option in range(len(current_kana[id])):
            print(str(option+1),". ",str(current_kana[id][option]))
        choice=-1
        choice=inputCheck(choice,1,len(current_kana[id])+1)-1
        clearConsole()
        print("Choose to change:")
        for option in range(len(kana_kanji[id][choice])):
            print(str(option+1),". ",str(kana_kanji[id][choice][option]))
        choice2=-1
        choice2=inputCheck(choice2,1,len(kana_kanji[id][choice])+1)-1
        to_change=kana_kanji[id][choice][choice2]#choosen word
        if " " in to_change:
            print("Remove brackets?")
            print("1.Yes    2.No")
            brackets=-1
            brackets=inputCheck(brackets,1,2)
            if brackets==1:
                to_change = to_change.split(" ", 1)[0].strip()
        editOne("top",id,choice,to_change)
        clearConsole()
    elif choice==2:
        clearConsole()
        print("Choose to change:")
        for option in range(len(current_defs[id])):
            print(str(option+1),". ",str(current_defs[id][option]))
        choice=-1
        choice=inputCheck(choice,1,len(current_defs[id])+1)-1
        clearConsole()
        print("Choose to change:")
        all_defs=flatten(defs[id][choice])
        for option in range(len(all_defs)):
            print(str(option+1),". ",str(all_defs[option]))
        choice2=-1
        choice2=inputCheck(choice2,1,len(all_defs)+1)-1
        to_change=all_defs[choice2]
        if "(" in to_change:
            print("Remove brackets?")
            print("1.Yes    2.No")
            print()
            brackets=-1
            brackets=inputCheck(brackets,1,2)
            if brackets==1:
                to_change = to_change.split("(", 1)[0][:-1].strip()
        editOne("bot",id,choice,to_change)
    elif choice==3:
        clearConsole()
        return
    elif choice==4:
        clearConsole()
        entryScreen()
        
        
def showOne(id):
    curr_str=current_sub[id].splitlines()
    print(" "*5,curr_str[0])
    print("{:<5} {:>20}".format(*[str(id),curr_str[1]]))
    print(" "*5,curr_str[2])
    
def showCurrent(scope, id):
    print("{:<5} {:>20}".format(*["Index |","Caption"]))
    print("-"*100)
    if scope:
        for index in range(id,num_of_captions):
            showOne(index)
            print("-"*100)
    else:
        for index in id:
            showOne(index)
            print("-"*100)
    choice = input("Type in 'exit' to exit or indexes of captions you want to edit and press enter:")
    clearConsole()
    if choice.lower()=='exit':
        operations(99)
    else:
        indexes = list(map(int,choice.split(' ')))
        for id in indexes:
            editCaption(id)
        clearConsole()
        entryScreen()
        
def entryScreen():
    print("1. Show current translation")
    print("2. Edit captions numbered... (1 or more)")
    print("3. Edit captions starting from...")
    print("4. Save to file\n")
    choice=-1
    choice=inputCheck(choice,1,4)
    operations(choice)
    
def operations(choice):
    clearConsole()
    if choice==1:
        showCurrent(True,0)
    elif choice==2:
        print("Input indexes(space between every index) and press enter:")
        ids = input()
        indexes = list(map(int,ids.split(' ')))
        for id in indexes:
            editCaption(id)
        clearConsole()
        entryScreen()
    elif choice==3:
        print("Index to start from:")
        id = int(input())
        for i in range(id,num_of_captions):
            editCaption(i)
        clearConsole()
        entryScreen()
    elif choice==4:
        for id in range(len(subs)):
            subs[id].text=current_sub[id]
        output=input("Enter output filename (with .srt): ")
        subs.save(str(output), encoding='utf-8')
        print("Saved to ",str(output))
    else:
        entryScreen()
entryScreen()
#
#print(parse.parse_srt(input))