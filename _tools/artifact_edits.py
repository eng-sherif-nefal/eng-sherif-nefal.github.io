"""Make small edit_version edits for the Claude artifact copy from two versions of index.html.
Usage: python3 -I _tools/artifact_edits.py OLD_index.html NEW_index.html > edits.json
The artifact's brand blocks (.brx) are kept identical to index.html, so the same edits apply there.
"""
import json,re,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from brands_sync import find_brx,CFG
a=open(sys.argv[1]).read();b=open(sys.argv[2]).read()
def parts(seg):
    i=seg.find('<div class="ch">');j=seg.find('</div>',i)+6
    bos=re.findall(r'(<div class="bo" data-b="([^"]+)">.*?</div></div>)(?=<div class="bo"|</div>$)',seg,re.S)
    return seg[i:j],[(n,x) for x,n in bos]
E=[]
for t in CFG['types']:
    r1=find_brx(a,t);r2=find_brx(b,t)
    if not r1 or not r2: continue
    A=a[r1[0]:r1[1]];B=b[r2[0]:r2[1]]
    if A==B: continue
    ca,ba=parts(A);cb,bb=parts(B);da=dict(ba);db=dict(bb)
    if ca!=cb:E.append({'old_text':ca,'new_text':cb})
    prev=None
    for n,x in bb:
        if n in da:
            if da[n]!=x:E.append({'old_text':da[n],'new_text':x})
        elif prev is None:
            # first block is new: insert right after the chips/other-name input part
            mid=A[A.find('</div>',A.find('<div class="ch">'))+6:]
            k=mid.find('<div class="bo"');anchor=mid[:k] if k>=0 else mid[:-6]
            E.append({'old_text':anchor,'new_text':anchor+x})
        else:E.append({'old_text':db[prev],'new_text':db[prev]+x})
        prev=n
    for n,x in ba:
        if n not in db:E.append({'old_text':x,'new_text':''})
t=a
for e in E:
    if t.count(e['old_text'])!=1: sys.exit('NOT UNIQUE: '+e['old_text'][:80])
    t=t.replace(e['old_text'],e['new_text'])
if t!=b:
    # fall back: whole-block replacements per changed type
    E=[]
    for ty in CFG['types']:
        r1=find_brx(a,ty);r2=find_brx(b,ty)
        if r1 and r2 and a[r1[0]:r1[1]]!=b[r2[0]:r2[1]]:E.append({'old_text':a[r1[0]:r1[1]],'new_text':b[r2[0]:r2[1]]})
print(json.dumps(E,ensure_ascii=False))
