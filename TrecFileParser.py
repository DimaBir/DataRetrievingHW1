import xml.etree.ElementTree as ElementTree
from StopWordsFilter import FilterStopWords


def parsetrecfile(pathtofile):

    # Reading file
    with open(pathtofile, 'r') as f:
        xml = f.read()

    # Adding a fake root tag
    xml = '<ROOT>' + xml + '</ROOT>'

    # Get all xml tree via root element as ElementTree
    root = ElementTree.fromstring(xml)

    # Initialize reuslt dictionary
    results = {}

    # Simple loop through each document and add results to dictionary
    for doc in root:
        textSet = FilterStopWords(doc.find('TEXT').text.strip())
        if textSet == set():
            continue
        # Key : DOCNO, VALUE: SET OF WORDS WITHOUT STOPWORDS
        results[doc.find('DOCNO').text.strip()] = textSet

    return results
