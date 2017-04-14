import node
from node import Node 
import math
import parse
import random
import copy


def preprocess(examples):
  data_list = copy.deepcopy(examples)
  ProbDict = {}
  for attribute in examples[0]:
    ProbDict[attribute] = {'total': 0}

  for row in examples:
    for attribute, value in row.iteritems():
      if not value == '?':
        ProbDict[attribute]['total'] += 1
        if ProbDict[attribute].has_key(value):
          ProbDict[attribute][value] += 1.0
        else:
          ProbDict[attribute][value] = 1.0

  #print 'ProbDict: ', ProbDict
  for row, table in ProbDict.iteritems():
    for attribute, value in table.iteritems():
      if not attribute == 'total':
        table[attribute] = table[attribute]/table['total']

  for row in examples:
    for attribute, value in row.iteritems():
      if value == '?':
        num = 0.0
        threshod = random.random()
        for key, prob in ProbDict[attribute].iteritems():
          num += prob
          if not num < threshod and not key == 'total':
            #print 'row[attribute]: ', row[attribute], '-> key: ', key
            row[attribute] = key
            break

  return examples

def pureClass(examples):
  if len(examples) == 1:
    return True
  else:
    firstClass = examples[0]['Class']
    for row in examples[1 : ]:
      if row["Class"] != firstClass:
        return False
    return True

def sameAtt(examples):
  arrs = examples[0].keys();
  arrs.remove('Class')

  for arr in arrs:
    value = examples[0][arr]
    for example in examples:
      if example[arr] != value:
        return False
  return True

def ID3(examples, default):
    examples = preprocess(examples)
    return ID3Helper(examples, default)

def ID3Helper(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''

  if (len(examples) == 0):
    return default
  elif(pureClass(examples)):
    return Node(examples[0]['Class'])
  elif(sameAtt(examples)):
    return mode(examples)

  best = bestAtt(examples)
  node = Node(best)
  node.modeClass = mode(examples).label

  subExamples = split(examples, best)

  for subKey in subExamples.keys():
    subNode = ID3(subExamples[subKey], mode(examples))
    node.children[subKey] = subNode

  return node

def bestAtt(examples):
  if(len(examples) == 0):      
    return none

  arrs = examples[0].keys();
  arrs.remove('Class')
  best = None
  bestInformationGain = -1.0

  for arr in arrs:
    subExamples = split(examples, arr)
    subEntropy = 0.0;

    for subKey in subExamples.keys():
      val_prob  = float(len(subExamples[subKey]))/float(len(examples))
      subEntropy += val_prob * entropy(subExamples[subKey])

    informationGain = entropy(examples) - subEntropy
    if informationGain > bestInformationGain:
      best = arr
      bestInformationGain = informationGain
  return best

def split(examples, attribute):
  '''
  return a list containing two lists. The two lists contain the examples splited by the attribute.
  For the examples with a ? attribute, split them into two lists randomly by the ratio of Y-examples and N-examples.
  '''
  subList = {}

  for example in examples:
    if not example[attribute] in subList.keys():
      subList[example[attribute]] = [example]
    else:
      subList[example[attribute]].append(example)

  return subList

def entropy(examples):
  '''
  return entropy of the examples
  '''
  val_freq     = {}
  data_entropy = 0.0

  # Calculate the frequency of each of the values in the target attr
  for record in examples:
      if (val_freq.has_key(record['Class'])):
          val_freq[record['Class']] += 1.0
      else:
          val_freq[record['Class']]  = 1.0

  # Calculate the entropy of the data for the target attribute
  for freq in val_freq.values():
      data_entropy += (-freq/len(examples)) * math.log(freq/len(examples), 2) 
      
  return data_entropy


def mode(examples):
  '''
  return the mode of the examples;
  '''
  classList = getClass(examples)
  label0=0
  label1=0

  for ele in examples:
    if(ele['Class']== classList[0]):
      label0+=1
    else:
      label1+=1
  if label0>=label1:
    node = Node(classList[0])
    node.modeClass = classList[0]
  else:
    node = Node(classList[1])
    node.modeClass = classList[1]
  return node

def getClass(examples):
  class1 = examples[0]['Class']
  for example in examples[1:]:
    if example['Class'] != class1:
      class2 = example['Class']
      return [class1, class2]

def prune(node, examples):
    examples = preprocess(examples)
    pruneHelper(node, examples)

def pruneHelper(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

  #if node is a leaf, return it
  if not notLeaf(node):
    return

  #If validation set is empty, make the node a leaf.
  if len(examples) == 0:
    node.children = {}
    node.label = node.modeClass
    return

  childExamples = split(examples, node.label)

  for childKey in node.children.keys():
    if childKey in childExamples.keys():
      pruneHelper(node.children[childKey], childExamples[childKey])
    else:
      pruneHelper(node.children[childKey], {})

  #After all the children has been traversed, then consider the node itself.
  if pruneAble(node, examples):
    node.children = {}
    node.label = node.modeClass

def pruneAble(node, examples):
  if len(examples) == 0:
    return True 
  '''
  A node can be pruned only when all its children are leaf nodes.
  '''
  for childKey in node.children.keys():
    if notLeaf(node.children[childKey]):
      return False

  '''
  A node should be pruned when test accuracy doesn't reduce after pruning
  '''
  modeNum = 0.0
  for example in examples:
    if example['Class'] == node.modeClass:
      modeNum += 1.0

  if modeNum/len(examples) >= test(node, examples):
    return True;
  return False


def notLeaf(node):
  return len(node.children) != 0

def test(node, examples):
    examples = preprocess(examples)
    return testHelper(node, examples)

def testHelper(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  rightClassified = 0.0

  for example in examples:
    if example['Class'] == evaluate(node, example):
      rightClassified += 1.0
  return rightClassified/len(examples)

def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  if node == None:
    return node;
  if len(node.children) == 0:
    return node.label
  return evaluate(node.children[example[node.label]], example)


