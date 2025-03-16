# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.8.2
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00 \xb8\
c\
onst STORAGE_API\
_KEY = 'api_key'\
;\x0aconst STORAGE_\
TARGET_LANG = 't\
arget_lang';\x0a\x0ale\
t popup = null;\x0a\
let is_translati\
on_enabled = fal\
se;\x0alet last_hig\
hlighted_element\
 = null;\x0alet tra\
nslating = false\
;\x0a\x0aconst LANGUAG\
ES = {\x0a  ko: '\xed\x95\
\x9c\xea\xb5\xad\xec\x96\xb4',\x0a  en: \
'English',\x0a  ja:\
 '\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e',\x0a  \
zh: '\xe4\xb8\xad\xe6\x96\x87',\x0a  \
es: 'Espa\xc3\xb1ol',\x0a\
  fr: 'Fran\xc3\xa7ais\
',\x0a  de: 'Deutsc\
h',\x0a};\x0a\x0aconst st\
yle = document.c\
reateElement('st\
yle');\x0astyle.tex\
tContent = `\x0a  .\
s-trans-hoverabl\
e {\x0a    backgrou\
nd-color: rgba(0\
, 96, 223, 0.1) \
!important;\x0a    \
cursor: pointer \
!important;\x0a  }\x0a\
`;\x0adocument.head\
.appendChild(sty\
le);\x0a\x0awindow.add\
EventListener('t\
ranslationStateC\
hanged', (event)\
 => {\x0a  is_trans\
lation_enabled =\
 event.detail.en\
abled;\x0a  if (!is\
_translation_ena\
bled) {\x0a    hide\
Popup();\x0a  }\x0a});\
\x0a\x0afunction creat\
ePopup() {\x0a  con\
st popup = docum\
ent.createElemen\
t('div');\x0a  popu\
p.style.cssText \
= `\x0a    position\
: fixed;\x0a    bac\
kground: white;\x0a\
    border: 1px \
solid #ccc;\x0a    \
border-radius: 4\
px;\x0a    padding:\
 8px;\x0a    box-sh\
adow: 0 2px 4px \
rgba(0,0,0,0.2);\
\x0a    z-index: 10\
000;\x0a    font-fa\
mily: system-ui,\
 -apple-system, \
sans-serif;\x0a    \
font-size: 14px;\
\x0a    display: no\
ne;\x0a  `;\x0a\x0a  cons\
t translate_butt\
on = document.cr\
eateElement('but\
ton');\x0a  transla\
te_button.textCo\
ntent = 'Transla\
te';\x0a  translate\
_button.style.cs\
sText = `\x0a    ba\
ckground: #0060d\
f;\x0a    color: wh\
ite;\x0a    border:\
 none;\x0a    paddi\
ng: 4px 8px;\x0a   \
 border-radius: \
4px;\x0a    cursor:\
 pointer;\x0a  `;\x0a\x0a\
  translate_butt\
on.addEventListe\
ner('click', han\
dleTranslate);\x0a \
 popup.appendChi\
ld(translate_but\
ton);\x0a  document\
.body.appendChil\
d(popup);\x0a  retu\
rn popup;\x0a}\x0a\x0afun\
ction showPopup(\
x, y) {\x0a  if (!i\
s_translation_en\
abled) {\x0a    ret\
urn;\x0a  }\x0a\x0a  if (\
!popup) {\x0a    po\
pup = createPopu\
p();\x0a  }\x0a\x0a  popu\
p.style.display \
= 'block';\x0a  pop\
up.style.left = \
`${x}px`;\x0a  popu\
p.style.top = `$\
{y}px`;\x0a}\x0a\x0afunct\
ion hidePopup() \
{\x0a  if (popup) {\
\x0a    popup.style\
.display = 'none\
';\x0a  }\x0a}\x0a\x0adocume\
nt.addEventListe\
ner('mouseup', (\
event) => {\x0a  if\
 (!is_translatio\
n_enabled || tra\
nslating) {\x0a    \
return;\x0a  }\x0a\x0a  c\
onst selection =\
 window.getSelec\
tion();\x0a  const \
selected_text = \
selection.toStri\
ng().trim();\x0a  i\
f (selected_text\
) {\x0a    const ra\
nge = selection.\
getRangeAt(0);\x0a \
   const rect = \
range.getBoundin\
gClientRect();\x0a \
   showPopup(rec\
t.left, rect.bot\
tom + 5);\x0a  } el\
se {\x0a    hidePop\
up();\x0a  }\x0a});\x0a\x0aa\
sync function ha\
ndleTranslate() \
{\x0a  if (!is_tran\
slation_enabled \
|| translating) \
{\x0a    return;\x0a  \
}\x0a\x0a  hidePopup()\
;\x0a\x0a  const stora\
ge = await brows\
er.storage.local\
.get([STORAGE_AP\
I_KEY, STORAGE_T\
ARGET_LANG]);\x0a  \
const api_key = \
storage[STORAGE_\
API_KEY];\x0a  cons\
t target_lang = \
storage[STORAGE_\
TARGET_LANG] || \
'ko'; // Default\
 to Korean if no\
t set\x0a  if (!api\
_key) {\x0a    aler\
t('Please set yo\
ur OpenAI API ke\
y in the extensi\
on settings');\x0a \
   return;\x0a  }\x0a\x0a\
  try {\x0a    tran\
slating = true;\x0a\
\x0a    const selec\
tion = window.ge\
tSelection();\x0a  \
  const common_a\
ncestor = select\
ion.getRangeAt(0\
).commonAncestor\
Container;\x0a    s\
election.removeA\
llRanges();\x0a    \
const range = do\
cument.createRan\
ge();\x0a    range.\
selectNodeConten\
ts(common_ancest\
or);\x0a    selecti\
on.addRange(rang\
e);\x0a    const se\
lected_text = se\
lection.toString\
().trim();\x0a    c\
onst paragraphs \
= selected_text\x0a\
      .split(/\x5cn\
+/)\x0a      .map((\
p) => p.trim())\x0a\
      .filter((p\
) => p);\x0a    con\
st paragraph_nod\
es = [];\x0a    con\
st paragraph_nod\
e_next_siblings \
= [];\x0a\x0a    // Fi\
nd last text nod\
es that contain \
the paragraph te\
xt\x0a    let parag\
raph_index = 0;\x0a\
    let remain_p\
aragraph_text = \
paragraphs[parag\
raph_index];\x0a   \
 const walker = \
document.createT\
reeWalker(common\
_ancestor, NodeF\
ilter.SHOW_TEXT,\
 () => NodeFilte\
r.FILTER_ACCEPT)\
;\x0a    let node;\x0a\
    while ((node\
 = walker.nextNo\
de())) {\x0a      c\
onst lines = nod\
e.textContent\x0a  \
      .trim()\x0a  \
      .split(/\x5cn\
+/)\x0a        .map\
((p) => p.trim()\
)\x0a        .filte\
r((p) => p);\x0a   \
   for (const li\
ne of lines) {\x0a \
       if (line \
&& remain_paragr\
aph_text.startsW\
ith(line)) {\x0a   \
       remain_pa\
ragraph_text = r\
emain_paragraph_\
text.slice(line.\
length).trim();\x0a\
          if (re\
main_paragraph_t\
ext.length === 0\
) {\x0a            \
paragraph_nodes.\
push(node);\x0a    \
        paragrap\
h_node_next_sibl\
ings.push(node.n\
extSibling);\x0a   \
         paragra\
ph_index++;\x0a    \
        remain_p\
aragraph_text = \
paragraphs[parag\
raph_index];\x0a   \
       }\x0a       \
 }\x0a      }\x0a    }\
\x0a    while (para\
graph_index < pa\
ragraphs.length)\
 {\x0a      paragra\
ph_nodes.push(ra\
nge.endContainer\
);\x0a      paragra\
ph_node_next_sib\
lings.push(range\
.endContainer.ne\
xtSibling);\x0a    \
  paragraph_inde\
x++;\x0a    }\x0a    s\
election.removeA\
llRanges();\x0a\x0a   \
 for (let i = 0;\
 i < paragraphs.\
length; i++) {\x0a \
     let result_\
element;\x0a      t\
ry {\x0a        con\
st paragraph = p\
aragraphs[i];\x0a  \
      const para\
graph_node = par\
agraph_nodes[i];\
\x0a        const p\
aragraph_node_ne\
xt_sibling = par\
agraph_node_next\
_siblings[i];\x0a\x0a \
       result_el\
ement = document\
.createElement('\
span');\x0a        \
result_element.t\
extContent = 'Tr\
anslating...';\x0a \
       result_el\
ement.style.cssT\
ext = `\x0a        \
    color: #666;\
\x0a            mar\
gin-top: 0.5em;\x0a\
            marg\
in-bottom: 0.5em\
;\x0a          `;\x0a \
       const con\
tainer = documen\
t.createElement(\
'span');\x0a       \
 container.appen\
dChild(document.\
createElement('b\
r'));\x0a        co\
ntainer.appendCh\
ild(result_eleme\
nt);\x0a        par\
agraph_node.pare\
ntNode.insertBef\
ore(container, p\
aragraph_node_ne\
xt_sibling);\x0a\x0a  \
      const resp\
onse = await fet\
ch('https://api.\
openai.com/v1/ch\
at/completions',\
 {\x0a          met\
hod: 'POST',\x0a   \
       headers: \
{\x0a            'C\
ontent-Type': 'a\
pplication/json'\
,\x0a            'A\
uthorization': `\
Bearer ${api_key\
}`,\x0a          },\
\x0a          body:\
 JSON.stringify(\
{\x0a            mo\
del: 'gpt-4o-min\
i',\x0a            \
messages: [\x0a    \
          {\x0a    \
            role\
: 'system',\x0a    \
            cont\
ent: `You are a \
translator. Tran\
slate the given \
text to ${LANGUA\
GES[target_lang]\
}. Only respond \
with the transla\
ted text, withou\
t any additional\
 explanation or \
context.`,\x0a     \
         },\x0a    \
          {\x0a    \
            role\
: 'user',\x0a      \
          conten\
t: paragraph,\x0a  \
            },\x0a \
           ],\x0a  \
        }),\x0a    \
    });\x0a        \
const data = awa\
it response.json\
();\x0a        if (\
!response.ok) {\x0a\
          throw \
new Error(data.e\
rror?.message ||\
 'Translation fa\
iled');\x0a        \
}\x0a        const \
translated_text \
= data.choices[0\
].message.conten\
t.trim();\x0a      \
  result_element\
.textContent = t\
ranslated_text;\x0a\
      } catch (e\
rror) {\x0a        \
result_element.t\
extContent = `Tr\
anslation error:\
 ${error.message\
}`;\x0a      }\x0a    \
}\x0a  } catch (err\
or) {\x0a    alert(\
`Translation err\
or: ${error.mess\
age}`);\x0a  } fina\
lly {\x0a    transl\
ating = false;\x0a \
 }\x0a}\x0a\x0adocument.a\
ddEventListener(\
'mousedown', (ev\
ent) => {\x0a  if (\
popup && !popup.\
contains(event.t\
arget)) {\x0a    hi\
dePopup();\x0a  }\x0a}\
);\x0a\x0afunction isI\
nteractiveElemen\
t(element) {\x0a  r\
eturn (\x0a    elem\
ent.tagName === \
'INPUT' ||\x0a    e\
lement.tagName =\
== 'TEXTAREA' ||\
\x0a    element.tag\
Name === 'SELECT\
' ||\x0a    element\
.tagName === 'BU\
TTON' ||\x0a    ele\
ment.tagName ===\
 'A'\x0a  );\x0a}\x0a\x0adoc\
ument.addEventLi\
stener('mousemov\
e', (event) => {\
\x0a  if (!is_trans\
lation_enabled |\
| translating) {\
\x0a    return;\x0a  }\
\x0a\x0a  const target\
 = event.target;\
\x0a  if (last_high\
lighted_element \
=== target) {\x0a  \
  return;\x0a  }\x0a\x0a \
 removeHighlight\
();\x0a\x0a  // Skip i\
f hovering over \
the popup or int\
eractive element\
s\x0a  if (popup?.c\
ontains(target) \
|| isInteractive\
Element(target))\
 {\x0a    return;\x0a \
 }\x0a\x0a  // Add hig\
hlight to curren\
t element if it \
has text\x0a  if (t\
arget.textConten\
t?.trim()) {\x0a   \
 target.classLis\
t.add('s-trans-h\
overable');\x0a    \
last_highlighted\
_element = targe\
t;\x0a  }\x0a});\x0a\x0adocu\
ment.addEventLis\
tener('mouseleav\
e', () => {\x0a  re\
moveHighlight();\
\x0a});\x0a\x0adocument.a\
ddEventListener(\
'click', (event)\
 => {\x0a  if (!is_\
translation_enab\
led || translati\
ng) {\x0a    return\
;\x0a  }\x0a\x0a  removeH\
ighlight();\x0a\x0a  c\
onst clicked_ele\
ment = event.tar\
get;\x0a\x0a  // Skip \
if clicking on t\
he popup or if e\
lement is intera\
ctive\x0a  if (popu\
p?.contains(clic\
ked_element) || \
isInteractiveEle\
ment(clicked_ele\
ment)) {\x0a    ret\
urn;\x0a  }\x0a\x0a  cons\
t text = clicked\
_element.textCon\
tent?.trim();\x0a  \
if (!text) {\x0a   \
 return;\x0a  }\x0a\x0a  \
const selection \
= window.getSele\
ction();\x0a  selec\
tion.removeAllRa\
nges();\x0a  const \
range = document\
.createRange();\x0a\
  range.selectNo\
deContents(click\
ed_element);\x0a  s\
election.addRang\
e(range);\x0a\x0a  if \
(event.ctrlKey |\
| event.metaKey)\
 {\x0a    handleTra\
nslate();\x0a  } el\
se {\x0a    const r\
ect = range.getB\
oundingClientRec\
t();\x0a    showPop\
up(rect.left, re\
ct.bottom + 5);\x0a\
  }\x0a});\x0a\x0afunctio\
n removeHighligh\
t() {\x0a  if (last\
_highlighted_ele\
ment) {\x0a    last\
_highlighted_ele\
ment.classList.r\
emove('s-trans-h\
overable');\x0a    \
last_highlighted\
_element = null;\
\x0a  }\x0a}\x0a\
"

qt_resource_name = b"\
\x00\x0d\
\x0f\xa6\xe0\xb3\
\x00t\
\x00r\x00a\x00n\x00s\x00l\x00a\x00t\x00o\x00r\x00.\x00j\x00s\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x95\xa1\x10a\x83\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
