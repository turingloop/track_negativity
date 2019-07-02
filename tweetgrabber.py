import tweepy
import csv
import time

#twitter authorization
from twitter_keys import consumer_key, consumer_secret, access_token, access_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def get_all_tweets(screen_name):
    #counter to keep track of requests to avoid time out
    counter = 0
    #initialize a list to hold all the tweepy Tweets
    alltweets = [] 
    #make initial request for most recent tweets
    new_tweets = api.user_timeline(screen_name = screen_name ,count=200) 
    #save most recent tweets
    alltweets.extend(new_tweets)
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1   
    #keep grabbing tweets
    while len(new_tweets) > 0:        
        #waits for 30 min after 10 requests
        if counter == 10:
            time.sleep(1800)
            counter = 0       
        #this prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        counter = counter + 1        
        #save most recent tweets
        alltweets.extend(new_tweets)
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1   
    #transform the tweepy tweets into a 2D array that will populate the csv	
    tweetarray = [[tweet.source, tweet.text.encode("utf-8"), tweet.created_at, tweet.retweet_count, tweet.favorite_count, tweet.id_str] for tweet in alltweets]    
    #write the csv
    with open('tweetstore_2014_2019.txt', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["source","text","created_at","retweet_count","favorite_count","is_retweet","id_str"])
        writer.writerows(tweetarray)    
    pass
    

