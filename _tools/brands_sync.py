"""Sync the form's brand choices with the Nefal price list.
Usage: python3 _tools/brands_sync.py <price_list.xlsx> [html ...]
Default html = index.html. Rewrites the brand blocks (.brx) of the synced types, then rebuilds en.html.
Prints a JSON report {added:{type:[...]}, removed:{...}, changed:{...}}.
"""
import json,re,os,sys,subprocess
H=os.path.dirname(os.path.abspath(__file__));R=os.path.dirname(H)
sys.path.insert(0,H)
from brands_parse import parse
CFG=json.load(open(os.path.join(H,'brands_config.json')))
NAMES={'ksd':'مخفي (كونسيلد)','wal':'جداري (سبليت)','cas':'كاسيت','flr':'دولابي','cen':'سنترال سبليت','pkg':'باكدج','des':'صحراوي','fan':'مراوح شفط'}
def disp(sh): return CFG['display'].get(sh,sh.strip())
def order(names):
    o=CFG['order'];return sorted(names,key=lambda n:(o.index(n) if n in o else 999,n))
def key(b,i):
    k=re.sub(r'[^A-Za-z0-9]','',b);return k or ('x%d'%i)
def find_brx(s,t):
    i=s.find('<input type="checkbox" name="br_'+t+'"')
    if i<0: return None
    j=s.rfind('<div class="brx">',0,i);d=0
    for m in re.finditer(r'<div\b|</div>',s[j:]):
        d+=1 if m.group()=='<div' else -1
        if d==0: return j,j+m.end()
def radios(nm,opts):
    one=len(opts)==1
    return ''.join('<label><input type="radio" name="%s" value="%s"%s>%s</label>'%(nm,o,' checked' if one else '',o) for o in opts)
def build(t,old,brands):
    """brands: list of (name,c,m)"""
    a=old.find('<div class="ch">');b=old.find('</div>',a)
    head=old[:a]
    tail_start=b+len('</div>')
    # bool+input part up to first bo or end
    rest=old[tail_start:]
    k=rest.find('<div class="bo"')
    mid=rest[:k] if k>=0 else rest[:-len('</div>')]
    chips=''.join('<label><input type="checkbox" name="br_%s" value="%s">%s</label>'%(t,n,n) for n,_,_ in brands)
    chips+='<label><input type="checkbox" name="br_%s" value="أخرى">أخرى</label>'%t
    bos=''
    for i,(n,c,m) in enumerate(brands):
        if not c and not m: continue
        kk=key(n,i);x='<div class="bo" data-b="%s"><b>%s</b>'%(n,n)
        if c: x+='<span class="bol">التشغيل <span class="req">*</span></span><div class="ch" data-bo="1">'+radios('bo_%s_%s_c'%(t,kk),c)+'</div>'
        if m: x+='<span class="bol">بارد / حار <span class="req">*</span></span><div class="ch" data-bo="1">'+radios('bo_%s_%s_m'%(t,kk),m)+'</div>'
        bos+=x+'</div>'
    return head+'<div class="ch">'+chips+'</div>'+mid+bos+'</div>'
def current(s,t):
    r=find_brx(s,t);seg=s[r[0]:r[1]]
    names=[v for v in re.findall(r'name="br_%s" value="([^"]+)"'%t,seg) if v!='أخرى']
    out={}
    for i,n in enumerate(names):
        kk=key(n,i)
        out[n]=(re.findall(r'name="bo_%s_%s_c" value="([^"]+)"'%(t,kk),seg),re.findall(r'name="bo_%s_%s_m" value="([^"]+)"'%(t,kk),seg))
    return out
def apply(html,data):
    s=html;rep={'added':{},'removed':{},'changed':{}}
    for t in CFG['types']:
        if t=='des': src={disp(x):([],[]) for x in data['desert']}
        elif t=='fan': src={disp(x):([],[]) for x in data['fans']}
        else: src={disp(x):(v['c'],v['m']) for x,v in data['units'].get(t,{}).items()}
        if not src: continue  # never wipe a type if the file has nothing for it
        r=find_brx(s,t)
        if not r: continue
        cur=current(s,t)
        lst=[(n,)+tuple(src[n]) for n in order(list(src))]
        new=build(t,s[r[0]:r[1]],lst)
        a=[n for n in src if n not in cur];d=[n for n in cur if n not in src]
        ch=[n for n in src if n in cur and (sorted(cur[n][0])!=sorted(src[n][0]) or sorted(cur[n][1])!=sorted(src[n][1]))]
        if a: rep['added'][NAMES[t]]=a
        if d: rep['removed'][NAMES[t]]=d
        if ch: rep['changed'][NAMES[t]]=ch
        s=s[:r[0]]+new+s[r[1]:]
    return s,rep
if __name__=='__main__':
    xlsx=sys.argv[1];files=sys.argv[2:] or [os.path.join(R,'index.html')]
    data=parse(xlsx);reps=[]
    for f in files:
        h=open(f).read();n,rep=apply(h,data)
        if n!=h: open(f,'w').write(n)
        reps.append(rep)
    if os.path.join(R,'index.html') in [os.path.abspath(f) for f in files]:
        subprocess.run([sys.executable,os.path.join(H,'build.py')],check=True)
    print(json.dumps(reps[0],ensure_ascii=False))
