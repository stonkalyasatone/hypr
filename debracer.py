from another_lexer import Token
class OpNode:
  """
  represents an operator
  """
  op=""
  arg=[]
  def __init__(s,o,a):
    s.op=o
    s.arg=a
  def __repr__(s):
    return s.op+"("+", ".join([str(i) for i in s.arg])+")"
  def rpn(s):
    return " ".join([i.rpn() for i in s.arg])+" "+s.op+("1" if s.arg==1 else "")
class BaseNode:
  """
  variables or numbers or anything else that doesn't need lower tokens
  """
  val=None
  isvar=False
  def __init__(s,v,i=False):
    s.val=v
    s.isvar=i
  def __repr__(s):
    return ("$" if s.isvar else "")+str(s.val)
  def rpn(s):
    return str(s.val)

  
def parse(tk,variables=[]):
  """
  Converts tokens into ASTs using the Debracer algorithm, among others. Note that as of now some tokens are still left intact.
  """
  #global _tokens
  tokens=tk.copy()
  #done=True
  #NODIFY ALL THE TOKENS!!!1!!1!!!!!11!1111
  for i in range(len(tokens)):
    if tokens[i].ttype=="number":
      try:
        tokens[i]=BaseNode(int(tokens[i].tvalue))
      except:
        tokens[i]=BaseNode(float(tokens[i].tvalue))
      continue
    if tokens[i].ttype=="string":
      tokens[i]=BaseNode(tokens[i].tvalue)
      continue
    if tokens[i].ttype=="word":
      if tokens[i].tvalue in variables:
        tokens[i]=BaseNode(tokens[i].tvalue,True)
        continue
  def scan2(ops):
    nonlocal tokens
    for i in range(len(tokens)):
      if(type(tokens[i])!=Token):continue #At this stage, only tokens can be operators.
      if(tokens[i].tvalue not in ops):continue #We only care about the tokens we're looking for. Ignore everything else.
      if(type(tokens[i-1]) not in [OpNode,BaseNode]):continue #Make sure the left operator has been fully reduced.
      if(type(tokens[i+1]) not in [OpNode,BaseNode]):continue #Make sure the right operator has been fully reduced.
      tokens=tokens[:i-1]+[OpNode(tokens[i].tvalue,[tokens[i-1],tokens[i+1]])]+tokens[i+2:]
      return True #There are more tokens to search for.
    return False#We're done here.
  def scan1(ops):
    nonlocal tokens
    for i in range(len(tokens)):
      if(type(tokens[i])!=Token):continue #At this stage, only tokens can be operators.
      if(tokens[i].tvalue not in ops):continue #We only care about the tokens we're looking for. Ignore everything else.
      if(type(tokens[i-1])!=Token):continue #Make sure the left is NOT part of an expression.
      if(type(tokens[i+1]) not in [OpNode,BaseNode]):continue #Make sure the right operator has been fully reduced.
      tokens=tokens[:i]+[OpNode(tokens[i].tvalue,[tokens[i+1]])]+tokens[i+2:]
      return True #There are more tokens to search for.
    return False#We're done here.
  def scan1f(ops):
    nonlocal tokens
    for i in range(len(tokens)):
      if(type(tokens[i])!=Token):continue #At this stage, only tokens can be operators.
      if(tokens[i].tvalue not in ops):continue #We only care about the tokens we're looking for. Ignore everything else.
      if(type(tokens[i-1]) not in [OpNode,BaseNode]):continue #Make sure the left operator has been fully reduced.
      tokens=tokens[:i-1]+[OpNode(tokens[i].tvalue,[tokens[i-1]])]+tokens[i+1:]
      return True #There are more tokens to search for.
    return False#We're done here.
  
  def debrace():
    nonlocal tokens
    for i in range(len(tokens)):
      if(type(tokens[i])!=Token):continue #At this stage, only tokens can be braces.
      if(tokens[i].tvalue!="("):continue #We only care about "(". If you feel pain when you see unmatched braces, here you go: ")"
      if(type(tokens[i+2])!=Token):continue
      if(tokens[i+2].tvalue!=")"):continue
      tokens=tokens[:i]+[tokens[i+1]]+tokens[i+3:]
      return True
    return False
  while True:
    #casually adding support for operators that I'm not even ready to implement yet
    #just because why not
     
    if scan1(["-","~"]):continue
    if scan2(["**"]):continue
    if scan2(["*","/","//","%"]):continue
    if scan2(["+","-"]):continue
    if scan2(["<<",">>"]):continue
    if scan2(["&"]):continue
    if scan2(["^"]):continue
    if scan2(["|"]):continue
    if scan2([">","<",">=","<=","==","!="]):continue
    if scan2(["="]):continue
    if debrace():continue
    break
  return tokens

      
      
