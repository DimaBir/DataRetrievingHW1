from os import listdir
from os.path import isfile, join
import pickle
from ManualTrecFileParser import RegexParseTrecFile
from enum import Enum
import sys
import shelve


def progress_bar(progress, text):
    if isinstance(progress, int):
        progress = float(progress)
    block = int(round(20*progress))
    progress_line = "\rCompleted: [{0}] {1:5.2f}% {2}.".format("#"*block + "-"*(20-block), progress*100, text)
    sys.stdout.write(progress_line)
    sys.stdout.flush()


class inverted_index(object):
    def __init__(self, ind_file):
        self.index = shelve.open(ind_file, writeback=True)
        self.docno_dict = []


def InvertedIndex(input_dir, output_dir):
    index_object = inverted_index(output_dir + 'index')
    index_object.index.clear()
    index_object.index.sync()
    path = input_dir
    trec_files = [f for f in listdir(path) if isfile(join(path, f))]
    num_files = len(trec_files)
    num = 1
    print("Indexing {} TREC files".format(num_files))
    progress_bar(0, "of TREC files")
    for trec_file in trec_files:
        trec_dict = RegexParseTrecFile(path + trec_file)
        for docno, text in trec_dict.items():
            internal_index = len(index_object.docno_dict)
            index_object.docno_dict.append(docno.strip())
            for word in text:
                if word not in index_object.index:
                    index_object.index[word] = [internal_index]
                else:
                    index_object.index[word].append(internal_index)
        if num % 2000 == 0:
            index_object.index.sync()
        progress_bar(num / num_files, "of TREC files")
        num += 1
    print("\nFinished indexing, writing results to files...")
    index_object.index.close()
    with open(output_dir + 'index_dict', 'wb') as f:
        pickle.dump(index_object.docno_dict, f)


if __name__ == "__main__":
    input_dir = r"/data/HW1/AP_Coll_Parsed/"
    output_dir = r'/home/student/HW1/'
    InvertedIndex(input_dir, output_dir)
