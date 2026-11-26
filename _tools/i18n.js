/*en264 — English layer: the page logic stays the same, every Arabic text shown is translated*/
(function(){
var D=__DICT__;
var AR=/[؀-ۿ]/;
var L='\\u0621-\\u065F\\u0660-\\u0669\\u0671-\\u06D3';
var keys=Object.keys(D).sort(function(a,b){return b.length-a.length});
function esc(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}
var RX=new RegExp('(^|[^'+L+'])('+keys.map(esc).join('|')+')(?!['+L+'])','g');
var C=new Map();
function tr(s){if(!s||!AR.test(s))return s;if(C.has(s))return C.get(s);var t=s.trim(),r;
 if(Object.prototype.hasOwnProperty.call(D,t))r=s.replace(t,D[t]);
 else{r=s;for(var i=0;i<2;i++)r=r.replace(RX,function(m,p,k){return p+D[k]})}
 if(C.size>8000)C.clear();C.set(s,r);return r}
window.__tr=tr;window.__trT=function(s){return String(s).split('\n').map(tr).join('\n')};
var SK={SCRIPT:1,STYLE:1,TEXTAREA:1,NOSCRIPT:1};
function fixText(n){var p=n.parentNode;if(!p||SK[p.nodeName])return;var v=n.data,x=tr(v);if(x!==v)n.data=x}
function fixAttr(el){['placeholder','title','alt','aria-label'].forEach(function(a){if(el.hasAttribute&&el.hasAttribute(a)){var v=el.getAttribute(a),x=tr(v);if(x!==v)el.setAttribute(a,x)}})}
function walk(root){if(!root)return;if(root.nodeType===3){fixText(root);return}if(root.nodeType!==1||SK[root.nodeName])return;fixAttr(root);
 var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT|NodeFilter.SHOW_ELEMENT,null),n;
 while(n=w.nextNode()){if(n.nodeType===3)fixText(n);else fixAttr(n)}}
var mo=new MutationObserver(function(ms){ms.forEach(function(m){if(m.type==='characterData')fixText(m.target);else if(m.type==='attributes')fixAttr(m.target);else m.addedNodes.forEach(walk)})});
mo.observe(document.documentElement,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['placeholder','title','alt','aria-label']});
function init(){walk(document.body);document.title='Quotation Request Form — Nefal';try{update()}catch(e){}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
