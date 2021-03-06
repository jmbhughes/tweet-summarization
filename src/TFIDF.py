from tweet import *
import math, time, sys, os
from constants import *

MINIMUM_THRESHOLD = 12

class TFIDF:

    def __init__(self, tweet_collection):
        self.tweets = tweet_collection

    def normalizing_factor(self, tweet):
        return max(MINIMUM_THRESHOLD, tweet.length)

    def idf(self, word):
        ''' Inverse document frequency for a given word '''
        return self.tweets.word_count / len(self.tweets.word_locations[word])

    def tf(self, tweet, word):
        ''' term frequency over a single document documents for a given word '''
        def count_occurrences(word, sentence):
            return sentence.lower().split().count(word)
        return count_occurrences(word, tweet.clean_text)
        #return sum([self.tweets.collection[tweet].word_freq(word) for tweet in self.tweets.word_locations[word]])

    def weight_word(self, tweet, word, stopped=True):
        ''' The weight of a word under h-tfidf '''
        if stopped and word in STOP_WORD_LIST:
            return 0
        else:
            return self.tf(tweet, word) * math.log(self.idf(word), 2.0)

    def weight_tweet(self, tweet, stopped=True):
        ''' The weight of a tweet under h-tfidf '''
        return sum([self.weight_word(tweet, word, stopped=stopped) for word in tweet.clean_text.split()]) / self.normalizing_factor(tweet)

    def build_summary(self, length=5, stopped=True):
        ''' Generates a summary of specified length using the sumbasic algorithm 

            Parameters:
                length -- the number of tweets the summary should take 
        '''

        weights = [(tweet, self.weight_tweet(tweet, stopped=stopped)) for tweetid, tweet in self.tweets.collection.items()]
        weights = sorted(weights, key = lambda pair: pair[1])
        if len(weights) < length:
            return [tweet for tweet, weight in weights]
        else:
            return [tweet for tweet, weight in weights[-length:]]

def usage():
    string = "python SumBasic.py <path to tweets> <location to save> <length> <stopped>\n\n"
    string += "the file of the tweets should be in jsonlist format\n"
    string += "summary length is the number of tweets\n"
    string += "stopped is true if words in the stop list are given a weight of zero\n"
    return string
    
if __name__ == "__main__":
    start_time = time.time()
    args = sys.argv[1:]
    if len(args) != 4:
        print(usage())
    else:
        print("Running Hybrid-TF-IDF summarizer with parameters:")
        print("\t input tweet corpus: ", args[0])
        print("\t output location: ", args[1])
        print("\t summary length: ", args[2])
        print("\t stopped: ", args[3])

    input_location, output_location, length, stopped = args[0], args[1], int(args[2]), bool(args[3])
    tweets = TweetCollection()
    tweets.add_from_file(input_location)
    summarizer = TFIDF(tweets)
    summary = summarizer.build_summary(length, stopped=stopped)

    with open(output_location, "w") as summary_out:
        for tweet in summary:
            print(tweet.raw_text, file=summary_out)
    print("Finished in ", time.time() - start_time, " seconds")

