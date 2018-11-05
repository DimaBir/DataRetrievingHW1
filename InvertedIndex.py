from os import listdir
from os.path import isfile, join
import pickle


class Node(object):
    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next


class DoubleList(object):
    head = None
    tail = None
    iterator = None

    def append(self, data):
        new_node = Node(data, None, None)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = None
            self.tail.next = new_node
            self.tail = new_node

    def init_iterator(self):
        self.iterator = self.head

    def get_next(self):
        if self.iterator is None:
            self.init_iterator()
        retval = self.iterator
        self.iterator = self.iterator.next
        return retval

    def get_prev(self):
        if self.iterator is None:
            self.iterator = self.tail
        retval = self.iterator
        self.iterator = self.iterator.prev
        return retval

    def get_last(self):
        return self.tail

    def remove(self, node):
        prev = node.prev
        next = node.next
        if node == self.head:
            self.head = next
        if node == self.tail:
            self.tail = prev
        if node == self.iterator:
            self.iterator = next
        if prev is not None:
            prev.next = next
        if next is not None:
            next.prev = prev
index = {}
docno_dict = []


def InvertedIndex():
    path = r"/data/HW1/"
    trec_files = [f for f in listdir(path) if isfile(join(path, f))]
    for trec_file in trec_files:
        trec_dict = get_info_dict(trec_file)
        for docno, text in trec_dict.items():
            internal_index = len(docno_dict)
            docno_dict.append(docno)
            for word in set(text.split()):
                if word not in index:
                    index[word] = DoubleList()
                index[word].append(internal_index)
    with open('/home/student/HW1/index', 'wb') as f:
        pickle.dump(index, f)
