import xml.etree.ElementTree as ElementTree


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
        results[doc.find('DOCNO').text.strip()] = doc.find('TEXT').text.strip()

    return results


result = parsetrecfile('test.trec')

print("Modified Dict : ")
for (key, value) in result.items():
    print(key, " :: ", value)

