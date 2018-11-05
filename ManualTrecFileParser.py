from StopWordsFilter import FilterStopWords
import re


def RegexParseTrecFile(pathtofile):
    # Reading file
    with open(pathtofile, 'r') as f:
        xml = f.read()

    # Adding a fake root tag (Not necessary in our parser)
    xml = '<ROOT>' + xml + '</ROOT>'

    # Initialize result dictionary
    results = {}

    # Find all documents in file
    documents = re.findall("<DOC>[\s\S]*?<\/DOC>", xml)

    # Iterate through each DOC and gather DOCNO and TEXT
    for doc in documents:
        # Regex Pattern to find all betwee <DOC></DOC>
        docnoTagRegexResultList = re.findall("<DOCNO>(.*?)<\/DOCNO>", doc)

        # Transform return value (that is List) to string
        docno = ''.join(docnoTagRegexResultList)

        # Find all between <TEXT></TEXT>
        textTagRegexResultList = re.findall("<TEXT>(.*?)<\/TEXT>", doc, re.S)

        # Transform result list to string
        textTagRegexResultListString = ''.join(textTagRegexResultList)

        # Clear end of lines and tabs from string
        textTagRegexResultListClear = textTagRegexResultListString.replace('\n', ' ').replace('\r', '')

        # Clear all Stop Words from text
        text = FilterStopWords(textTagRegexResultListClear)

        # If text in DOC was empty , dont add
        if not text:
            continue

        # Add legal elements to result dictionary
        results[docno] = text

    return results



