import re,sys,os
D=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,D)
from extract import segments,human
g=open(sys.argv[1],encoding='utf-8').read();nl=open(sys.argv[2],encoding='utf-8').read()
E=set(open(os.path.join(D,'en_vocab.txt'),encoding='utf-8').read().split())
words=lambda s:set(w.lower() for a,b,t in segments(s) if human(t) for w in re.findall(r'[A-Za-zÀ-ÿ]{3,}',re.sub(r'\$\{[^}]*\}','',t)))
susp=sorted(w for w in words(nl) if w not in E)
for w in susp:
    m=re.search(r'(?<![A-Za-zÀ-ÿ])'+w+r'(?![A-Za-zÀ-ÿ])',g,flags=re.I)
    if m: print(w,'|',g[max(0,m.start()-50):m.end()+40].replace('\n',' '))
