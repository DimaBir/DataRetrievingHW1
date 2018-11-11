import heapq
from InvertedIndex import progress_bar

# Creates and fills min and max heaps
# Params: dictionary: dictionary to parse
# Returns: Tuple(minHeap, maxHeap)
def createHeaps(dictionary):
    num_terms = len(dictionary)
    num = 1
    print("Calculating most and least frequent terms out of {} terms...".format(num_terms))
    minHeap = MinHeap()
    maxHeap = MaxHeap()
    for key, value in dictionary.items():
        maxHeap.pushMaxHeap((key, len(value)))
        minHeap.pushMinHeap((key, len(value)))
        progress_bar(num / num_terms, "of terms.")
        num += 1
    return minHeap, maxHeap


# Base Class of Object Heap
class Heap(object):
    def __init__(self):
        self.heap = []

    def items(self):
        items = {}
        i = 0
        while i < len(self.heap):
            # swap back to (key, value) pair
            items[self.heap[i][1]] = self.heap[i][0]
            i += 1
        return items


# Inherit from Heap Class, implements Minimum Heap Object
class MinHeap(Heap):
    def __init__(self):
        super().__init__()

    def pushMinHeap(self, item):
        # item = (word, frequency)
        # If heap already have at least 10 elements compare with min, if greater push current
        if len(self.heap) >= 10:
            minElement = self.popMinHeap()
            if minElement[0] >= item[1]:
                item = (minElement[1], minElement[0])
        # inserting (value, key) pair to heap, since heap sort items by first value
        heapq.heappush(self.heap, (item[1], item[0]))
        return

    def popMinHeap(self):
        return heapq.heappop(self.heap)


# Inherit from Heap Class, implements Maximum Heap Object
class MaxHeap(Heap):
    def __init__(self):
        super().__init__()

    def pushMaxHeap(self, item):
        # item = (word, frequency)
        # In Max Heap we work with negative elements , so we prepare item to work with
        item = (item[0], -item[1])
        # If heap already have at least 10 elements compare with max, if greater push current
        if len(self.heap) >= 10:
            # Get Max Element in Heap
            maxElement = self.popMaxHeap()
            # If max element of heap is lower then current item (or grater in the positive context) we will leave it
            if -maxElement[0] >= item[1]:
                # Push max element back into heap
                item = (maxElement[1], -maxElement[0])
        # inserting (value, key) pair to heap, since heap sort items by first value
        heapq.heappush(self.heap, (item[1], item[0]))
        return

    def popMaxHeap(self):
        (key, value) = heapq.heappop(self.heap)
        return -key, value

