import heapq
from operator import itemgetter


# Prints dictionary as Word:   Frequency:
# Params: result: dictionary to sort
def printDictionary(dictionary):
    for key in dictionary:
        print("Word:", key, "; Frequency:", dictionary[key])


# Sorts dictionary by value
# Params: result: dictionary to sort
# returns: sorted dictionary by asc order
def sortDictionary(result, reverseFlag=True):
    resultSorted = {}
    for k, v in sorted(result.items(), key=itemgetter(1), reverse=reverseFlag):
        resultSorted[k] = v
    return resultSorted


# Upates dictionary value from posting list to its length
# Params: result: dictionary to modify
# retiurns: dictionary of key value pairs, where key is word and value is document frequency
def transformListToLength(dictionary):
    result = {}
    for key, value in dictionary.items():
        result[key] = len(value)
    return result


# Extracts n keys from dictionary
# params:
#   - dictionary to extract from
# Returns:
#   - list of keys
def extractKeysToList(n, dictionary):
    topNElements = {k: sortDictionary(dictionary)[k] for k in list(sortDictionary(dictionary))[:n]}
    topNWords = []
    for key, value in topNElements.items():
        topNWords.append(key)
    return topNWords


# Gets n largest values keys in dictionary
# Params:
#        - n : amount of top elements to be returned. if n > |dictonary| will be returned all keys
#        - dictionary: dictionary to work in
# returns: list of words
def getNLargest(n, dictionary):
    sortedWords = {key: value for key, value in dictionary.items() if value in heapq.nlargest(n, dictionary.values())}
    return extractKeysToList(n, sortedWords)


# Gets n smallest values keys in dictionary
# Params:
#        - n : amount of top elements to be returned. if n > |dictonary| will be returned all keys
#        - dictionary: dictionary to work in
# returns: list of words
def getNSmallest(n, dictionary):
    sortedWords = {key: value for key, value in dictionary.items() if value in heapq.nsmallest(n, dictionary.values())}
    return extractKeysToList(n, sortedWords)

