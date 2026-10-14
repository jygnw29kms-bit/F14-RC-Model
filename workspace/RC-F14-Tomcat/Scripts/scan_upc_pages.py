import pymupdf, os, re
pdf=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\references\UPC_F14_Structure_Report.pdf'
doc=pymupdf.open(pdf)
print('pages',len(doc))
for i,p in enumerate(doc):
    txt=p.get_text()
    if 'Design of fuselage sections' in txt or 'cross section 1' in txt.lower() or 'cross-section 1' in txt.lower():
        print('MATCH',i+1,txt[:1200].replace('\n',' | '))
