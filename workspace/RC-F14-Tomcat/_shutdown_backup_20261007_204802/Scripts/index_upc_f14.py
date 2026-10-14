import pymupdf, os, re, json
pdf=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\references\UPC_F14_Structure_Report.pdf'
doc=pymupdf.open(pdf)
terms=['wing pivot mechanism','horizontal stabilizer design','vertical stabilizer design','wing beam design','fuselage sections','cross-section','cross section']
hits=[]
for i,p in enumerate(doc):
    t=' '.join(p.get_text().split())
    tl=t.lower()
    found=[term for term in terms if term in tl]
    if found:
        hits.append({'page':i+1,'terms':found,'text':t[:2200]})
out=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\analysis\UPC_report_index.json'
with open(out,'w',encoding='utf-8') as f: json.dump(hits,f,indent=2,ensure_ascii=False)
for h in hits:
    print(h['page'], h['terms'], h['text'][:450])
print('wrote',out)
