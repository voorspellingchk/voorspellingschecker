import re,json,sys
def segments(s):
    """yield (start,end,text) for human-text segments in the file"""
    out=[]
    # split template/text: find text between > and < (HTML text nodes, also inside template literals)
    for m in re.finditer(r'>([^<>`]*?[A-Za-zÀ-ÿ][^<>`]*?)<',s):
        t=m.group(1)
        if '${' in t or '{' in t and '}' in t and ';' in t: 
            # split around ${...}
            pass
        out.append((m.start(1),m.end(1),t))
    # quoted JS strings
    for m in re.finditer(r"'((?:[^'\\\n]|\\.){2,}?)'|\"((?:[^\"\\\n]|\\.){2,}?)\"",s):
        g=m.group(1) if m.group(1) is not None else m.group(2)
        st=m.start(1) if m.group(1) is not None else m.start(2)
        out.append((st,st+len(g),g))
    return out
STOP=re.compile(r'^[\w\-.#:\[\]=*>+~ ,()%/@!$|&?^\\]*$')
def human(t):
    t2=t.strip()
    if len(t2)<2 or not re.search(r'[A-Za-zÀ-ÿ]{2}',t2): return False
    if re.match(r'^(https?:|data:|#|\.|--|var\(|rgba?\(|\d)',t2): return False
    if re.search(r'[{};]\s*$',t2) and ':' in t2: return False  # css
    if re.fullmatch(r'[a-z0-9_\-]+',t2): return False  # identifiers/keys
    if re.fullmatch(r'[a-zA-Z_$][\w$]*(\.[\w$]+)+',t2): return False
    if re.search(r'^[\w\-]+=',t2): return False
    if re.fullmatch(r'[a-z\-]+(\s[a-z\-]+)*',t2) and len(t2.split())<=3 and not re.search(r'[ëéèï]',t2): 
        # lowercase short: could be classnames like "btn ghost" or words like "nu" - keep if dutch-looking
        return bool(re.search(r'\b(de|het|een|en|van|nog|niet|geen|op|nu|jaar|bron|gepost|vandaag|morgen)\b',t2))
    return True
if __name__=='__main__':
    s=open(sys.argv[1],encoding='utf-8').read()
    segs=[x for x in segments(s) if human(x[2])]
    uniq=sorted(set(x[2].strip() for x in segs))
    print(len(segs),len(uniq))
    json.dump(uniq,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
