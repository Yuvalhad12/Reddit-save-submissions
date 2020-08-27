from media import praw, time, Media
#No need to import praw seperately as it's already inside media package

#Initializing a praw instance.
#I chose to initialize the instance seperatley so the main script could use it as well.
r = praw.Reddit(username="",
    password="",
    client_id="",
    client_secret="",
    user_agent="")



user_to_annouce = 'yuvalhad12' #User to send the messages about the new links to 
users_to_save = [submission.author.name for submission in r.subreddit('pics').new(limit=100)] ##That's why we initialize our praw instance in the main thread and not in the package.


script = Media(praw_instance=r, list_of_users=users_to_save, user_to_annouce=user_to_annouce, short_URLs=True) #By default, short_URLs is false. Pass True only if you want the option to work
#short_URLs basically saves the url of the image without the domain to save space.
# You don't have to pass a user_to_annouce (It just won't annouce)


"""Because I don't want to annouce to my own user at least 100 submission of photos, I will create a new instance without a user to annouce to."""

script = Media(praw_instance=r, list_of_users=users_to_save, short_URLs=True)

script.run() #Starts the threads

#also don't need to import the time module as it's already in media package
time.sleep(10)
print('THE REST OF THE CODE CAN RUN WITHOUT A PROBLEM AS MEDIA IS USING THREADS') #that message will be printed after 10 seconds AFTER ININTIALIZING THE SCRIPT IS FINISHED


script.save_media('yuvalhad12') #If we want to add more users to search for their media, we can do it. (Will create a thread so the rest of the script could also run without a problem)