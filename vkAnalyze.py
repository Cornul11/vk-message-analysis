#!python3
import os
import re
import sys
import graphs
from collections import Counter, OrderedDict
from bs4 import BeautifulSoup

# To get rid of file extension when making graphs
file_split = re.compile(r'(.*)(.[a-zA-Z0-9]{3,4})')

"""
If value exists in the dictionary, increment count. Else add a new entry.
"""


def add_to_dictionary(dictionary, value):
    if value in dictionary:
        dictionary[value] += 1
    else:
        dictionary[value] = 1
    return dictionary


"""
Generates a list of frequent words from the list of messages.
Uses a list of common words to avoid.
Takes one message at a time and repeats the following steps:
    Get individual words by splitting the message on every space.
    Convert each word to lower case.
    If the word is in the list of common words, go to the next word.
    Otherwise, "clean" the word. This involves removing any non-alphanumeric characters.
    If the word is already in the dictionary, increment the count.
    Else add it to the list.
When the entire list of messages is covered, return the frequency dict.
"""


def get_word_frequency(message_list):
    with open('commonWordsRussian.txt', 'r') as word_file:
        common_words_list = word_file.read()
    clean_word = re.compile(r'[а-яА-Яa-zA-z0-9]+')
    frequency_dictionary = Counter()
    for messages in message_list:
        processed_words = []
        words_list = messages.split(' ')
        for words in words_list:
            word = words.lower()
            if word in common_words_list:
                continue
            if clean_word.search(word):
                word = clean_word.search(word).group()
                processed_words.append(word)
        frequency_dictionary.update(processed_words)
    return frequency_dictionary


"""
Function to accept command-line arguments.
If no arguments are found, then it prints an error and stops the script.
Else it returns the arguments.
"""


def get_file_name():
    # If no filename is given
    if len(sys.argv) < 2:
        print('Usage: vkAnalyze.py file_name.extension')
        sys.exit()
    # Get file name from command line
    return ' '.join(sys.argv[1:])


"""
Function to read the input file of chats.
Copies it to a variable and returns it.
"""


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as fi:
        text_to_analyze = fi.readlines()
    return text_to_analyze


"""
    Initialize all variables.
    Read one message at a time.
    Check if it matches our Regex "line" format.
    If it does, perform this process:
        Separate the date, time, person and put them into separate dictionaries.
        If the message isn't some sort of media attachment, add to message_list.
        Increment the number of messages.
    """


def collect_data(text_to_analyze):
    # Initializing our variables
    number_of_messages = 0
    message_list = []

    # Collecting data into variables
    for lines in text_to_analyze:
        if str(lines.text):
            print(lines.text)
            message_list.append(lines.text)
            number_of_messages += 1
    word_dictionary = get_word_frequency(message_list)
    return word_dictionary, number_of_messages


"""
Sorts a dictionary by value or key. Value by default.
Uses an OrderedDict since in Python dictionaries can't be sorted.
"""


def sort_dictionary(dictionary, sort_by='value'):
    if sort_by == 'key':
        return OrderedDict(sorted(dictionary.items()))
    return OrderedDict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))


def driver():
    # Read given file
    file_name_with_extension = get_file_name()
    file_name = file_split.search(file_name_with_extension)[1]
    text_to_analyze = BeautifulSoup(open(file_name_with_extension), "lxml")
    my_divs = text_to_analyze.findAll("div", {"class": "msg_body"})

    # Collect data
    '''date_dictionary, time_dictionary, person_dictionary, '''
    word_dictionary, number_of_messages = collect_data(my_divs)

    # Sort all Dictionaries here
    word_dictionary = OrderedDict(word_dictionary.most_common(20))

    if not os.path.exists('outputVk'):
        os.mkdir('outputVk')

    graphs.bar_graph(
        word_dictionary, 20, 'Uses',
        'Most used words in ' + str(number_of_messages) + ' messages in ' + file_name,
        'outputVk/' + file_name + 'word_frequency.png'
    )


if __name__ == "__main__":
    driver()
