import csv, json, pathlib, sys
p=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).parents[1]/'manufacturing/proof_fixtures/v107/proof_log_template.csv'
rows=list(csv.DictReader(p.open(encoding='utf-8-sig')))
if not rows or not any(r.get('article_id') for r in rows):
    print(json.dumps({'status':'NO_TEST_DATA','file':str(p)},indent=2)); raise SystemExit(0)
def f(v):
    try:return float(v)
    except:return None
out=[]
for aid in sorted(set(r['article_id'] for r in rows if r.get('article_id'))):
  for socket in sorted(set(r['socket'] for r in rows if r.get('article_id')==aid)):
    rr=[r for r in rows if r.get('article_id')==aid and r.get('socket')==socket]
    vals=[(f(r['load_N']),f(r['displacement_mm'])) for r in rr]
    vals=[x for x in vals if None not in x]
    pos=[x for x in vals if x[0]>0]
    stiffness=max((L/d for L,d in pos if d and d>0),default=None)
    zero=[d for L,d in vals if abs(L)<1e-9]
    perm=abs(zero[-1]-zero[0]) if len(zero)>=2 else None
    bx=[f(r['bore_x_mm']) for r in rr if f(r['bore_x_mm']) is not None]; bz=[f(r['bore_z_mm']) for r in rr if f(r['bore_z_mm']) is not None]
    growth=max((max(bx)-min(bx) if len(bx)>=2 else 0),(max(bz)-min(bz) if len(bz)>=2 else 0))
    out.append({'article_id':aid,'socket':socket,'estimated_peak_stiffness_N_per_mm':stiffness,'permanent_set_mm':perm,'max_recorded_bore_growth_mm':growth,'permanent_set_screen_pass':None if perm is None else perm<=0.20,'bore_growth_screen_pass':growth<=0.10})
print(json.dumps({'status':'V107_PROOF_LOG_EVALUATION','results':out},indent=2))