import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Gmail username devthrowaway0
#Gmail password throwawaythrowaway
port = 465  #SSL
smtp_server = "smtp.gmail.com"
sender_email = input("Your email: ")
password = input("password: ")

message = MIMEMultipart("alternative")
message["Subject"] = "Daily Dose of Awesome"
message["From"] = sender_email
message["To"] = sender_email
messageBody = f"""\
<html>
  <body style="background-color:#fff0f5">
    <p>
       <a href="https://www.reddit.com/r/todayilearned/">Links to TIL will go here as well as wikipedia and maybe more</a>
    </p>
  </body>
</html>
"""
messageAsHTML = MIMEText(messageBody, "html")
message.attach(messageAsHTML)
context = ssl.create_default_context()
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, sender_email, message.as_string())
except Exception as e:
    print("Could not authenticate sender")
