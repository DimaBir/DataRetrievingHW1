from StopWordsFilter import FilterStopWords
import re


def printDictionary(dictionary):
    for key in dictionary:
        print("DOCNO :", key, "\nTEXT =", dictionary[key], "\n")


def RegexParseTrecFile(pathtofile):
    # Reading file
    with open(pathtofile, 'r') as f:
        trecFileString = f.read()

    # Adding a fake root tag (Not necessary in our parser)
        trecFileString = '<ROOT>' + trecFileString + '</ROOT>'

    # Initialize result dictionary
    results = {}

    # Find all documents in file
    documents = re.findall("<DOC>[\s\S]*?<\/DOC>", trecFileString)

    # Iterate through each DOC and gather DOCNO and TEXT
    for doc in documents:
        # Regex Pattern to find all between <DOC></DOC>
        docnoTagRegexResultList = re.findall("<DOCNO>(.*?)<\/DOCNO>", doc)

        # If DOC don`t have DOCNO tag was, don`t continue
        if not docnoTagRegexResultList:
            continue

        # Transform return value (that is List) to string
        docno = ''.join(docnoTagRegexResultList)

        # Find all between <TEXT></TEXT>
        textTagRegexResultList = re.findall("<TEXT>(.*?)<\/TEXT>", doc, re.S)

        # If text in DOC was empty , don`t continue
        if not textTagRegexResultList:
            continue

        # Transform result list to string
        textTagRegexResultListString = ''.join(textTagRegexResultList)

        # Clear end of lines and tabs from string
        textTagRegexResultListClear = textTagRegexResultListString.replace('\n', ' ').replace('\r', '')

        # Clear all Stop Words from text
        text = FilterStopWords(textTagRegexResultListClear)

        # Add legal elements to result dictionary
        results[docno] = text

    return results


# TODO: remove on release
# Print dictionary keys and values example
# printDictionary(RegexParseTrecFile('test.txt'))
