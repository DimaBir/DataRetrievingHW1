import shelve
import DictionaryUtils
import HeapUtils


# Transforms lists elements to strings are separated by commas
# params: - list: list that will be transformed to strings
# returns: - str - string with elementשורs separated by commas
def formatListToStr(list):
    string = ""
    for i in list[:-1]:
        string = string + str(i) + ', '
    return string + str(list[-1])


# Writes string to file
# params:
#   - str: string to write to file
#   - path: path to file
def writeToFile(str, path):
    with open(path, 'w') as file:
        file.write(str + "\n")


# Creates statistics about most and least frequents words in documents
# params:
#   - output_dir: path to directory where output files will be saved
def createStatstics(output_dir):
    indexFile = shelve.open(output_dir + 'index')
    (minHeap, maxHeap) = HeapUtils.createHeaps(indexFile)
    topTenMostFrequentWords = DictionaryUtils.getNLargest(10, minHeap)
    topTenLeastFrequentWords = DictionaryUtils.getNSmallest(10, maxHeap)

    topTenMostFrequentWordsAsString  = formatListToStr(topTenMostFrequentWords)
    topTenLeastFrequentWordsAsString  = formatListToStr(topTenLeastFrequentWords)

    finalFileContent = "1) Top 10 most common terms: " + topTenMostFrequentWordsAsString + "\n" +\
                       "2) Top 10 least common terms: " + topTenLeastFrequentWordsAsString + "\n" +\
                       "3) Top 10 most frequent words include some 'Stop Words', as we know, from Zipf Law, that"+\
                       " we learned in class, Stop Words are the most frequent words in English language." +\
                       " These common words are expected in most if not all documents." +\
                       " On the other hand, the least frequent words include mostly typos and other mistakes," +\
                       " and precise numeric terms that are context specific or unique mistakes that are" +\
                       " not expected to repeat themselves."

    writeToFile(finalFileContent, output_dir + 'Part_3.txt')


if __name__ == "__main__":
    output_dir = r'/home/student/HW1/'
    createStatstics(output_dir)
