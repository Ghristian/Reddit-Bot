#Um einen Reddit-Bot zu erstellen, müssen Sie einige Schritte befolgen:

#1.Überprüfen Sie die Reddit API-Dokumentation und folgen Sie den Zugriffsregeln, um nicht gesperrt zu werden.
#   https://yojji.io/blog/how-to-make-a-reddit-bot

#2.Erstellen Sie eine Anwendung auf Reddit und erhalten Sie die Client-ID und das Geheimnis.
#   https://bing.com/search?q=how+to+create+a+reddit+bot

#3.Richten Sie ein repl.it-Konto ein und erstellen Sie ein neues Python-Projekt.
#   https://medium.com/analytics-vidhya/a-comprehensive-guide-to-creating-a-basic-reddit-bot-part-1-15fb0e4cebcb

#4.Schreiben Sie ein Skript mit der PRAW-Bibliothek, um mit der Reddit API zu interagieren.
#   https://www.tripsavvy.com/all-about-the-wurst-currywurst-1519692

#5.Führen Sie Ihren Bot auf repl.it aus und testen Sie ihn.
#   https://bing.com/search?q=average+price+of+currywurst+in+Germany


#How to run Bot on Raspberry Pi 2
   #https://www.reddit.com/r/raspberry_pi/comments/6b7sh1/got_my_reddit_bot_running_on_my_pi_2/
   #https://www.reddit.com/r/redditdev/comments/23j5od/hosting_a_bot_on_a_raspberry_pi/


#Now the Programm
# Import the PRAW library
import praw
import re

# Create a Reddit instance with your credentials
reddit = praw.Reddit(client_id="your_client_id",
                     client_secret="YdtyFyNY3RTHD1TX5Mz5gDX-VteWEg",
                     user_agent="your_user_agent",
                     username="your_username",
                     password="your_password")

# Define the subreddit you want to monitor
subreddit = reddit.subreddit("your_subreddit")

# Define the regex pattern to match amounts in euro
pattern = r"\b\d+(?:[.,]\d+)?\s*€\b"

# Define the average price of a currywurst in euro
price = 3.5

# Define a function to convert euro to currywurst
def euro_to_currywurst(euro):
    # Convert the euro string to a float
    euro = euro.replace(",", ".")
    euro = float(euro)
    # Calculate the number of currywurst
    currywurst = euro / price
    # Round the number to the nearest integer
    currywurst = round(currywurst)
    # Return the number as a string
    return str(currywurst)

# Define a function to convert euro to currywurst
def euro_to_doener(euro):
    # Convert the euro string to a float
    euro = euro.replace(",", ".")
    euro = float(euro)
    # Calculate the number of doener
    doener = euro / price
    # Round the number to the nearest integer
    doener = round(currywurst)
    # Return the number as a string
    return str(doener)
  
# Stream the comments from the subreddit
for comment in subreddit.stream.comments():
    # Check if the comment contains an amount in euro
    match = re.search(pattern, comment.body)
    if match:
        # Extract the amount from the match object
        amount = match.group()
        # Remove the euro symbol
        amount = amount.replace("€", "")
        # Convert the amount to currywurst
        currywurst = euro_to_currywurst(amount)
        #Convert the amount to doener
        doener = euro_to_doener(amount)
        # Generate a reply message
        reply = f"Für {amount} € könntest du {currywurst} Currywürste oder {doener} Döner kaufen."
        # Reply to the comment
        comment.reply(reply)
        # Print the reply for debugging
        print(reply)


#Added Bot Etiquette from https://github.com/acini/praw-antiabuse-functions/blob/master/anti-abuse.py

import collections, praw

#This is simple collection of functions to prevent reddit bots from:
#1. replying twice to same summon
#2. prevent chain of summons
#3. have limit on number of replies per submission

#Note: See TODO and make according changes
#Note: You can use reply function like this: post_reply(comment-content,praw-comment-object)
#Note: is_summon_chain returns True if grandparent comment is bot's own
#Note: comment_limit_reached returns True if current will be 5th reply in same thread, resets on process restart
#Note: don't forget to decalre `submissioncount = collections.Counter()` before starting your main loop
#Note: Here, r = praw.Reddit('unique client identifier')

def is_summon_chain(post):
  if not post.is_root:
    parent_comment_id = post.parent_id
    parent_comment = r.get_info(thing_id=parent_comment_id)
    if parent_comment.author != None and str(parent_comment.author.name) == 'bot_username': #TODO put your bot username here
      return True
    else:
      return False
  else:
    return False
  
def comment_limit_reached(post):
  global submissioncount
  count_of_this = int(float(submissioncount[str(post.submission.id)]))
  if count_of_this > 4: #TODO change the number accordingly. float("inf") for infinite (Caution!)
    return True
  else:
    return False
  
def is_already_done(post):
  done = False
  numofr = 0
  try:
    repliesarray = post.replies
    numofr = len(list(repliesarray))
  except:
    pass
  if numofr != 0:
    for repl in post.replies:
      if repl.author != None and repl.author.name == 'bot_username': #TODO put your bot username here
	done = True
	continue
  if done:
    return True
  else:
    return False

def post_reply(reply,post):
  global submissioncount
  try:
    a = post.reply(reply)
    submissioncount[str(post.submission.id)]+=1
    return True
  except Exception as e:
    warn("REPLY FAILED: %s @ %s"%(e,post.subreddit))
    if str(e) == '403 Client Error: Forbidden':
      print '/r/'+post.subreddit+' has banned me.'
      save_changing_variables()
    return False

submissioncount = collections.Counter()
