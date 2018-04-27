# Purpose: Use Tweepy to conduct a historical and live stream search of Twitter.
# Updated: Nov. 8, 2017 by Amir-mine
#
# Cross-platform way to use Tweepy to grab tweets as a JSON file, which is then stored in a CSV file.
# Allows the ability to store Unicode characters in UTF-8 format without crashing.
# Coded in PyCharm and Tested on MS Windows 10.
import numpy as np
import json
import tweepy
from tweepy import Cursor
import csv
import os  # Used to show where the new files were stored.
from StreamCaptureAsList import StreamParser
from matplotlib import pyplot as plt

# Your Twitter app authentication for Tweepy.
consumer_key = '#' #Consumer key (sign up on Twitter)
consumer_secret = '#' #Consumer Secret(sign up on Twitter)
access_token = '#' #Access token (sign up on Twitter)
access_token_secret = '#'  #Access token secret (sign up on Twitter)


def historical_search_print(storage):
    # Function for historical Search and print it
    print("----------------------")
    print("Printing Historical search... ")
    print("----------------------\n")
    # Checks to make sure the program has the variables set above.
    if consumer_key == '' or consumer_secret == '' or access_token == '' or access_token_secret == '':
        print("Error: Please set your Twitter app authentication for Tweepy in the source code!")
        quit()

    # Tweepy will log into the Twitter API with our credentials.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Filenames to use for output (they will be either ".json" or ".csv" depending on usage need).
    output_historical_file = "historical_tweets"
    output_livestream_file = "live_streamed_tweets"

    # Determines the maximum number of tweets to gather for both historical and live streaming.
    # Intentional never-ending loop to force the user to type an integer.
    while True:
        try:
            max_tweets = int(input("Maximum number of tweets to gather? "))
            break  # This exits the while-loop if there were no problems from the int() above.

        except ValueError:
            print("Error: Please only input a number.\n")

    historical_search_filter = input("What do you want to conduct a historical search on? ")

    tweets_collected = tweepy.Cursor(api.search, q=historical_search_filter).items(max_tweets)

    followers = []  # list for collecting the number of followers
    number_of_friends = []  # list for collecting the number of friends
    number_of_statuses = []  # list for collecting the number of statuses

    for result in tweets_collected:  # read the tweets and print them
        print('Tweet :', str(result.text))
        print('Language: ', str(result.lang))
        print('Username: ', str(result.user.name))
        print('Screen name: ', str(result.user.screen_name))
        print('Number of followers : ', str(result.user.followers_count))
        print('Number of statuses: ', str(result.user.statuses_count))
        print('Number of friends: ', str(result.user.friends_count))
        # print('Number of favorites: ', str(result.retweeted_status.favorite_count))
        print('Location: ', str(result.user.location))
        print('---------------------------------------------------------------')
        followers.append(result.user.followers_count)
        number_of_friends.append(result.user.friends_count)
        number_of_statuses.append(result.user.statuses_count)
    print("Success! All the tweets were printed.\n")
    plot_file(max_tweets, followers, number_of_friends, number_of_statuses, historical_search_filter)


def live_stream_print(storage):
    # Function to get live data from Twitter
    print()  # Blank line for whitespace.
    print("-------------------")
    print(" Live streaming... ")
    print("-------------------\n")
    # Checks to make sure the program has the variables set above.
    if consumer_key == '' or consumer_secret == '' or access_token == '' or access_token_secret == '':
        print("Error: Please set your Twitter app authentiction for Tweepy in the source code!")
        quit()

    # Tweepy will log into the Twitter API with our credentials.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Filenames to use for output (they will be either ".json" or ".csv" depending on usage need).

    output_livestream_file = "live_streamed_tweets"

    # Determines the maximum number of tweets to gather for both historical and live streaming.
    # Intentional never-ending loop to force the user to type an integer.
    while True:
        try:
            max_tweets = int(input("Maximum number of tweets to gather? "))
            max_seconds_checker = input("Maximum seconds by default is 120 seconds, do you want to change it? y/n ")
            if max_seconds_checker == 'y':
                max_seconds = int(input("Maximum seconds? "))
            else:
                max_seconds = 120
            break  # This exits the while-loop if there were no problems from the int() above.

        except ValueError:
            print("Error: Please only input a number.\n")

    print("Note: Maximum time the live stream query will last is: {} seconds.\n".format(max_seconds))

    livestream_search_filter = list(input('What do you want to live stream on? ').split(','))
    print()  # Blank line for whitespace.

    # We'll send a blank List to the StreamParser to fill up with tweets!
    tweets_list = []
    listener = StreamParser(tweets_list, max_tweets, max_seconds)
    stream = tweepy.Stream(auth, listener)

    # This line will filter Twitter streams to capture data by the keywords, which can be a List.
    print(stream.filter(track=livestream_search_filter))

    with open(output_livestream_file + ".json", 'w') as json_output_file:
        # Writes all of the tweets that were stored in the List (from StreamParser) as a proper JSON file.
        json.dump(tweets_list, json_output_file)

    with open("live_streamed_tweets" + ".csv", 'w', newline='', encoding='utf-8') as csvfile:
        tweetwriter = csv.writer(csvfile)
        tweetwriter.writerow(
            ["Twitter_Username", "Tweet_Text", "Language", "Location", "# of friends", "# of followers",
             "# of Statuses", "# of favorites"])

        with open("live_streamed_tweets" + ".json", 'r') as json_file:
            # Reads the entire JSON content, which can be one or more tweets.
            # Notice how it is json.load() and not json.loads() [with an 's']
            json_data = json.load(json_file)

        num_followers = []
        num_status = []
        num_friends = []
        # Each tweet is stored as a JSON-like string, such as: json_data[0]
        for one_element in json_data:
            # But, we need to reload even the json_data[0] again via json.loads() [notice the 's' on .loads()]
            # The difference between .load() and .loads() is that .loads() is for ONE string, not an entire file.
            tweet = json.loads(one_element)

            # The Twitter data fields we care about.
            name = tweet['user']['screen_name']
            tweet_text = tweet['text']
            language = tweet['user']['lang']
            place = tweet['user']['location']
            friends = tweet['user']['friends_count']  # number of friends
            followers = tweet['user']['followers_count']  # number of followers
            status_count = tweet['user']['statuses_count']  # number of statuses
            favorite_count = tweet['user']['favourites_count']  # number of favorites
            num_followers.append(followers)  # append to the list of followers
            num_friends.append(friends)  # append to the list of friends
            num_status.append(status_count)  # append to the list of statuses

            # Removes newline characters from the tweet_text to avoid accidentally creating new CSV rows in the wrong places.
            tweet_text = tweet_text.replace("\n", " ")

            # Writes the data fields to the CSV file.
            tweetwriter.writerow([name, tweet_text, language, place, friends, followers, status_count, favorite_count])

    print()

    read_file_csv('live_streamed_tweets.csv')  # read the csv file
    plot_file_live(max_tweets, num_followers, num_friends, num_status, livestream_search_filter)  # plot the result


def historical_search_csv(storage):
    '''Function to do historical Search and save to JSON and CSV files'''
    print("----------------------")
    print(" Historical search... ")
    print("----------------------\n")
    # Checks to make sure the program has the variables set above.
    if consumer_key == '' or consumer_secret == '' or access_token == '' or access_token_secret == '':
        print("Error: Please set your Twitter app authentiction for Tweepy in the source code!")
        quit()

    # Tweepy will log into the Twitter API with our credentials.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Filenames to use for output (they will be either ".json" or ".csv" depending on usage need).
    output_historical_file = "historical_tweets"
    output_livestream_file = "live_streamed_tweets"

    # Determines the maximum number of tweets to gather for both historical and live streaming.
    # Intentional never-ending loop to force the user to type an integer.
    while True:
        try:
            max_tweets = int(input("Maximum number of tweets to gather? "))
            break  # This exits the while-loop if there were no problems from the int() above.

        except ValueError:
            print("Error: Please only input a number.\n")

    historical_search_filter = input("What do you want to conduct a historical search on? ")

    tweets_collected = tweepy.Cursor(api.search, q=historical_search_filter).items(max_tweets)

    # Parses the historical JSON file.
    # print("\nAttempting to create your historical JSON file...")
    tweets_collected_list = []  # Blank list that we'll later fill up.
    with open(output_historical_file + ".json", 'w') as json_output_file:
        for tweet in tweets_collected:
            tweets_collected_list.append(json.dumps(tweet._json))  # Corrects the line-ending problem.

        json.dump(tweets_collected_list, json_output_file)  # Finally creates the JSON file.

        print("Success! The JSON file was saved correctly.\n")

        # Cross-platform way to show where the file was stored on the disk.
        print("File Name:", output_historical_file + ".json")
        print("Full Path: {}".format(os.path.join(os.getcwd(), output_historical_file + ".json")))
    print()
    convert(output_historical_file)  # convert the JSON to CSV

    # Print results if the user wants
    user_action = input("Do you want to see the results? y/n ")
    if user_action == 'y':
        read_file_csv('historical_tweets.csv')
    else:
        print('The file is saved in your folder.')


def live_stream_csv(storage):  # change the live stream tweets to csv file
    print()  # Blank line for whitespace.
    print("-------------------")
    print(" Live streaming... ")
    print("-------------------\n")
    # Checks to make sure the program has the variables set above.
    if consumer_key == '' or consumer_secret == '' or access_token == '' or access_token_secret == '':
        print("Error: Please set your Twitter app authentiction for Tweepy in the source code!")
    # quit()

    # Tweepy will log into the Twitter API with our credentials.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Filenames to use for output (they will be either ".json" or ".csv" depending on usage need).

    output_livestream_file = "live_streamed_tweets"

    # Determines the maximum number of tweets to gather for both historical and live streaming.
    # Intentional never-ending loop to force the user to type an integer.
    while True:
        try:
            max_tweets = int(input("Maximum number of tweets to gather? "))
            max_seconds_checker = input("Maximum seconds by default is 120 seconds, do you want to change it? y/n ")
            if max_seconds_checker == 'y':
                max_seconds = int(input("Maximum seconds? "))
            else:
                max_seconds = 120
            break  # This exits the while-loop if there were no problems from the int() above.

        except ValueError:
            print("Error: Please only input a number.\n")

    print("Note: Maximum time the live stream query will last is: {} seconds.\n".format(max_seconds))

    livestream_search_filter = list(input('What do you want to live stream on? ').split(','))
    print()  # Blank line for whitespace.

    # We'll send a blank List to the StreamParser to fill up with tweets!
    tweets_list = []
    listener = StreamParser(tweets_list, max_tweets, max_seconds)
    stream = tweepy.Stream(auth, listener)

    # This line will filter Twitter streams to capture data by the keywords, which can be a List.
    stream.filter(track=livestream_search_filter)

    print("\n\nAttempting to create your live stream JSON file...")
    with open(output_livestream_file + ".json", 'w') as json_output_file:
        # Writes all of the tweets that were stored in the List (from StreamParser) as a proper JSON file.
        json.dump(tweets_list, json_output_file)

        print("Success! The JSON file was saved correctly.\n")

        # Cross-platform way to show where the file was stored on the disk.
        print("File Name:", output_livestream_file + ".json")
        print("Full Path: {}".format(os.path.join(os.getcwd(), output_livestream_file + ".json")))
    print()
    convert('live_streamed_tweets')  # convert the file to csv

    # Print results if the user wants to see them
    user_action = input("Do you want to see the results? y/n ")
    if user_action == 'y':
        read_file_csv('live_streamed_tweets.csv')  # read the file and print them
    else:
        print('The file is saved in your folder.')  # skip reading the file


def convert(object):
    # Function that converts the JSON file to CSV file
    files_to_convert = [object]
    # Loops according to how many files we need to convert.
    for i in range(0, len(files_to_convert)):

        print("Input File: {}".format(files_to_convert[i] + ".json"))

        with open(files_to_convert[i] + ".csv", 'w', newline='', encoding='utf-8') as csvfile:
            tweetwriter = csv.writer(csvfile)
            tweetwriter.writerow(
                ["Twitter_Username", "Tweet_Text", "Language", "Location", "# of friends", "# of followers",
                 "# of Statuses"])

            with open(files_to_convert[i] + ".json", 'r') as json_file:
                # Reads the entire JSON content, which can be one or more tweets.
                # Notice how it is json.load() and not json.loads() [with an 's']
                json_data = json.load(json_file)

                # Each tweet is stored as a JSON-like string, such as: json_data[0]
                for one_element in json_data:
                    # But, we need to reload even the json_data[0] again via json.loads() [notice the 's' on .loads()]
                    # The difference between .load() and .loads() is that .loads() is for ONE string, not an entire file.
                    tweet = json.loads(one_element)

                    # The Twitter data fields we care about.
                    name = tweet['user']['screen_name']
                    tweet_text = tweet['text']
                    language = tweet['user']['lang']
                    place = tweet['user']['location']
                    friends = tweet['user']['friends_count']  # number of friends
                    followers = tweet['user']['followers_count']  # number of followers
                    status_count = tweet['user']['statuses_count']  # number of statuses
                    favorite_count = tweet['user']['favourites_count']  # number of favorites

                    # Removes newline characters from the tweet_text to avoid accidentally creating new CSV rows in the wrong places.
                    tweet_text = tweet_text.replace("\n", " ")

                    # Writes the data fields to the CSV file.
                    tweetwriter.writerow(
                        [name, tweet_text, language, place, friends, followers, status_count, favorite_count])

        # print("Success! The CSV file was saved correctly.")

        # Cross-platform way to show where the file was stored on the disk.
        print("Output File Name:", files_to_convert[i] + ".csv")
        print("Full Path: {}\n".format(os.path.join(os.getcwd(), files_to_convert[i] + ".csv")))


def read_file_csv(object):  # function that reads CSV file if the user wants to check the CSV file
    with open(object, "r",
              encoding="utf8") as f:  # encoding="utf8" is from https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
        f_csv = csv.reader(f)
        headings = next(f_csv)
        for row in f_csv:
            print('Username: ', row[0])
            print('Tweet text: ', row[1])
            print('Language: ', row[2])
            print('Location: ', row[3])
            print('# of friends: ', row[4])
            print('# of followers: ', row[5])
            print('# of Statuses: ', row[6])
            print('# of favorites: ', row[7])
            print('*****************************************************')


def plot_file(max_tweets, followers, number_of_friends, number_of_statuses, object):
    # Function for plotting the historical search
    plotting = ''  # selected option by user
    while plotting != 'q':  # loop to show the options and plot
        plotting = input(
            "Plotting Menu\n****************************************\n1.Plotting number of followers\n2.Plotting number of Friends\n3.Plotting number of statuses\nq.Main Menu\nPlease select your option: ")
        if plotting == '1':  # plot number of followers
            num_tweets = []
            for i in range(max_tweets):
                num_tweets.append(int(i) + 1)
            plt.bar(num_tweets, followers, color="red")
            plt.title("Number of followers of users who tweeted {}".format(object))
            plt.ylabel("Number of followers")
            plt.xlabel("Users")
            print()
            plt.show()
        elif plotting == '2':  # plot number of friends
            num_tweets = []
            for i in range(max_tweets):
                num_tweets.append(int(i) + 1)
            plt.bar(num_tweets, number_of_friends, color="blue")
            plt.title("Number of friends of users who tweeted {}".format(object))
            plt.ylabel("Number of friends")
            plt.xlabel("Users")
            print()
            plt.show()
        elif plotting == '3':  # plot number of statuses
            num_tweets = []
            for i in range(max_tweets):
                num_tweets.append(int(i) + 1)
            plt.bar(num_tweets, number_of_statuses, color="green")
            plt.title("Number of statuses of users who tweeted {}".format(object))
            plt.ylabel("Number of statuses")
            plt.xlabel("Users")
            print()
            plt.show()
        elif plotting == 'q':  # exit the plotting menu and go back to main menu
            break
        else:
            pass


def plot_file_live(max_tweets, num_followers, num_friends, num_status, object):
    # function to plot the live stream file
    plotting = ''  # get the selection by user
    while plotting != 'q':  # loop to show the options and plot
        plotting = input(
            "Plotting Menu\n****************************************\n1.Plotting number of followers\n2.Plotting number of Friends\n3.Plotting number of statuses\nq.Main Menu\nPlease select your option: ")
        if plotting == '1':  # plot the number of followers
            num_tweets = []
            for i in range(max_tweets):
                num_tweets.append(int(i) + 1)
            plt.bar(num_tweets, num_followers, color="red")
            plt.title("Number of followers of users who tweeted {}".format(object[0]))
            plt.ylabel("Number of followers")
            plt.xlabel("Users")
            print()
            plt.show()
        elif plotting == '2':  # plot the number of friends
            num_tweets = []
            for i in range(max_tweets):
                num_tweets.append(int(i) + 1)
            plt.bar(num_tweets, num_friends, color="blue")
            plt.title("Number of friends of users who tweeted {}".format(object[0]))
            plt.ylabel("Number of friends")
            plt.xlabel("Users")
            print()
            plt.show()
        elif plotting == '3':  # plot the number of statuses
            num_tweets = []
            for i in range(max_tweets):
                num_tweets.append(int(i) + 1)
            plt.bar(num_tweets, num_status, color="green")
            plt.title("Number of statuses of users who tweeted {}".format(object[0]))
            plt.ylabel("Number of statuses")
            plt.xlabel("Users")
            print()
            plt.show()
        elif plotting == 'q':
            break
        else:
            pass


def Comparison():
    # Function to compare the live stream and historical search
    count = int(input("How many tweets do you want to compare? "))
    with open("historical_tweets.csv", "r",
              encoding="utf8") as f:  # encoding="utf8" is from https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
        f_csv = csv.reader(f)
        headings = next(f_csv)
        hist_num_statuses = []  # list the number of statuses
        hist_num_followers = []  # list the number of followers
        for row in f_csv:
            hist_num_statuses.append(row[6])
            hist_num_followers.append(row[5])
    with open("live_streamed_tweets.csv", "r", encoding="utf8") as g:
        # open the live stream file
        g_csv = csv.reader(g)
        headings = next(g_csv)
        live_stream_statues = []  # list the number of statuses by users who tweeted
        live_stream_followers = []  # list the number of followers by users who tweeted
        for row in g_csv:
            live_stream_followers.append(row[5])
            live_stream_statues.append(row[6])
        num_tweets = []  # make a list of number of tweets
        for i in range(count):
            num_tweets.append(int(i) + 1)
        num_tweets = np.array(num_tweets)
    p1 = plt.bar(num_tweets - 0.2, hist_num_statuses[:count], color='Blue',
                 width=0.3)  # bar plot of historical search statuses
    p2 = plt.bar(num_tweets + 0.2, live_stream_statues[:count], color='Red',
                 width=0.3)  # bar plot of live stream statuses
    plt.title("Comparing number of statuses of people in historical search and live stream")
    plt.ylabel("Number of statuses")
    plt.xlabel("Users")
    plt.legend([p1, p2], ["# of statuses of peoples who tweeted in Hist. search ",
                          "# of statuses of peoples who tweeted in Live stream"])
    plt.show()

    p3 = plt.bar(num_tweets - 0.2, hist_num_followers[:count], color='Blue',
                 width=0.3)  # bar plot of historical search followers
    p4 = plt.bar(num_tweets + 0.2, live_stream_followers[:count], color='Red',
                 width=0.3)  # bar plot of live stream followers
    plt.title("Comparing number of followers of people in historical search and live stream")
    plt.ylabel("Number of followers")
    plt.xlabel("Users")
    plt.legend([p3, p4], ["# of followeres of peoples who tweeted in Hist. search ",
                          "# of followeres of peoples who tweeted in Live stream"])
    plt.show()


def menu():
    '''The main menu function '''
    print()
    print('Main Menu')
    print()
    print('1. Historical Search-print')
    print('2. Live Stream-print')
    print('3. Historical Search to CSV file')
    print('4. Live Stream to CSV file')
    print('5. Comparing live stream and historical search')
    print('q. To Exit')
    print()


def PR(selection, storage):
    '''The process function runs the selected function by user'''
    if selection == '1':
        historical_search_print(storage)  # print historical result
    elif selection == '2':
        live_stream_print(storage)  # print live stream
    elif selection == '3':
        historical_search_csv(storage)  # make a CSV file of historical search
    elif selection == '4':
        live_stream_csv(storage)  # make a CSV file of live stream
    elif selection == '5':
        Comparison()  # run the function to compare the results
    else:
        return 'q'


def main():
    '''The main function of Twitter Usage'''
    print()
    print('Welcome to Twitter Historical search and live stream system ')
    storage = []
    selection = ''
    while selection != 'q':
        menu()
        selection = input('Select one of the options: ')
        response = PR(selection, storage)  # process the request and run the chosen function
        if selection == 'q':
            break


if __name__ == "__main__":
    main()