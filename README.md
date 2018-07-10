# Dependencies
* python twitter api: `pip install twitter` 
* valid twitter api keys

# How To Run

## Generate csv of unique tweets based on #IOT
**NOTE:** update `unique_tweets.py` with valid api credentials.  

executing `unique_tweets.py` will generate `unique_tweets.csv` with 2000 lines. To change this number update `UNIQUE_TWEETS_NUM`, be aware of your api rate limit. To change the search parameter update `QUERY`. 

## Testing
executing `test_unique_tweets.py` will run unit tests and print out a report. 