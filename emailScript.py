import smtplib, ssl, os, platform, praw, webbrowser, requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
#Gmail username devthrowaway0
#Gmail password throwawaythrowaway
sender_email = ""
password = ""
port = 465  #SSL
smtp_server = "" #"smtp.gmail.com"
message = MIMEMultipart("alternative")
message["Subject"] = "Daily Dose of Awesome"
platform = platform.system();
id = "PDjyla087HtZlA"
version = "1.0"
user = "DevThrowaway0"
agent = f"{platform}:{id}:{version} (by u/{user})"
secret = "QXagmo14R-X_wcopdYjKF6d5KUW6Gw"

def query_wikipedia():
    queryResult = []
    link = "https://en.wikipedia.org/wiki/Special:Random"
    request = requests.get(link)
    scraper = BeautifulSoup(request.content, "html.parser")
    title = scraper.find(class_= "firstHeading").text
    return f"https://en.wikipedia.org/wiki/{title}"

def htmlMessage():
    reddit = praw.Reddit(client_id=id,client_secret=secret,user_agent=agent)
    msg = "<p>Today, from TIL (via reddit.com)</p>"
    i = 1
    for top in reddit.subreddit("todayilearned").hot(limit=5):
        msg = msg + f"<a href='{top.url}'>{i}. {top.title}</a> <br>"
        i = i + 1

    article = query_wikipedia()
    msg = msg + f"<br><br><a href='{article}'>Click for a randomly generated wikipedia article!</a>"
    fullMessage = f"""\
    <html><body style="background-color:#fff0f5"><p>{msg}</p></body></html>
    """
    return fullMessage

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
    messageBody = htmlMessage()
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
message["From"] = sender_email
message["To"] = sender_email
sendEmailToClient()
    # TODO: add better exception handling
    # TODO: make program run on a daily schedule
    # TODO: make script run on startup
    # TODO: hide secret information and login information. Probably should've been done from the start but whatever.
