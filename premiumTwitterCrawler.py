#Documentation for searchtweetsAPI pypi.org/project/searchtweets/
# https://twitterdev.github.io/tweet_parser/tweet_parser.html#tweet_parser.tweet.Tweet  -  Returned tweet object fields
from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
import csv

def getHeaders():
	header = ["Keyword", "User", "Screen Name", "Tweet ID", "Created At", "Tweet Type", "Tweet Text", "Retweet Count", "Favorite Count", "Language", "Geo Coordinates", "Profile Location"]
	return header

def getResults(keyword, username, screenName, tweetid, creationDate, tweetType, tweetText, retweets, favorites, language, geo, profLoc):
	result = [keyword, username, screenName, tweetid, creationDate, tweetType, tweetText, retweets, favorites, language, geo, profLoc]
	return result

def queryConstructor(searchTerm):
	query = searchTerm # adding a hashtag to the search query seems to filter out more of the unrelated tweets, but also severely limits the number of tweets returned. 
	print(query)
	return query

def writeToFile(file, writeArray): # write collected tweets to a file
	with open(file, mode='a') as tweets:
		tweetWriter = csv.writer(tweets, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		tweetWriter.writerow(writeArray)								
		tweets.close()

tweetOutputFile = "premiumTweets - 2018 to 2019.csv"

searchList = []# list of keywords to use in the queries
with open('premiumKeywords.txt', 'r') as myfile: # import text file of keywords. File consists of keywords separated by commas
	search=myfile.read().replace('\n', '')
	print("Search file imported\n")
	if search is not None:
		searchList = search.split(',')

print(searchList) # Print the searchList to be sure it contains all the requested 

premium_search_args = load_credentials("./twitter_keys.yaml", #load credentials for the searchtweets API. The ./twitter_keys.yaml file is located in the same place as the rest of the program files
										yaml_key="search_tweets_api",
										env_overwrite=False) #connect to the twitter API

"""
.yaml file looks like this:

search_tweets_api:
  account_type: premium
  endpoint: [your twitter application endpoint]
  consumer_key: [your consumer_key from twitter api]
  consumer_secret: [your consumer_secret from twitter api] 
"""

writeToFile(tweetOutputFile, getHeaders())# write the header to the csv file first. As it is written now, the header will be added every time the code is run.
 
for keyword in searchList: # search each keyword in the searchList imported above

	rule = gen_rule_payload(queryConstructor(keyword), from_date="2018-01-01", results_per_call=500) #create the search rule for the search API. Timestamp is in the following form: YYYY-mm-DD. Max results per call for premium account is 500 Additional parameters: to_date="2019-07-11",
	print(rule)
	tweets = collect_results(rule, max_results=10000, result_stream_args=premium_search_args) # send the query to the API with the rule created previously, the total number of tweets that you want returned, and what type of account you are using (Premium or Enterprise)

	for tweet in tweets: # write collected tweets to a file.

		writeToFile(tweetOutputFile, getResults(keyword, tweet.name, tweet.screen_name, tweet.created_at_datetime, tweet.tweet_type, tweet.all_text, tweet.id, tweet.retweet_count, tweet.favorite_count, tweet.lang, tweet.geo_coordinates, tweet.profile_location))# Write the desired results from the tweets into a csv file. Tweet fields can be found from the tweet_parser URL at the top.
		# Fields: keyword - keyword used in the search query, name - name of the twitter user, screen_name - screen name of the twitter user, created_at_datetime - time the tweet was created in YYYY-mm-DD format, 
		#         tweet_type - type of tweet. Can be either tweet, quote, or retweet, all_text - text of the tweet, id - snowflake id of the tweet, retweet_count - number of retweets a particular tweet has,
		#         favorite_count - number of times the tweet has been favorited, lang - language the tweet is written in to two character codes, geo_coordinates - location that the tweet was tweeted from. Usually in lat/long format,
		#         profile_location - location of the twitter user from their profile. Collected because most tweets do no have location data.