import openai
from decouple import config
import json
import tweepy
import time


# API Keys
API_KEY = config('API_KEY')
CONSUMER_KEY = config('CONSUMER_KEY')
CONSUMER_SECRET_KEY = config('CONSUMER_SECRET_KEY')
ACCESS_TOKEN = config('ACCESS_TOKEN')
SECRET_ACESS_TOKEN = config('SECRET_ACESS_TOKEN')
SESSION_TOKEN = config('SESSION_TOKEN')


# Initializations
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, SECRET_ACESS_TOKEN)
api = tweepy.API(auth)
openai.api_key = API_KEY

mention = {}

# Get Answer FROM OPENAI
def openaiAnswer(question):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{question}",
        temperature=0.9,
        max_tokens=1063,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    text = json.loads(json.dumps(response['choices']))[0]['text']
    return text


# Reply to Tweet/Mention
def replyTweet(id, replyMessage):
    api.update_status(status=replyMessage, in_reply_to_status_id=id,
                      auto_populate_reply_metadata=True)
    print(f'-------------Replying to {id}-----------------')


# Getting Tweet ID from the mentions
def getRecentMention():
    print('----------Retrieving Mention Id--------------')
    mention = api.mentions_timeline()[0]
    mention_id = mention.id
    original_tweet_id = mention.in_reply_to_status_id
    if original_tweet_id != None:
        original_tweet = api.get_status(original_tweet_id)
        return {
            'comment_mention': True,
            'mention_id': str(mention_id),
            'original_tweet_id': original_tweet_id,
            'original_tweet_text': original_tweet.text,
            'mention_text': mention.text,
            'original_tweet_url': f'https://twitter.com/{original_tweet.user.screen_name}/status/{original_tweet_id}'
        }
    else:
        return {
            'comment_mention': False,
            'mention_id': str(mention_id),
            'original_tweet_text':mention.text,
            'original_tweet_url': f'https://twitter.com/{mention.user.screen_name}/status/{mention_id}'
        }
    

def quoteTweet(tweeturl,message):
    api.update_status(message, attachment_url=tweeturl)


def writeInFile(id):
    with open('last_seen_id.txt','w') as f:
        f.write(id)


# Checking Last seen id to Current Mention Id , if they are same then no need to tweet
def main():
    recentMention = getRecentMention()
    message = recentMention['original_tweet_text'].replace("@asktorobo","") +'in short not more then 180 chracter'
    with open('last_seen_id.txt','r') as f:
        id = f.read()
        if str(id) != recentMention['mention_id']:
            if recentMention['comment_mention']:
                replyTweet(recentMention['mention_id'],openaiAnswer(message)[0:186])
            else:
                replyTweet(recentMention['mention_id'],openaiAnswer(message)[0:186])
            writeInFile(recentMention['mention_id'])


# Add a Web Hooks for more efficient API calls.

# while True:
#     time.sleep(15)
#     main()



