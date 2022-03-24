###Process Commands and send back output
#import sendMessage
import SongDownloader
import os,signal
import sys
from credentials import iMessageEmail,iMessagePhone
from MessageListener import getMostRecentText
import time
from imageToText import isAttachment,PrintImageAttachment
from terminal import term
from SongDownloader import removeQuotes

def processResponse(message,isItFromMe,sender,conn):
    #########################~~~~PLACE YOUR CUSTOM FUNCTIONS HERE~~~~#########################
    if isAttachment(conn):
        pid=os.fork()
        if pid==0: #child process
            print('processing image')
            PrintImageAttachment(conn,sender)
            sys.exit("child process terminated")
    if(message == "exit" and isItFromMe):
        #sendMessage.messageSend("goodbye...",sender)
        exit()
    if (str.lower(message[0:4]) == "song"):
            pid=os.fork()
            if pid == 0 : #child process
                SongDownloader.songGetter(message,sender)
                sys.exit("child process terminated")

    if (str.lower(message) == "clear" and isItFromMe):
            os.system("python3 clearChat.py {} {}".format(iMessagePhone,iMessageEmail))
    if message[0] == "ä":
        term(message,sender,iMessageEmail)
    if (str.lower(message[0:7].lower()) == "picture"):
        os.system('cd Image-Downloader; python3 image_downloader.py --engine "Google" --driver "chrome_headless" --max-number 1 --output "folder" "{}"'.format(message[8:]))
        os.system("osascript sendPicture.scpt \"{}\"".format(sender))
    if (str.lower(message[0:6]) == "lyrics"):
        os.system("lyrics {}".format(message[7:]))
        results = os.popen("lyrics \"{}\"".format(message[7:])).read()[:-1]
        f = open("response.txt", "w")
        f.write(results)
        f.close()
        os.system("osascript sendtxt.scpt \"{}\"".format(sender))
        inform = 'osascript -e \'tell application "Messages" \n send \"complete.\" to buddy "{}" of service "E:{}" \n end tell\''.format(sender,iMessageEmail)
        os.system(inform)
