import parse

global ValueDict
def preprocess(examples):
  data_list = parse.parse(examples)
  global ValueDict
  ValueDict = {}
  ValueCounter = {}

  for attribute in data_list[0]:
  	ValueDict[attribute] = {}
  	ValueCounter[attribute] = 0

  for row in data_list:
    for attribute, value in row.iteritems():
      if not ValueDict[attribute].has_key(value):
        ValueCounter[attribute] += 1
        ValueDict[attribute][value] = ValueCounter[attribute]

  print '**********\nrow 0 before preprocess:\n', data_list[0]

  for row in data_list:  	
    for attribute, value in row.iteritems():
      row[attribute] = ValueDict[attribute][value]

  print '**********\nValueDict:\n', ValueDict
  print '**********\nrow 0 after preprocess:\n', data_list[0]
  return data_list
  
preprocess("house_votes_84.data")