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
# returns: return min Heap
def getNLargest(n, minHeap):
    sortedWords = minHeap.items()
    return extractKeysToList(n, sortedWords)


# Gets n smallest values keys in dictionary
# Params:
#        - n : amount of top elements to be returned. if n > |dictonary| will be returned all keys
#        - dictionary: dictionary to work in
# returns: max Heap
def getNSmallest(n, maxHeap):
    sortedWords = maxHeap.items()
    return extractKeysToList(n, sortedWords)

