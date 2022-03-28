import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image
import pandas as pd
import os
from credentials import iMessageEmail,iMessagePhone
import numpy as np
import sys

def PrintImageAttachment(conn,sender):
     try:
         filename = str(pd.read_sql_query("select filename from attachment ORDER BY ROWID DESC limit 1", conn)['filename'][0])
         os.system("cp {} test.png".format(filename))
         #print(filename)
         img = Image.open("test.png")
         text = pytesseract.image_to_string(img)
         if len(text) < 10:
             exit()
         print(text)
         f = open("response.txt", "w")
         f.write(text)
         f.close()
         os.system("osascript sendtxt.scpt \"{}\"".format(sender))
         inform = 'osascript -e \'tell application "Messages" \n send \"Image to text complete.\" to buddy "{}" of service "E:{}" \n end tell\''.format(sender,iMessageEmail)
         os.system(inform)
     except Exception as e:
         print("image conversion failed")
         print(e)
         sys.exit(1)

def isAttachment(conn):
     return bool(pd.read_sql_query("select cache_has_attachments from message ORDER BY ROWID DESC limit 1", conn)["cache_has_attachments"][0])
