class Node:
    def __init__(self, label = None):
        self.label = label
        self.children = {}
        self.modeClass = ""
	# you may want to add additional fields here...

def breadth_first_search(root):

    '''
    given the root node, will complete a breadth-first-search on the tree, returning the value of each node in the correct order
    '''
    tree = ''
    NodeList = [root]
    while len(NodeList) != 0:
        length = len(NodeList)
        for i in range(0, length):
            node = NodeList[0]
            del NodeList[0]
        #value = '%d ' %node.label
            tree += str(node.label) + "-"+ str(node.modeClass) + "   "
            if node.children != None:
                for i in node.children.keys():
                    NodeList.append(node.children[i])
        tree += "\n"
    return tree