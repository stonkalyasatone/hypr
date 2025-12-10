"""
var i
i=0
while i<=100
  i++
  if i%15==0
    push "FizzBuzz"
    invoke print
    continue
  endc
  if i%5==0
    push "Buzz"
    invoke print
    continue
  endc
  if i%3==0
    push "Fizz"
    invoke print
    continue
  endc
  push i
  invoke print
endl
"""
def coda_onset(c: str):
  """
    Using the Onset-Coda Dynamic Flow Generator, or OCD Flow Generator algorithm
    to handle advanced constructs, like ifs and thens.
  """
  code=c
  code=code.split("\n")
  code=[i.strip() for i in code if i!='']
  out=""
  cstack=[]
  lstack=[]
  cid=-1
  lid=-1
  for line in code:
    temp=line.split()
    if len(temp)==0:
      continue
    if temp[0]=="if":
      cid+=1
      cstack.append((cid,True))
      out+="if "+("".join(temp[1:]))+" then jmp @then"+str(cstack[-1][0])+"\n"
      out+="jmp @else"+str(cstack[-1][0])+"\n"
      out+="@then"+str(cstack[-1][0])+"\n"
    elif temp[0]=="else":
      cstack[-1]=(cstack[-1][0],False)
      out+="jmp @end"+str(cstack[-1][0])+"\n"
      out+="@else"+str(cstack[-1][0])+"\n"
    elif temp[0]=="endc":
      if cstack[-1][1]:
        out+="@else"+str(cstack[-1][0])+"\n"
      out+="@end"+str(cstack[-1][0])+"\n"
      cstack.pop()
    elif temp[0]=="while":
      lid+=1
      lstack.append(lid)
      out+="@loop"+str(lstack[-1])+"\n"
      out+="if "+("".join(temp[1:]))+" then jmp @cntl"+str(lstack[-1])+"\n"
      out+="jmp @endl"+str(lstack[-1])+"\n"
      out+="@cntl"+str(lstack[-1])+"\n"
    elif temp[0]=="continue":
      out+="jmp @loop"+str(lstack[-1])+"\n"
    elif temp[0]=="break":
      out+="jmp @endl"+str(lstack[-1])+"\n"
    elif temp[0]=="endl":
      out+="jmp @loop"+str(lstack[-1])+"\n"
      out+="@endl"+str(lstack[-1])+"\n"
      lstack.pop()
    else:
      out+=line+"\n"
  return out
#[id, has else]
#id
