from os import listdir
from os.path import isfile, join
import pickle
from ManualTrecFileParser import RegexParseTrecFile
from enum import Enum
import sys

def progress_bar(progress, doc):
    if isinstance(progress, int):
        progress = float(progress)
    block = int(round(20*progress))
    text = "\rCompleted: [{0}] {1:5.2f}% of documents: {2}".format("#"*block + "-"*(20-block), progress*100, doc)
    sys.stdout.write(text)
    sys.stdout.flush()


class DoubleListNode(object):
    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next


class DoubleList(object):
    head = None
    tail = None
    iterator = None

    def append(self, data):
        new_node = DoubleListNode(data, None, None)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = None
            self.tail.next = new_node
            self.tail = new_node

    def init_iterator(self):
        self.iterator = self.head

    def init_reverse_iterator(self):
        self.iterator = self.tail

    def get_next(self):
        if self.iterator is None:
            return None
        retval = self.iterator
        self.iterator = self.iterator.next
        return retval

    def get_prev(self):
        if self.iterator is None:
            return None
        retval = self.iterator
        self.iterator = self.iterator.prev
        return retval

    def get_last(self):
        return self.tail

    def remove(self, node_value):
        current_node = self.head

        while current_node is not None:
            if current_node.data == node_value:
                # if it's not the first element
                if current_node.prev is not None:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                else:
                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
                    self.head = current_node.next
                    current_node.next.prev = None

            current_node = current_node.next


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
    def __init__(self):
        self.index = {}
        self.docno_dict = []

    def eval(self, query):
        if query.type == TreeNodeType.DATA:
            return self.index[query.data]
        retval = DoubleList()
        if query.type == TreeNodeType.AND:
            left = self.eval(query.left)
            right = self.eval(query.right)
            left.init_iterator()
            right.init_iterator()
            left_it = left.get_next()
            right_it = right.get_next()
            while left_it is not None and right_it is not None:
                if left_it.data == right_it.data:
                    retval.append(left_it.data)
                    left_it = left.get_next()
                    right_it = right.get_next()
                if left_it.data < right_it.data:
                    left_it = left.get_next()
                else:
                    right_it = right.get_next()
        if query.type == TreeNodeType.OR:
            left = self.eval(query.left)
            right = self.eval(query.right)
            left.init_iterator()
            right.init_iterator()
            left_it = left.get_next()
            right_it = right.get_next()
            while left_it is not None or right_it is not None:
                if right_it is None or left_it.data < right_it.data:
                    retval.append(left_it.data)
                    left_it = left.get_next()
                if left_it is None or left_it.data > right_it.data:
                    retval.append(right_it.data)
                    right_it = right.get_next()
                else:
                    retval.append(left_it.data)
                    left_it = left.get_next()
                    right_it = right.get_next()
        if query.type == TreeNodeType.NOT:
            left = self.eval(query.left)
            right = self.eval(query.right)
            left.init_iterator()
            right.init_iterator()
            left_it = left.get_next()
            right_it = right.get_next()
            while left_it is not None:
                while right_it is not None and right_it.data < left_it.data:
                    right_it = right.get_next()
                if right_it is not None and right_it.data > left_it.data:
                    retval.append(left_it.data)
                left_it = left.get_next()
        return retval


def InvertedIndex():
    index_object = inverted_index()
    path = r"/data/HW1/AP_Coll_Parsed/"
    trec_files = [f for f in listdir(path) if isfile(join(path, f))]
    num_files = len(trec_files)
    num = 1
    for trec_file in trec_files:
        progress_bar(num / num_files, trec_file)
        trec_dict = RegexParseTrecFile(path + trec_file)
        for docno, text in trec_dict.items():
            internal_index = len(index_object.docno_dict)
            index_object.docno_dict.append(docno)
            for word in text:
                if word not in index_object.index:
                    index_object.index[word] = DoubleList()
                index_object.index[word].append(internal_index)
        num += 1
    with open('/home/student/HW1/index', 'wb') as f:
        pickle.dump(index_object.index, f)
    with open('/home/student/HW1/index_dict', 'wb') as f:
        pickle.dump(index_object.docno_dict, f)


if __name__ == "__main__":
    InvertedIndex()
