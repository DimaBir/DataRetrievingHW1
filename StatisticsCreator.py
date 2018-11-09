import shelve
import DictionaryUtils
from InvertedIndex import InvertedIndex


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
#   - input_dir : path to directory where documents are
#   - output_dir: path to directory where output files will be saved
def createStatstics(input_dir, output_dir):
    indexFile = shelve.open(output_dir + 'index')
    topTenMostFrequentWords = DictionaryUtils.getNLargest(10, DictionaryUtils.transformListToLength(indexFile))
    topTenLeastFrequentWords = DictionaryUtils.getNSmallest(10, DictionaryUtils.transformListToLength(indexFile))

    topTenMostFrequentWordsAsString  = formatListToStr(topTenMostFrequentWords)
    topTenLeastFrequentWordsAsString  = formatListToStr(topTenLeastFrequentWords)

    finalFileContent = "1) Top 10 most common terms: " + topTenMostFrequentWordsAsString + "\n" +\
                       "2) Top 10 least common terms: " + topTenLeastFrequentWordsAsString + "\n" +\
                       "3) Top 10 most frequent words are includes some 'Stop Words', as we know, from Zipf Law, that"+\
                       " we learned in the class, Stop Words are most frequent words in English language.In other" +\
                       " hand, Least frequent words are regular words, and dependent on the subject, so they are" +\
                       " exists in specific documents that describes that subject"

    writeToFile(finalFileContent, output_dir + 'Part3.txt')


if __name__ == "__main__":
    input_dir = r"/data/HW1/AP_Coll_Parsed/"
    output_dir = r'/home/student/HW1/'
    createStatstics(input_dir, output_dir)