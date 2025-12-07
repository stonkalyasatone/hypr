symbols=["//","**","++","--",">=","<=","==","!=","+=","-=","*=","/="]+list("!@#$%^&*()-+=[]\\{}|:;\'<>?,./")
symbol_chars=list(set(list("".join(symbols))))
class Token:
  ttype=""
  tvalue=""
  def __init__(s,t,v):
    s.ttype=t
    s.tvalue=v
  def __repr__(s):
    return f"('{s.ttype}':'{s.tvalue}')"
def tokenise(code):
  """
  Turns code into tokens.
  In comes code, out comes tokens. Easy as that.
  """
  ctv=""
  ctt=""
  tokens=[]
  idx=0
  isstr=False
  #This new tokeniser can support symbols of longer lengths! Also words!
  while idx<len(code):
    c=code[idx]
    if isstr:
      if c=="\\":
        idx+=1
        if(code[idx]=="n"):
          ctv+="\n"
        elif(code[idx]=="t"):
          ctv+="\t"
        elif(code[idx]=="h"):
          ctv+="#"
        elif(code[idx]=="l"):
          ctv+="@"
        elif(code[idx]=="s"):
          ctv+=";"
        elif(code[idx]=="q"):
          ctv+='"'
        else:
          ctv+=code[idx]    
      elif c=='"':
        isstr=False
      else:
        ctv+=c
      idx+=1     
    else:
      if c=="#":
        while(((code+"\n")[idx])!="\n"):
          idx+=1
      elif c in "0123456789.":
        if ctt=="word":
          ctv+=c
        elif ctt!="number":
          tokens+=[Token(ctt,ctv)]
          ctt="number"
          ctv=c
        else:
          ctv+=c
        idx+=1
      elif c=="\n":
        tokens+=[Token("EOL",""),Token("SOL","")]
        idx+=1
      elif c==" " or c=="\t":
        #purge the previous token
        tokens+=[Token(ctt,ctv)]
        ctt=""
        ctv=""
        idx+=1
      elif c=='"':
        tokens+=[Token(ctt,ctv)]
        ctt="string"
        ctv=""
        isstr=True
        idx+=1
      elif c in symbol_chars:
        if ctt!="symbol":
          tokens+=[Token(ctt,ctv)]
          ctt="symbol"
          ctv=c
          idx+=1
        else:
          if ctv+c not in symbols:
            tokens+=[Token(ctt,ctv)]
            ctv=""
            #idx is not modified here because the new character has to be processed differently
          else:
            ctv+=c
            idx+=1
      elif c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
        if ctt!="word":
          tokens+=[Token(ctt,ctv)]
          ctt="word"
          ctv=c
          idx+=1
        else:
          ctv+=c
          idx+=1
      else:
        idx+=1
        raise Warning(f"Unexpected character '{c}' will be ignored in tokenization.")
  tokens+=[Token(ctt,ctv)]
  tokens=[i for i in tokens if i.ttype!='']
  return [Token("SOL","")]+tokens+[Token("EOL","")]

        
    
