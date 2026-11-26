import json,re,sys,os
H=os.path.dirname(os.path.abspath(__file__));R=os.path.dirname(H)
src=os.path.join(R,'index.html')
s=open(src).read()
D=json.load(open(os.path.join(H,'dict.json')))
ver=re.search(r'إصدار (R\d+)',s).group(1)
D={k.replace('R30',ver):v.replace('R30',ver) for k,v in D.items()}
js=open(os.path.join(H,'i18n.js')).read().replace('__DICT__',json.dumps(D,ensure_ascii=False))
e=s
e=re.sub(r'<html[^>]*>','<html lang="en" dir="ltr">',e,count=1)
e=e.replace('<a class="lng264" href="en.html?v='+ver+'">English</a>','<a class="lng264" href="./?v='+ver+'">العربية</a>')
assert 'lng264' in e
i=e.find('<script>\n{\nconst frm=');assert i>0
e=e[:i]+'<script>'+js+'</script>\n'+e[i:]
assert e.count('function text(){')==1
e=e.replace('function text(){','function text(){return window.__trT(text0())}function text0(){',1)
open(os.path.join(R,'en.html'),'w').write(e)
print('built',ver,len(e))
