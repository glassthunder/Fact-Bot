import smtplib, ssl, os, platform, praw, webbrowser, requests, time, schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
userEmail = ""
password = ""
port = 465  #Default Gmail SSL port
smtp_server = ""
message = MIMEMultipart("alternative")
message["Subject"] = "Daily Dose of Awesome"
platform = platform.system();
id = os.environ.get("REDID")
version = "1.0"
user = os.environ.get("REDUSER")
agent = f"{platform}:{id}:{version} (by u/{user})"
secret = os.environ.get("REDSECRET")

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
    global userEmail
    global password
    global smtp_server
    try:
        file = open("./config.txt", 'r')
        for i, current in enumerate(file):
            line = current.strip()
            if len(line) == 0:
                raise IOError
            if i == 0:
                userEmail = line
                continue
            if i == 1:
                password = line
                continue
            if i == 2:
                smtp_server = line
                continue
            if i == 3:
                port = int(line)
                file.close()
                break;
    except (FileNotFoundError, IOError) as e:
        print("It seems a config file does not exist. Let's create one.")
        file = open("./config.txt", 'w')
        userEmail = input("Your email: ")
        password = input("Password (which is stored on your machine and only accessible by you): ")
        smtp_server = input("Your mail server address, ex: smtp.gmail.com (a lookup might be required): ")
        port = eval(input("Lastly, your mail server's ssl port (Gmail default is 465) : "))
        file.write(f"{userEmail}\n{password}\n{smtp_server}\n{port}")
        print(f"Config file complete! Make sure to keep this file safe as it contains private information.")
        file.close()
    except Exception as e:
        print("An unexpected error occured")

def sendEmailToClient():
    messageBody = htmlMessage()
    messageAsHTML = MIMEText(messageBody, "html")
    message.attach(messageAsHTML)
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(userEmail, password)
            server.sendmail(userEmail, userEmail, message.as_string())
            print("Email sent!")
    except (smtplib.SMTPSenderRefused, smtplib.SMTPRecipientsRefused, smtplib.SMTPDataError) as e:
        print("Message was refused.")
    except  smtplib.SMTPConnectError as e:
        print("Connection could not be established.")
    except smtplib.SMTPAuthenticationError as e:
        print("Could not authenicate.")
    except smtplib.SMTPException as e:
        print("An unexpected error occured")

init()
message["From"] = userEmail
message["To"] = userEmail
schedule.every().day.at("06:00").do(sendEmailToClient)
if __name__ == "__main__":
    while True:
        schedule.run_pending()
