from StopWordsFilter import FilterStopWords
import re


def printDictionary(dictionary):
    for key in dictionary:
        print("DOCNO :", key, "\nTEXT =", dictionary[key], "\n")

# Parses trec file, using regex expressions
# params:
# - pathtofile: path to trec file 
# return: 
# - Dictionary: Key=DOCNO, Value=TEXT 
# Value as Set of splitted strings from <TEXT><\TEXT> without stop words
def RegexParseTrecFile(pathtofile):
    # Reading file
    with open(pathtofile, 'r') as f:
        trecFileString = f.read()

    # Adding a fake root tag (Not necessary in our parser)
    trecFileString = '<ROOT>' + trecFileString + '</ROOT>'

    # Initialize result dictionary
    results = {}

    # Find all documents in file, including subtags. 
    documents = re.findall("<DOC>[\s\S]*?<\/DOC>", trecFileString)

    # TODO: Check if necessary find tags as case-INsensetive,
    #       if its needed use: re.findall(pattern, string, re.I)
    # Iterate through each DOC and cut only DOCNO and TEXT tags
    for doc in documents:
        # Regex Pattern to find content between <DOC></DOC>
        docnoTagRegexResultList = re.findall("<DOCNO>(.*?)<\/DOCNO>", doc)

        # If DOC don`t have DOCNO tag, don`t continue
        if not docnoTagRegexResultList:
            continue

        # Transform returned regex match from List to string
        docno = ''.join(docnoTagRegexResultList)

        # Extract all text between <TEXT></TEXT>
        textTagRegexResultList = re.findall("<TEXT>(.*?)<\/TEXT>", doc, re.S)

        # If text in DOC was empty or tag do not exists, don`t continue
        if not textTagRegexResultList:
            continue

        # Transform regex match from List to string
        textTagRegexResultString = ''.join(textTagRegexResultList)

        # Remove end of lines and tabs from string
        textTagRegexResultClear = textTagRegexResultString.replace('\n', ' ').replace('\r', '')

        # Remove all Stop Words from text, returns Set of strings
        text = FilterStopWords(textTagRegexResultClear)

        # Add legal elements to result dictionary
        results[docno] = text

    return results


# TODO: remove on release
# Print dictionary keys and values example
# printDictionary(RegexParseTrecFile('test.txt'))
