import smtplib, ssl, os, platform
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Gmail username devthrowaway0
#Gmail password throwawaythrowaway
sender_email = ""
password = ""
port = 465  #SSL
smtp_server = "" #"smtp.gmail.com"



def init():
    global sender_email
    global password
    global smtp_server
    try:
        file = open("./config.txt", 'r') #should probably put this one directory back after we package python files
        for i, current in enumerate(file):
            line = current.strip()
            if len(line) == 0:
                raise IOError
            if i == 0:
                sender_email = line
                continue
            if i == 1:
                password = line
                continue
            if i == 2:
                smtp_server = line
                file.close()
                break;
            else:
                raise IOError

    except (FileNotFoundError, IOError) as e:
        print("It seems a config file does not exist. Let's create one.")
        file = open("./config.txt", 'w')
        sender_email = input("Your email: ")
        password = input("Password (which is stored on your machine and only accessible by you): ")
        smtp_server = input("Lastly, your mail server (a lookup might be required): ")
        file.write(f"{sender_email}\n{password}\n{smtp_server}")
        print(f"Config file complete! Make sure to keep this file safe as it contains private information.")
        file.close()


def sendEmailToClient(): #will later take links generated from wikipedia and reddit as input
    messageAsHTML = MIMEText(messageBody, "html")
    message.attach(messageAsHTML)
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, sender_email, message.as_string())
            print("Email sent")
    except Exception as e:
        print("Could not authenticate sender")
        print(f"{sender_email}\n{password}\n{smtp_server}")
init()
message = MIMEMultipart("alternative")
message["Subject"] = "Daily Dose of Awesome"
message["From"] = sender_email
message["To"] = sender_email
messageBody = f"""\
<html>
  <body style="background-color:#fff0f5">
    <p>
       <a href="https://www.reddit.com/r/todayilearned/">
        Links to TIL will go here as well as wikipedia and maybe more
       </a>
    </p>
  </body>
</html>
"""
sendEmailToClient()
    # TODO: add better exception handling
    # TODO: remember the really important thing you said you wouldn't forget but did
