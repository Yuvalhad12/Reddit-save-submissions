# Save Reddit's User's Submission media

That script would save submission's media (currently only photos) from multiple users cocurrently. In addition, it alerts the user whenever media was found \ saved.


Basically, the script is very simple, and all the user has to do is enter the REDDIT USERS he wants the script to follow, and the REDDIT USER he wants to notify whenever media is found.

The script is super simple and highly self-explainatory, but if you need any help understanding it, feel free to tell me.

# THE LATEST VERSION IS ALWAYS IN "MAINVERSION"

# changelog in V2:
1. Moved to a more conventional OOP-based coding.
2. The script tests by itself what is a valid user (redditor) and what's not (In case the user inputs usernames by himself).
3. Photos are now seperated to folders, every folder is the username's name.
4. using UJSON module as it's faster than the regular json module (according to the devs).
5. APPENDING LINKS TO JSON FILE now happens more often and more smart - the script will check if there are changes to the url string before overwriting the json file itself.
6. Added option to write shortened links to the json file to save space and time
7. The script itself now runs in threads (Thus, the main thread is not occupied by the package objects.)
