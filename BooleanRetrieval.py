from os import listdir
from os.path import isfile, join
import pickle
from InvertedIndex import inverted_index


class TreeNodeType(Enum):
    AND = 1
    OR = 2
    NOT = 3
    DATA = 4


class TreeNode(object):
    def __init__(self, type, data=None, left=None, right=None):
        self.type = type
        self.data = data
        self.left = left
        self.right = right

    def eval(self, index_object):
        if self.type == TreeNodeType.DATA:
            return index_object.index[query.data]
        retval = []
        left_ret = index_object.eval(self.left)
        right_ret = index_object.eval(self.right)
        i = j = 0
        if self.type == TreeNodeType.AND:
            while i < len(left_ret) and j < len(right_ret):
                if left_ret[i] == right_ret[j]:
                    retval.append(left[i])
                    i += 1
                    j += 1
                elif left_ret[i] < right_ret[j]:
                    i += 1
                else:
                    j += 1
        if self.type == TreeNodeType.OR:
            while i < len(left_ret) or j < len(right_ret):
                if j >= len(right_ret) or (i < len(left_ret) and left_ret[i] < right_ret[j]):
                    retval.append(left[i])
                    i += 1
                elif i >= len(left_ret) or (j < len(right_ret) and left_ret[i] > right_ret[j]):
                    retval.append(right_ret[j])
                    j += 1
                else:
                    retval.append(left_ret[i])
                    i += 1
                    j += 1
        if self.type == TreeNodeType.NOT:
            while i < len(left_ret):
                while j < len(right_ret) and right_ret[j] < left_ret[i]:
                    j += 1
                if j < len(right_ret) and right_ret[j] > left_ret[i]:
                    retval.append(left_ret[i])
                i += 1
        return retval


def string_parentheses_parse(string):
    retval = []
    first = string.find("(")
    beginning = 0
    while first != -1:
        if first != beginning:
            retval += string[beginning: first - 1].split()
        i = first
        parentheses_level = 1
        start = first + 1
        end = 0
        while parentheses_level > 0:
            i += 1
            if string[i] == "(":
                parentheses_level += 1
            if string[i] == ")":
                parentheses_level -= 1
        end = i
        retval.append(string_parentheses_parse(string[start: end]))
        beginning = i + 1
        first = string[beginning: -1].find("(")
        if first != -1:
            first += beginning
    retval += string[beginning:].split()
    return retval


def make_query_aux(lres):
    if len(lres) == 1:
        if isinstance(lres[0], list):
            return make_query_aux(lres[0])
        else:
            tree_node = TreeNode(TreeNodeType.DATA, data=lres[0])
            return tree_node
    if "OR" in lres:
        left_side = lres[:lres.index("OR")]
        right_side = lres[lres.index("OR")+1:]
        tree_node = TreeNode(TreeNodeType.OR, left=make_query_aux(left_side), right=make_query_aux(right_side))
        return tree_node
    if "AND" in lres:
        left_side = lres[:lres.index("AND")]
        right_side = lres[lres.index("AND") + 1:]
        tree_node = TreeNode(TreeNodeType.AND, left=make_query_aux(left_side), right=make_query_aux(right_side))
        return tree_node
    if "NOT" in lres:
        left_side = lres[:lres.index("NOT")]
        right_side = lres[lres.index("NOT") + 1:]
        tree_node = TreeNode(TreeNodeType.NOT, left=make_query_aux(left_side), right=make_query_aux(right_side))
        return tree_node


def make_query(string):
    list_res = string_parentheses_parse(string)
    return make_query_aux(list_res)


def BooleanRetrieval(input_dir, output_dir):
    index_object = inverted_index(output_dir + 'index')
    with open(output_dir +'index_dict', 'rb') as f:
        index_object.docno_dict = pickle.load(f)
    with open(input_dir + 'BooleanQueries.txt', 'rb') as q:
        with open(output_dir + 'Part_2.txt', 'wb') as f:
            queries = q.readlines()
            for query_string in queries:
                query_string_clean = query_string.strip().decode('ASCII')
                query_tree = make_query(query_string_clean)
                reslist = query_tree.eval(index_object)
                sstr = ""
                for x in reslist:
                    sstr += str(index_object.docno_dict[x]) + " "
                if sstr.endswith(" "):
                    sstr = sstr[:-1]
                sstr += "\n"
                f.write(sstr.encode('ASCII'))


if __name__ == "__main__":
    input_dir = r"/data/HW1/"
    output_dir = r'/home/student/HW1/'
    BooleanRetrieval(input_dir, output_dir)
