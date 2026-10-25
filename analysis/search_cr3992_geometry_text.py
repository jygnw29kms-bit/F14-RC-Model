from pypdf import PdfReader
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/references/NASA_CR3992_F14_VSTFE.pdf")
r=PdfReader(str(p)); terms=['mylar','digitized','cross section','cross-section','body station','fuselage station','station','surface grid','outer mold','geometry model']
for i,page in enumerate(r.pages):
 txt=(page.extract_text() or '').replace('\n',' ')
 low=txt.lower()
 if any(t in low for t in terms):
  # print only geometry-related pages likely
  hits=[t for t in terms if t in low]
  if i<40 or 70<=i<=95:
   print('\n===',i+1,hits,'===\n',txt[:9000])
