import pymupdf, os, re
pdf=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\references\UPC_F14_Structure_Report.pdf'
doc=pymupdf.open(pdf)
for i,p in enumerate(doc):
    t=' '.join(p.get_text().split())
    if 'Figure 3.16' in t or 'Figure 3.17' in t or '3.16' in t and 'cutaway' in t.lower():
        print('PAGE',i+1,t[:2200])
