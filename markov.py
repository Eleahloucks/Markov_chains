"""Generate Markov text from text files."""

from random import choice
import sys

def open_and_read_file():
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    #create file object
    file = open(sys.argv[1])
    #read file
    text = file.read()
    #close file - you only have a certain number of active file discriptors
    file.close()

    return text


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains('hi there mary hi there juanita')

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}
    #take text string and split on spaces
    words = text_string.split()
    #loop through words using enumerate so we can reference the next word
    for i, word in enumerate(words):
        #try this block for error
        try:
            # if the tuple of the word and the next word is already a key
            if (word, words[i + 1]) in chains.keys():
                #add the value to the list of words
                chains[(word, words[i + 1])].append(words[i + 2])
            else:
                #set value to the next word in text
                chains[(word, words[i + 1])] = [words[i + 2]]
        #except if there is index error
        except IndexError:
            break

    return chains


def make_text(chains):
    """Return text from chains."""

    #create  var that chooses random key
    working_key = choice(list(chains.keys()))
    #add key words to words
    words = [working_key[0], working_key[1]]
    #start while true loop because we dont many working keys there will be
    while True:
        try:
            #next var picks a word from value list
            next = choice(chains[working_key])
            #add word to words list
            words.append(next)
            #reassign working key to next index key in tuple with next value from list
            working_key = (working_key[1], next)
        #stop loop when there is a key error because we have reached the end of our text
        except KeyError:
            break

    #return words with spaces in between each
    return ' '.join(words)


input_path = 'green-eggs.txt'

# Open the file and turn it into one long string
input_text = open_and_read_file()

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

print(random_text)
