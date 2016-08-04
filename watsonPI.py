import sys
import requests
import json
import time
import operator
import twitter

from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights 

#This function is used to receive and analyze
#the last 200 tweets of a Twitter handle using
#the Watson PI API
def analyze(handle):

  #The Twitter API credentials
  twitter_consumer_key = 'aNBOL6jkf0smhi9VFpJiPVyo0'
  twitter_consumer_secret = 'VUshxjYJy7OqpT36HiAT4oZDLTN5IB5QAnWmB9c8jm1Af9XHST'
  twitter_access_token = '760397209250562048-bkqnceF3XE6jRHXlbNLzVOuK7ZANt0S'
  twitter_access_secret = 'NWJVAwiXi7ufi34ZycEk59lDjLrACE2bkVVNlKikaROYc'

  #Invoking the Twitter API
  twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                  consumer_secret=twitter_consumer_secret,
                  access_token_key=twitter_access_token,
                  access_token_secret=twitter_access_secret)

  #Retrieving the last 200 tweets from a user
  statuses = twitter_api.GetUserTimeline(screen_name=handle, count=500, include_rts=False)

  #Putting all 200 tweets into one large string called "text"
  text = "" 
  for s in statuses:
      if (s.lang =='en'):
          text += s.text.encode('utf-8')

  #Analyzing the 200 tweets with the Watson PI API
  pi_result = PersonalityInsights(username="4a843381-79f6-428a-a5b0-8c96b4118810", password="cUmBmwBZApio").profile(text)

  #Returning the Watson PI API results
  return pi_result

#This function is used to flatten the result 
#from the Watson PI API
def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data


#This function is used to compare the results from
#the Watson PI API
def compare(dict1, dict2):
  compared_data = {}
  for keys in dict1:
        if dict1[keys] != dict2[keys]:
          compared_data[keys] = abs(dict1[keys] - dict2[keys])
  return compared_data


#The two Twitter handles
user_handle = "@realDonaldTrump"
celebrity_handle = "@HillaryClinton" 
print("IBM Watson Personality Insight Analyzer\n")
#time.sleep(2)
print("Donald Trump v/s Hilary Clinton\n")
#time.sleep(2)
print("Top 5 features based on their last 500 tweets\n\n")
#Analyze the user's tweets using the Watson PI API
user_result = analyze(user_handle)
celebrity_result = analyze(celebrity_handle)

#Flatten the results received from the Watson PI API
user1 = flatten(user_result)
user2= flatten(celebrity_result)

#Compare the results of the Watson PI API by calculating
#the distance between traits
compared_results = compare(user1,user2)

#Sort the results
sorted_results = sorted(compared_results.items(), key=operator.itemgetter(1))

#Print the results to the user
print('{:^25}{:^20}{:^20}{:^20}\n'.format('Common Traits',user_handle,celebrity_handle,'Absolute Difference'))
for keys, value in sorted_results[:5]:
  print('{:^25}{:^20}{:^20}{:^20}'.format(keys,user1[keys],user2[keys],compared_results[keys]))
print('\n\n')
