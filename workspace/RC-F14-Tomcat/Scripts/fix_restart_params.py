from pathlib import Path
files=[
 Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC\F14TomcatRC.py'),
 Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC_v18\F14TomcatRC_v18.py')]
old="""    design.userParameters.add('ReviewSpan20',adsk.core.ValueInput.createByReal(mm(span)),'mm','Source wing reference scale; body datum registration pending')
    design.userParameters.add('SourceSpanFull',adsk.core.ValueInput.createByReal(mm(source_span_in*25.4)),'mm','Grumman basic-wing defining-table tip WBL times two')"""
new="""    if not design.userParameters.itemByName('ReviewSpan20'):
        design.userParameters.add('ReviewSpan20',adsk.core.ValueInput.createByReal(mm(span)),'mm','Source wing reference scale; body datum registration pending')
    if not design.userParameters.itemByName('SourceSpanFull'):
        design.userParameters.add('SourceSpanFull',adsk.core.ValueInput.createByReal(mm(source_span_in*25.4)),'mm','Grumman basic-wing defining-table tip WBL times two')"""
for p in files:
    s=p.read_text(encoding='utf-8')
    if old not in s:
        print('pattern missing',p)
        continue
    p.write_text(s.replace(old,new,1),encoding='utf-8')
    print('patched',p)
