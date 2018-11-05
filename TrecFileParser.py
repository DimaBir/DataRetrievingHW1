import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import ParseError
from StopWordsFilter import FilterStopWords


def FindMissingTag(xml):
    try:
        tree = ElementTree.fromstring(xml)
        return tree
    except ParseError as e:
        formatted_e = str(e)
        line = int(formatted_e[formatted_e.find("line ") + 5: formatted_e.find(",")])
        column = int(formatted_e[formatted_e.find("column ") + 7:])
        split_str = xml.split("\n")
        print
        "{}\n{}^".format(split_str[line - 1], len(split_str[line - 1][0:column]) * "-")


def parsetrecfile(pathtofile):

    # Reading file
    with open(pathtofile, 'r') as f:
        xml = f.read()

    # Adding a fake root tag
    xml = '<ROOT>' + xml + '</ROOT>'

    # Get all xml tree via root element as ElementTree
    root = FindMissingTag(xml)

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

