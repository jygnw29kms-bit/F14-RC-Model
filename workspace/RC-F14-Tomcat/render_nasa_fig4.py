import fitz
pdf=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\references\NASA_CR_163098_F14_three_view.pdf'
doc=fitz.open(pdf)
page=doc[24]
pix=page.get_pixmap(matrix=fitz.Matrix(3,3), alpha=False)
out=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\references\NASA_F14_Fig4_3view.png'
pix.save(out)
print(out, pix.width, pix.height)
