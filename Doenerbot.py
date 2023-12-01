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
                     client_secret="your_client_secret",
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

