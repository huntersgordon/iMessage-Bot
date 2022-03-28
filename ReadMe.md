iMessage-bot is a modularly designed & customizable chatbot engine intended for receiving, processing, and sending back text messages on Mac OS.

Written in Python, AppleScript, and NodeJS, iMessage-bot communicates with chat.db using a pandas SQL query to read the last received message in real-time. 

Configuration:

***Important:*** you must [disable SIP](https://developer.apple.com/documentation/security/disabling_and_enabling_system_integrity_protection) on your machine in order to begin. This is because chat.db is a protected file on Mac OS. 

In addition, in ***credentials.py***, add your registered iMessage email and [phone number in the E.164 Format](https://blog.insycle.com/phone-number-formatting-crm#E164)

eg:
```iMessageEmail = "john@example.com"
   iMessagePhone = "+15654445593"
```

To start processing text:

```python3 start.py```

There are many other features included with my bot, such as:
1. song search and downloading via YouTube-DL
-texting someone running the bot the word "song", followed by a song name will send back Youtube results in iMessage;
subsequently, the recipient is prompted to send back a number index of the desired song, and receives a downloaded song back

2. image to text
- Images sent to the account running the bot are transcribed using open-source OCR using python's Pillow image processing library

3. Command line interaction via text message
 - iMessage-bot is designed to give you more power in your text messages through enabling command-line interaction through your text message system. 
 - In command process, 'ä' is the default character used to trigger command line interaction for text users. e.g. texting the bot ```ä echo hello``` will text back the word hello.

4. File retrieval via text message
 - Seamlessly communicate with your filesystem remotely by querying iMessage-bot via the aforementioned command-line interaction system.
