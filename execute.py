code='"5348434e2063616c63756c61746f72 >s\n"7072696e74 invoke\n22 jsr\n36 jmp\n0 1 =\nrtn\n1 <s =\n4 jsr\n2 1 =\n3 2 =\n1 ? 3 ? % 0 != isf\n15 jmp\n1 1 ? 3 ? // =\n0 0 ? 1 + =\n10 jmp\n2 2 ? 0 ? * =\n4 jsr\n3 3 ? 1 + =\n1 ? 1 > isf\n10 jmp\n2 ? >s\nrtn\n4 1 =\n5 1 -u =\n4 4 ? 1 + =\n4 ? >s\n6 jsr\n6 <s =\n6 ? 5 ? <= isf\n24 jmp\n"4e657720486967686c7920436f6d706f73697465204e756d62657220466f756e642120497420697320 4 ? + "207769746820 + 6 ? + "20666163746f72732e + >s\n"7072696e74 invoke\n5 6 ? =\n4 ? 10000 >= isf\nrtn\n24 jmp\n\n'
#Copy output from compiler!
code=code.split("\n")
pointer=0#Instruction Pointer
memory=[None]*10#Allot passing will be done in the future :)
rstack=[]#Return stack, for jsr and rtn
vstack=[]#Value stack, intended to store arguments,
#though technically you can store literally anything
estack=[]#Expression stack, for operators
#Definetly consider merging this into vstack, leaving us with a 2-stack system
keys={'0':0,'1':1,'2':2,'3':3,
      '4':4,'5':5,'6':6,'7':7,
      '8':8,'9':9,'a':10,'b':11,
      'c':12,'d':13,'e':14,'f':15}
def strlit(s):
  S=""
  for i in range(0,len(s)-1,2):
    c=keys[s[i]]*16+keys[s[i+1]]
    S+=chr(c)
  return S
encountered=set()
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
  if token=="*":
    arg1=estack.pop()
    arg0=estack.pop()
    estack.append(arg0*arg1)
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
while pointer<len(code):
  line=code[pointer]
  #print(line)
  line=line.split(" ")
  for token in line:
    if len(token)==0:
      continue
    if token[0]=='"':
      #String literal
      estack.append(strlit(token[1:]))
    else:
      try:
        estack.append(int(token))#Integer literal
      except ValueError:
        try:
          estack.append(float(token))#Floating-point literal
        except ValueError:
          #not a number token
          run(token)
  pointer+=1
