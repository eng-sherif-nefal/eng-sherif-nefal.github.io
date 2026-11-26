"""Read Nefal price list (xlsx) brand sheets -> brands dict per form type."""
import re,openpyxl,json,sys
INV=re.compile(r'انفرتر|إنفرتر|أنفرتر|انفيرتر|أنفيرتر|إنفيرتر|inverter',re.I)
REG=re.compile(r'عادي')
def norm_mode(v):
    v=re.sub(r'\s+','',str(v))
    if 'بارد' in v and 'حار' in v: return 'حار / بارد'
    if 'بارد' in v: return 'بارد فقط'
    return None
def ttype(t):
    s=t.lower()
    if 'دكت' in t or 'الدكــت' in t or 'دكــت' in t or 'duct' in s: return 'cen'
    if 'package' in s or 'باكدج' in t: return 'pkg'
    if 'مركزي' in t or 'المركزية' in t: return 'pkg'
    if 'مخفي' in t: return 'ksd'
    if 'كاسيت' in t: return 'cas'
    if 'دولابي' in t: return 'flr'
    if 'جدار' in t or 'split' in s: return 'wal'
    return None
def parse(path):
    wb=openpyxl.load_workbook(path,read_only=True,data_only=True)
    names=wb.sheetnames
    i0=names.index('KDK') if 'KDK' in names else 0
    out={'units':{},'fans':[],'desert':[]}
    for sh in names[i0:]:
        ws=wb[sh];rows=[[c for c in r] for r in ws.iter_rows(values_only=True)]
        heads=[str(c) for r in rows for c in r if isinstance(c,str)]
        joined=' | '.join(heads)
        if 'FAN' in joined.upper() and 'CFM' in joined.upper() and not ttype(joined):
            if any(_isdata(r) for r in rows): out['fans'].append(sh)
            continue
        if 'CFM' in joined.upper():
            if any(_isdata(r) for r in rows): out['desert'].append(sh)
            continue
        ty=None;op=None;mode=None
        for r in rows:
            vals=[c for c in r if c not in (None,'')]
            if not vals: continue
            strs=[v for v in vals if isinstance(v,str)]
            if len(vals)==1 and isinstance(vals[0],str):
                t=vals[0].strip();nt=ttype(t)
                if nt: ty=nt;op=None;mode=None
                if INV.search(t): op='انفرتر'
                elif REG.search(t): op='On/Off (عادي)'
                continue
            if any(isinstance(v,str) and ('القدرة' in v) for v in vals): continue
            if ty and _isdata(r):
                m=None
                for v in vals:
                    if isinstance(v,str):
                        mm=norm_mode(v)
                        if mm: m=mm;break
                if m: mode=m
                d=out['units'].setdefault(ty,{}).setdefault(sh,{'c':set(),'m':set()})
                if op: d['c'].add(op)
                if mode: d['m'].add(mode)
    for ty in out['units']:
        for sh in out['units'][ty]:
            d=out['units'][ty][sh];d['c']=sorted(d['c'],key=lambda x:0 if x=='انفرتر' else 1);d['m']=sorted(d['m'],key=lambda x:0 if x=='بارد فقط' else 1)
    return out
def _isdata(r):
    nums=[c for c in r if isinstance(c,(int,float)) and c>50]
    caps=[c for c in r if isinstance(c,str) and re.search(r'طن|حصان|\d',c)]
    return len(nums)>=2
if __name__=='__main__':
    print(json.dumps(parse(sys.argv[1]),ensure_ascii=False,indent=1))
