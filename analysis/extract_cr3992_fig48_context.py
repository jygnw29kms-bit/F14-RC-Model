from pypdf import PdfReader
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/references/NASA_CR3992_F14_VSTFE.pdf")
r=PdfReader(str(p))
for i in range(max(0,84),min(len(r.pages),94)):
    txt=r.pages[i].extract_text() or ''
    print('\n=== PDF PAGE',i+1,'===\n',txt[:12000])
