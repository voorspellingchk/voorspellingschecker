"""Generate the English editor from the Dutch (canonical) editor.
Usage: python3 make_en.py <nl editor> <en editor out>
Order: en_lines.json (whole lines) -> en_code.json (exact replacements, longest first)
-> en_text.json (short phrases, only inside human-text segments)."""
import json,re,sys,os
D=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,D)
from extract import segments,human
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
ld=lambda f:json.load(open(os.path.join(D,f),encoding='utf-8'))
warn=[]
lines=s.split('\n');LP={a:b for a,b in ld('en_lines.json')}
for a in LP:
    if a not in lines: warn.append('line not found: '+a[:70])
s='\n'.join(LP.get(l,l) for l in lines)
for k,v in sorted(ld('en_code.json'),key=lambda kv:-len(kv[0])):
    if k not in s: warn.append('code key not found: '+k[:70])
    s=s.replace(k,v)
T=ld('en_text.json');keys=sorted(T,key=len,reverse=True)
segs=sorted({(a,b) for a,b,t in segments(s) if human(t)});merged=[]
for a,b in segs:
    if merged and a<merged[-1][1]: merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
    else: merged.append((a,b))
out=[];pos=0
for a,b in merged:
    out.append(s[pos:a]);t=s[a:b]
    for i,k in enumerate(keys):
        if k in t: t=t.replace(k,'\x00%d\x00'%i)
    out.append(re.sub('\x00(\\d+)\x00',lambda m:T[keys[int(m.group(1))]],t));pos=b
out.append(s[pos:]);s=''.join(out)
open(dst,'w',encoding='utf-8').write(s)
for w in warn: print('WARN',w,file=sys.stderr)
print('ok',dst)
