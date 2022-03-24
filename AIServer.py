import time
import sqlite3
import pandas as pd
import os
import cleverbotfree.cbfree
import sys



def chat(msg):
    cb = cleverbotfree.cbfree.Cleverbot()
    #userInput = input('User: ')
    txt = cb.single_exchange(msg)
    cb.browser.close()
    return txt
#inspired by:
#https://towardsdatascience.com/heres-how-you-can-access-your-entire-imessage-history-on-your-mac-f8878276c6e9

iMessageEmail = "huntersgordon@me.com"
iMessagePhone = "+18186215850"
activator = "ä" #must be 1 char

def removeQuotes(s):
    s = s.replace("'","")
    s = s.replace('"',"")
    s = s.replace("`","")
    s = s.strip("'").strip("`").strip('"')
    return s

def getRecentSender():
    #Thanks to 'linux sleuthing' for the idea of looking in the chat_message_join table
    #function returns guid if user is using imessage. else returns 0 for groupchats or SMS
    isFromMe = str(pd.read_sql_query("select is_from_me from message ORDER BY ROWID DESC limit 1",conn)['is_from_me'][0])
    print("is it from me?: " + isFromMe)
    #################### DELETE THESE LINES IF YOU WANT TO SEE OUTPUT IN SAME CHAT
    if (isFromMe == "1"):
        return iMessagePhone,1,isFromMe
    ####################
    is_Imessage = 0
    rowID = pd.read_sql_query("select ROWID from message ORDER BY ROWID DESC limit 1",conn)['ROWID'][0]
    chatID = pd.read_sql_query("select chat_id from chat_message_join where message_id={}".format(rowID),conn)["chat_id"][0]
    raw_phone_number = pd.read_sql_query("select guid from chat where ROWID={}".format(chatID),conn)["guid"][0]
    #################
    print("raw is:" + str(raw_phone_number))
    if ("chat" in raw_phone_number):
        #The last message received was in a groupchat, hence ignore
        #return "groupChat"
        is_Imessage = 3
        return 0,is_Imessage,isFromMe
    if(raw_phone_number[0:8] == "iMessage"):
        is_Imessage = 1
        phone_number=raw_phone_number[raw_phone_number.rindex(';')+1:]
    else:
        #It's an SMS
        phone_number=raw_phone_number[raw_phone_number.rindex(';')+1:]
        return phone_number,is_Imessage,isFromMe
    return phone_number,is_Imessage,isFromMe

conn = sqlite3.connect('/Users/Hunter/Library/Messages/chat.db') #or your username
cur = conn.cursor()
last = pd.read_sql_query("select text from message ORDER BY ROWID DESC limit 1",conn)['text'][0]

lastAiChat = ""
while(True):
    new = pd.read_sql_query("select text from message ORDER BY ROWID DESC limit 1",conn)['text'][0]
    if (new!=last):
        #from =
        print("text: " + new)
        senderObj = getRecentSender()
        sender = senderObj[0]
        is_Imessage = senderObj[1]
        isFromMe = senderObj[2]
        print("most recent text from: " + str(sender))
        last = new
        #########################~~~~CUSTOM FUNCTIONS~~~~###################################
        if (new == "clear" and isFromMe == "1"):
            print("lets do it")
            os.system("python3 clearChat.py +18186215850 huntersgordon@me.com")
        if (new == "facetime me bro"):
            os.system("python3 facetime.py")
        #######################~~~~CUSTOM FUNCTIONS~~~~#####################################
        if(isFromMe!="1" and sender != 0 or ((new[0] == activator) and sender != 0)): #control computer if it's from me, or if a friend has sent the activating key, and it's not a groupchat

            #to run messages thru terminal:
            #  response = os.popen(new[1:]).read()[:-1] #get output of command and exclude the return character
            print("lets go")
            #to be impersonated by an AI:
            #response = str(chat(new[1:]))
            response = str(chat(new)).lower()[:-1]
            lastAiChat = response

            if (response != ""): #if there is output, then send it back. terminal style
                response = removeQuotes(response)
                if(is_Imessage == 0):
                    response2 = 'osascript -e \'tell application "Messages" \n send \"' + response + '\" to buddy "{}" of service "SMS" \n end tell\''.format(sender)
                else:
                    response2 = 'osascript -e \'tell application "Messages" \n send \"' + response + '\" to buddy "{}" of service "E:{}" \n end tell\''.format(sender,iMessageEmail)
                os.system(response2)
    time.sleep(0.5) #or a desired resolution
