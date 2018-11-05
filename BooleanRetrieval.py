from os import listdir
from os.path import isfile, join
import pickle
from InvertedIndex import TreeNodeType, TreeNode, inverted_index, DoubleListNode, DoubleList


def string_parentheses_parse(string):
    retval = []
    first = string.find("(")
    beginning = 0
    while first != -1:
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


def BooleanRetrieval():
    index_object = inverted_index()
    with open('/home/student/HW1/index', 'rb') as f:
        index_object.index = pickle.load(f)
    with open('/home/student/HW1/index_dict', 'rb') as f:
        index_object.docno_dict = pickle.load(f)
    index_object.populate_full_list()
    with open('/data/HW1/BooleanQueries.txt', 'rb') as q:
        with open('/home/student/HW1/Part_2.txt') as f:
            queries = q.readlines()
            for query_string in queries:
                query_string_clean = query_string.strip()
                query_tree = make_query(query_string_clean)
                reslist = index_object.eval(query_tree)
                for x in reslist:
                    sstr = str(index_object.docno_dict[x]) + " "
                if sstr.endswith(" "):
                    sstr = sstr[:-1]
                sstr += "\n"
                f.write(sstr)

