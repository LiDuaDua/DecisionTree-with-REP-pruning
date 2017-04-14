# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - dictionary containing the children where the key is child number (1,...,k) and the value is the actual node object
# if node has no children, self.children = None
# value - value at the node
#
#
# The values for bfs should be returned as simply a string of value space value space value. For example if the tree looks like the following:
#     5
#   2   3
#
# The tree data structure is a node with value 5, with a dictionary of children {1: b, 2: c} where b is a node with value 2 and c is a node with value 3.  Both b and c have children of None.
# The bfs traversal of the above tree should return the string '5 2 3'
class Node:
	def __init__(self):
		self.value = None
		self.children = None

	def get_value(self):
		
		'''
		given a node, will return the value at this node
		'''
		
		return self.value

	def get_children(self):
		
		'''
		given a node, will return the children of this node
		'''
		
		return self.children

def breadth_first_search(root):
	
	'''
	given the root node, will complete a breadth-first-search on the tree, returning the value of each node in the correct order
	'''
	
	tree = ''
	NodeList = [root]
	while len(NodeList) != 0:
		node = NodeList[0]
		del NodeList[0]
		value = '%d ' %node.value
		tree += value
		if node.children != None:
			for i in range(1, len(node.children) + 1):
				NodeList.append(node.children[i])
	return tree

def tester():
	a = Node()
	a.value = 5
	b = Node()
	b.value = 7
	a.children = {1: b}
	print str(a.get_value()) + ' should be 5.'
	print str(a.get_children()) + ' should be {1: ' + str(b) + '}.'
	print str(breadth_first_search(a)) + ' should be 5 7.'

def bfs():
	a = Node()
	a.value = 17
	b = Node()
	b.value = 11
	c = Node()
	c.value = 33
	d = Node()
	d.value = 6
	e = Node()
	e.value = 15
	f = Node()
	f.value = 24
	g = Node()
	g.value = 36
	h = Node()
	h.value = 3
	i = Node()
	i.value = 7
	j = Node()
	j.value = 13
	k = Node()
	k.value = 16
	l = Node()
	l.value = 22
	a.children = {1: b, 2: c}
	b.children = {1: d, 2: e}
	c.children = {1: f, 2: g}
	d.children = {1: h, 2: i}
	e.children = {1: j, 2: k}
	f.children = {1: l}
	print str(breadth_first_search(a)) + ' should be 17 11 33 6 15 24 36 3 7 13 16 22.'

#tester()
#bfs()
