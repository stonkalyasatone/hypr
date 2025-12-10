#c=input("Newline character? (should be known while compiling)")
STYLE_ERROR="\033[31m"
STYLE_INPUT="\033[33m\033[1m"
STYLE_SUCCESS="\033[32m"
CLEAR="\033[0m"
from time import time
while True:
  try:
    a=int(input(STYLE_INPUT+"Allot size? "+CLEAR))
    if a<0:
      print(STYLE_ERROR,"Cannot allocate a negative number of variables.",CLEAR)
    else:
      break
  except:
    print(STYLE_ERROR,"What you entered wasn't a number.",CLEAR)
    
while True:
  try:
    with open(input(STYLE_INPUT+"Compiler output file? "+CLEAR)) as f:
      code=f.read()
    break
  except OSError as e:
    print(STYLE_ERROR,"Failed to open file, please try again",CLEAR)
    print(STYLE_ERROR,"Reason:",e,CLEAR)

code=code.split("\n")
pointer=0#Instruction Pointer
memory=[None]*a#Allot passing will be done in the future :)
rstack=[]#Return stack, for jsr and rtn
vstack=[]#Value stack, intended to store arguments,
#though technically you can store literally anything
estack=[]#Expression stack, for operators
#Definetly consider merging this into vstack, leaving us with a 2-stack system
keys={'0':0,'1':1,'2':2,'3':3,
      '4':4,'5':5,'6':6,'7':7,
      '8':8,'9':9,'a':10,'b':11,
      'c':12,'d':13,'e':14,'f':15}
import math
EXEC_TIMER=time()
def strlit(s):
  S=""
  for i in range(0,len(s)-1,2):
    c=keys[s[i]]*16+keys[s[i+1]]
    S+=chr(c)
  return S
#encountered=set()
def run(token):
  #encountered.add(token)
  #return
  global pointer,memory,rstack,vstack,estack
  if token=="-u":
    estack.append(-estack.pop())
  if token=="jmp":
    pointer=estack.pop()-1
  if token=="jsr":
    rstack.append(pointer)
    pointer=estack.pop()-1
  if token=="rtn":
    pointer=rstack.pop()
  if token=="<=":
    arg1=estack.pop()
    arg0=estack.pop()
    estack.append(arg0<=arg1)
  if token==">=":
    arg1=estack.pop()
    arg0=estack.pop()
    estack.append(arg0>=arg1)
  if token=="<":
    arg1=estack.pop()
    arg0=estack.pop()
    estack.append(arg0<arg1)
  if token==">":
    arg1=estack.pop()
    arg0=estack.pop()
    estack.append(arg0>arg1)
  if token=="==":
    arg1=estack.pop()
    arg0=estack.pop()
    estack.append(arg0==arg1)
  if token=="!=":
    arg1=estack.pop()
    arg0=estack.pop()
    estack.append(arg0!=arg1)
  if token=="+":
    arg1=estack.pop()
    arg0=estack.pop()
    try:
      estack.append(arg0+arg1)
    except:
      estack.append(str(arg0)+str(arg1))
  if token=="-":
    arg1=estack.pop()
    arg0=estack.pop()
    estack.append(arg0-arg1)
  if token=="*":
    arg1=estack.pop()
    arg0=estack.pop()
    estack.append(arg0*arg1)
  if token=="/":
    arg1=estack.pop()
    arg0=estack.pop()
    estack.append(arg0/arg1)
  if token=="//":
    arg1=estack.pop()
    arg0=estack.pop()
    estack.append(arg0//arg1)
  if token=="%":
    arg1=estack.pop()
    arg0=estack.pop()
    estack.append(arg0%arg1)
  if token==">s":
    vstack.append(estack.pop())
    #print("Pushed",vstack[-1])
  if token=="<s":
    estack.append(vstack.pop())
  if token=="?":
    estack.append(memory[estack.pop()])
  if token=="=":
    arg1=estack.pop()
    arg0=estack.pop()
    memory[arg0]=arg1
  if token=="isf":
    if(not estack.pop()):
      pointer+=1
  if token=="invoke":
    op=estack.pop()
    if op=="print":
      print(vstack.pop())
    if op=="input":
      vstack.append(input(vstack.pop()))
    if op=="int":
      vstack.append(int(vstack.pop()))
    if op=="float":
      vstack.append(float(vstack.pop()))
    if op=="str":
      vstack.append(str(vstack.pop()))
    if op=="round":
      vstack.append(round(vstack.pop()))
    if op=="log":
      vstack.append(math.log(vstack.pop(),10))
def handle(token):
  global estack
  if len(token)==0:
      return
  if token[0]=='"':
    #String literal
    estack.append(strlit(token[1:]))
  elif token[0]=='f':
    #Floating-point literal
    estack.append(float(token[1:]))
  elif token[0] in "0123456789":
    #Integer literal
    estack.append(int(token))
  else:
    #Command token
    run(token)
while pointer<len(code):
  line=code[pointer]
  #print(line)
  line=line.split(" ")
  #print("Line:",line)
  for token in line:
    handle(token)
    #print("T:",token,"S:",estack)
  pointer+=1
EXEC_TIMER=(time()-EXEC_TIMER)*1000
print(STYLE_SUCCESS,"Execution successful in",f"{EXEC_TIMER:.3f}","ms",CLEAR)
try:
  input("Press any key to continue... (or press Ctrl+C)")#pause a little bit
except:
  exit()
