from threading import Thread
import praw, pathlib
import urllib.request
from prawcore.exceptions import NotFound
import ujson
import time
import re

#Credit to django. https://github.com/django/django/blob/master/django/utils/text.py
def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)



def load_URLS():
    if pathlib.Path('downloaded_urls.json').exists():
        with open('downloaded_urls.json', 'r') as f:
            downloaded_urls = ujson.load(f)
        f.close()
        return downloaded_urls
    return []



class Media():
    EXTENSTIONS = ('jpeg', 'jpg', 'png', 'mp4')
    def __init__(self, praw_instance, list_of_users, user_to_annouce = None, short_URLs = False):
        if not list_of_users:
            print('empty list of users. Exits')
            raise SystemExit()
        if user_to_annouce and not type(user_to_annouce) == str:
            print('user_to_annouce must be a string.')
            raise SystemExit()


        self.praw_instance = praw_instance
        self.list_of_users = list_of_users
        self.URLS = load_URLS()
        self.user_to_annouce = user_to_annouce
        self.flag = False # a flag that changes to True whenever the URLs list is updated.
        self.short_URLs = short_URLs # a flag that if true, shortens the url strings to save space.


    def save_media(self, username):
        while True:
            try:
                print('looking for ' +username)
                for submission in self.praw_instance.redditor(username).stream.submissions():
                    t = Thread(target=self.save_media_thread, args=(submission, username))
                    t.start()
            except:
                print('servers must have failed, retries in 5 minutes')
                time.sleep(300)

    def save_media_thread(self, submission, username):
        url = submission.url
        if self.short_URLs:
            url_to_save = url.split('/')[-1]
        else:
            url_to_save = url

        if url.endswith(Media.EXTENSTIONS) and (url_to_save not in self.URLS):
            extension = '.' + url.split('.')[-1]
            title = get_valid_filename(submission.title) +' ' +username +extension
            self.URLS.append(url_to_save)
            self.flag = True
            path = pathlib.Path(username)
            path.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(submission.url ,path / title)
            print('{} | {}'.format(username, title))

            while self.user_to_annouce:
                try:
                    self.praw_instance.redditor(self.user_to_annouce).message(username + " uploaded new media", url)
                except Exception as e:
                    print(e)
                    time.sleep(240) # if there's a user and there's an exception, it's probably rate limit error.

                else:
                    break # if try is successful we can break the loop

    def save_urls(self):
        while True:
            time.sleep(10)
            if self.flag:
                with open('downloaded_urls.json', 'w') as  f:
                    ujson.dump(self.URLS, f,indent=4)
                f.close()
            self.flag = False


    def run(self):
        for user in self.list_of_users:
            try:
                self.praw_instance.redditor(user).id
                t = Thread(target=self.save_media, args=(user, ))
                t.start()
            except NotFound:
                print('user ' +user + " doesn't exist.")


        t = Thread(target=self.save_urls)
        t.start()

        print('all script functions have started successfully!')
