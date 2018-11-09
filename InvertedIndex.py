from os import listdir
from os.path import isfile, join
import pickle
from ManualTrecFileParser import RegexParseTrecFile
from enum import Enum
import sys
import shelve


def progress_bar(progress, doc):
    if isinstance(progress, int):
        progress = float(progress)
    block = int(round(20*progress))
    text = "\rCompleted: [{0}] {1:5.2f}% of documents: {2}".format("#"*block + "-"*(20-block), progress*100, doc)
    sys.stdout.write(text)
    sys.stdout.flush()


class TreeNodeType(Enum):
    AND = 1
    OR = 2
    NOT = 3
    DATA = 4


class TreeNode(object):
    def __init__(self, type, data = None, left = None, right = None):
        self.type = type
        self.data = data
        self.left = left
        self.right = right


class inverted_index(object):
    def __init__(self, ind_file):
        self.index = shelve.open(ind_file, writeback=True)
        self.docno_dict = []

    def eval(self, query):
        if query.type == TreeNodeType.DATA:
            return self.index[query.data]
        retval = []
        left = self.eval(query.left)
        right = self.eval(query.right)
        i = j = 0
        if query.type == TreeNodeType.AND:
            while i < len(left) and j < len(right):
                if left[i] == right[j]:
                    retval.append(left[i])
                    i += 1
                    j += 1
                elif left[i] < right[j]:
                    i += 1
                else:
                    j += 1
        if query.type == TreeNodeType.OR:
            while i < len(left) or j < len(right):
                if j >= len(right) or (i < len(left) and left[i] < right[j]):
                    retval.append(left[i])
                    i += 1
                elif i >= len(left) or (j < len(right) and left[i] > right[j]):
                    retval.append(right[j])
                    j += 1
                else:
                    retval.append(left[i])
                    i += 1
                    j += 1
        if query.type == TreeNodeType.NOT:
            while i < len(left):
                while j < len(right) and right[j] < left[i]:
                    j += 1
                if j < len(right) and right[j] > left[i]:
                    retval.append(left[i])
                i += 1
        return retval


def InvertedIndex(input_dir, output_dir):
    index_object = inverted_index(output_dir + 'index')
    index_object.index.clear()
    path = input_dir
    trec_files = [f for f in listdir(path) if isfile(join(path, f))]
    num_files = len(trec_files)
    num = 1
    for trec_file in trec_files:
        progress_bar(num / num_files, trec_file)
        trec_dict = RegexParseTrecFile(path + trec_file)
        for docno, text in trec_dict.items():
            internal_index = len(index_object.docno_dict)
            index_object.docno_dict.append(docno.strip())
            for word in text:
                if word not in index_object.index:
                    index_object.index[word] = [internal_index]
                else:
                    index_object.index[word].append(internal_index)
        if num % 200 == 0:
            index_object.index.sync()
        num += 1
    index_object.index.close()
    with open(output_dir + 'index_dict', 'wb') as f:
        pickle.dump(index_object.docno_dict, f)


if __name__ == "__main__":
    input_dir = r"/data/HW1/AP_Coll_Parsed/"
    output_dir = r'/home/student/HW1/'
    InvertedIndex(input_dir, output_dir)
