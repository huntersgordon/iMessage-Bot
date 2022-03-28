import subprocess
import os
#to run messages thru terminal:

def removeQuotes(s):
    s = str(s)
    s = s.replace("'","")
    s = s.replace('"',"")
    s = s.replace("`","")
    s = s.strip("'").strip("`").strip('"')
    return s
    
def term(message,sender,iMessageEmail):
    response = ""

    p = subprocess.Popen(message[1:],shell=True) #get output of command
    stdout, stderr = p.communicate()
    if(stdout):
        try:
            response = stdout.decode('ascii') # [-1] excludes the return character
        except:
            response = "There was an error."
    else:
        try:
            response = stderr.decode('ascii')
        except:
            response = "There was an error."
    #print("lets go")

    if (response != ""): #if there is output, then send it back. terminal style
        response = removeQuotes(response)
        if(is_Imessage == 0):
            response2 = 'osascript -e \'tell application "Messages" \n send \"' + response + '\" to buddy "{}" of service "SMS" \n end tell\''.format(sender)
        else:
            response2 = 'osascript -e \'tell application "Messages" \n send \"' + response + '\" to buddy "{}" of service "E:{}" \n end tell\''.format(sender,iMessageEmail)
        os.system(response2)
