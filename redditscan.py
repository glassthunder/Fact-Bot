import praw, os, platform

#bot account info for testing purposes. Should eventually be removed with authentication info stored in a .ini file.
#name: DevThrowaway0, password: throwawaythrowaway
name = os.name
platform = platform.system();
id = "PDjyla087HtZlA"
version = "1.0"
user = "DevThrowaway0"
agent = f"{platform}:{id}:{version} (by u/{user})"
secret = "QXagmo14R-X_wcopdYjKF6d5KUW6Gw"

reddit = praw.Reddit(
     client_id=id,
     client_secret=secret,
     user_agent=agent
 )


i = 1
#This needs be formatted into an email. prints to terminal right now for testing purposes
print("Today, from TIL (via reddit.com)")
for top in reddit.subreddit("todayilearned").hot(limit=10):
    print(f"{i}. {top.title}", end="\n")
    print(f"Accompanying link: {top.url}", end="\n\n")
    i = i + 1

# TODO: add exception handling
