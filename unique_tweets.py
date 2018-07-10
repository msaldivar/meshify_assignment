#!/usr/bin/python3

import twitter
import threading
import multiprocessing

UNIQUE_TWEETS_NUM = 2000
QUERY = '#IOT'

api = twitter.Api(
    consumer_key='...',
    consumer_secret='...',
    access_token_key='...',
    access_token_secret='...')

unique_tweets = set()  # shared data structure: holds all the unique tweets
search = []  # shared data structure: holds the api search results
lock = threading.Lock()


def main():
    # sanity check on credentials
    assert credentials_check() == True, "API credentials failed"
    global search

    # initiate the shared data structures
    search = api.GetSearch(QUERY, count=100)
    # make sure search doesn't return zero tweets
    assert search != [], "search returned no results. Query issue?"
    process_search_results(search)

    thread_list = create_threads(get_thread_count())
    start_threads(thread_list)
    join_threads(thread_list)

    create_csv()


def credentials_check():
    """check that credentials are valid"""
    try:
        api.VerifyCredentials()
        return True
    except:
        return False


def search_twitter():
    """
    The method that threads will execute. 

    The method determines what 'page' we are on by using the last tweet 
    ID minus 1 (curr_id = tweet.id-1). A lock is used to make sure the
    correct ID is calculated before making the search. Otherwise we could end up
    in a condition of multiple threads returning the same tweets because they're
    requesting the same 'page'.  

    Once the api returns the data is processed to find only unique tweets and 
    is stored [tweet.ID, tweet.text]. The data can always be reprocessed and 
    search on tweet.ID to get metadata. 

    If UNIQUE_TWEETS_NUM is greater than the tweets available just have the 
    thread return. Also if UNIQUE_TWEETS_NUM is too large it's possible to 
    hit the rate limit causing the program to fail. 

    Returns:
    unique_tweets() will be updated 

    """
    while len(unique_tweets) != UNIQUE_TWEETS_NUM:
        global lock
        global search
        with lock:
            curr_id = search[-1].id - 1
            search = api.GetSearch(QUERY, count=100, max_id=curr_id) 
            if not search: 
                # no longer getting new 'pages' so have thread return. 
                return 
            process_search_results(search)     


def process_search_results(search):
    """
    use search results to add to the set() of unique tweets.

    Parameters: 
    search : list
        the current search results from the twitter api.

    Returns:
    unique_tweets() will be updated.
    
    """
    for tweet in search:
        if len(unique_tweets) == UNIQUE_TWEETS_NUM:
            break
        unique_tweets.add((tweet.id_str,
                           str(tweet.text.encode('utf-8')).replace('\n', '')))


def get_thread_count():
    """
    Note: optimal thread count is highly system dependent.
    To help generalize this problem the number of threads will be based on the 
    return value of nproc.
    
    Returns: 
    int for how many threads to create.
     
    """
    return multiprocessing.cpu_count()


def create_threads(thread_num):
    """Returns a list of initizlized threads."""
    return [threading.Thread(target=search_twitter) for i in range(thread_num)]


def start_threads(thread_list):
    """Start the threads and set them as a daemon process."""
    for thread in thread_list:
        thread.daemon = True
        thread.start()


def join_threads(thread_list):
    """Join the threads"""
    for thread in thread_list:
        thread.join()


def create_csv():
    """Generate .csv file: Tweet ID, Tweet.text."""
    with open("unique_tweets.csv", "w", encoding='utf-8') as outfile:
        for tweet in unique_tweets:
            outfile.write(str(tweet[0]) + "," + str(tweet[1]) + "\n")

        outfile.close()


if __name__ == "__main__":
    main()