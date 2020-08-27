"""This version is old AND WILL NOT BE UPDATED OT SUPPORTED. pleae use newer version"""


import praw, urllib.request, time, threading, pickle, pathlib


#Enter reddit credentials
r = praw.Reddit(username="",
    password="",
    client_id="",
    client_secret="",
    user_agent="")


#Subs that you want the script to follow. Notice that this is a list and infinite names (or just one name) can be entered
USERS_TO_FOLLOW = ["USER1", "USER2"]

#User that you want to notify whenever new media is posted
USER_TO_ANNOUCE = "USER3"

#Supported extensions. You can add more extenstions but than the bot is not guranteed to work.
EXTENSIONS = ('jpeg', 'jpg', 'png')

#If the script can't find an existing file of urls, it will create one.
if not pathlib.Path('downloaded_urls.pkl').exists():
    with open('downloaded_urls.pkl', 'wb') as f:
        pickle.dump([], f)


#Loads the file of urls as a variable
with open('downloaded_urls.pkl', 'rb') as f:
    downloaded_urls = pickle.load(f)


"""Saves the URLs to a pickle file. I decided to use this as a pickle file because I don't need to know which
URLs have been saved (as they can often change). In addition, this script downloades the media from those URLs
so I really don't need any access to those URLs. 

#The only reason we save those URLs is so the script would ignore any multiple posts of the same URL. """
def save_to_txt():
    global downloaded_urls
    print(downloaded_urls)
    with open('downloaded_urls.pkl', 'wb') as f:
        pickle.dump(downloaded_urls, f)

#That part is pretty much self explainatory. Retrieves media, saves it, and prints out the details about the saved file.
def main(user_to_follow):
    global downloaded_urls
    while True:
        try:
            for submission in r.redditor(user_to_follow).stream.submissions():
                url = submission.url
                if url.endswith(EXTENSIONS) and url not in downloaded_urls:
                    extension = url.split('.')[-1]
                    #Title would consist only valid chars in enlgish and backspaces
                    title = ''.join(e for e in submission.title if e.isalnum() or e == ' ')
                    urllib.request.urlretrieve(url, '{}.{}'.format(title, extension))
                    print("Title: {} | User: {}".format(title, user_to_follow))
                    downloaded_urls.append(url)
                    r.redditor(USER_TO_ANNOUCE).message(user_to_follow + " uploaded new media", url)
        except Exception as e:
            print(e)
            print('servers must have failed, retries in 5 minutes')
            time.sleep(300)


if __name__ == "__main__":

    """Because we want the script to be able to search for media from more than ONE user, we'll use
    threads which allow us to spawm multiple instances of the same function concurrently"""
    for user in USERS_TO_FOLLOW:
        t = threading.Thread(target=main, args=(user, ))
        t.start()

    #While the threads are running, we will save the new URLs that were found, every ten seconds.
    while True:
        save_to_txt()
        time.sleep(10)
