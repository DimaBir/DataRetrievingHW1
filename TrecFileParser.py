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
        try:
            # Key : DOCNO, VALUE: SET OF WORDS WITHOUT STOPWORDS
            key = doc.find('DOCNO').text.strip()
            text = FilterStopWords(doc.find('TEXT').text.strip())
            results[key] = text
        except AttributeError:
            print("Doc {} has no text".format(key))
    return results


result = parsetrecfile('test.trec')
