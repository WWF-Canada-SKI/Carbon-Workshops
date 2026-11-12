"""Assert every number written into Grasslands/05_Monitoring/README.md.
Re-run after any edit.  scipy-free; uses /tmp/claude-0/tdist.py.
"""
import math, re
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
GRASS = os.path.dirname(HERE)          # .../Grasslands
sys.path.insert(0, HERE)               # tdist.py lives beside this script
from tdist import tinv
t2   = lambda a,df: tinv(a,df)        # two-sided critical value
tone = lambda a,df: tinv(2*a,df)      # one-sided
ok=[]
def chk(label, got, want, tol):
    good = abs(got-want) <= tol
    ok.append(good)
    print(('  ok  ' if good else ' FAIL ')+f'{label}: got {got!r} want {want!r}')

# ---------------------------------------------------------------- worked example
S1=[11.15135,10.07148,10.474109]
S2=[12.936561,9.648159,11.539946]
mean=lambda x: sum(x)/len(x)
sd=lambda x: math.sqrt(sum((v-mean(x))**2 for v in x)/(len(x)-1))
print('Step 1 -- the grazed/ungrazed contrast')
chk('S1 mean', round(mean(S1),2), 10.57, 0)
chk('S1 sd',   round(sd(S1),2),   0.55,  0)
chk('S2 mean', round(mean(S2),2), 11.37, 0)
chk('S2 sd',   round(sd(S2),2),   1.65,  0)
d=mean(S2)-mean(S1); sp=math.sqrt((sd(S1)**2+sd(S2)**2)/2)
chk('difference', round(d,2), 0.81, 0)
chk('pooled sd',  round(sp,2), 1.23, 0)
chk('diff as % of grazed mean', round(100*d/mean(S1),1), 7.7, 0)
hw=t2(0.10,4)*sp*math.sqrt(2/3)
chk('CI low',  round(d-hw,2), -1.33, 0)
chk('CI high', round(d+hw,2),  2.95, 0)

print('Step 1 -- the three sample sizes')
n=next(k for k in range(3,200) if t2(0.10,2*k-2)*sp*math.sqrt(2/k)<=d)
chk('n, interval excludes zero (50% power)', n, 14, 0)
def n_pow(beta, sigma=sp, delta=d):
    k=4
    for _ in range(500):
        df=2*k-2
        need=2*((t2(0.10,df)+tone(beta,df))**2)*sigma**2/delta**2
        c=max(4,math.ceil(need))
        if c==k: return k
        k=c
    raise RuntimeError
chk('n, 80% power', n_pow(0.20), 30, 0)
chk('n, 90% power', n_pow(0.10), 41, 0)

# ---------------------------------------------------------------- MDD tables
CV=0.30
def n_indep(cv,rel,alpha=0.10,beta=0.20):
    k=4
    for _ in range(500):
        df=2*k-2
        need=2*((t2(alpha,df)+tone(beta,df))**2)*cv**2/rel**2
        c=max(4,math.ceil(need))
        if c==k: return k
        k=c
def n_paired(cv,rel,rho,alpha=0.10,beta=0.20):
    cvd=cv*math.sqrt(2*(1-rho)); k=4
    for _ in range(500):
        df=k-1
        need=((t2(alpha,df)+tone(beta,df))**2)*cvd**2/rel**2
        c=max(3,math.ceil(need))
        if c==k: return k
        k=c
print('Step 2 -- independent resampling table, CV 0.30')
for rel,want in [(0.05,446),(0.10,113),(0.15,51),(0.20,29),(0.30,14)]:
    chk(f'  {rel:.0%} change', n_indep(CV,rel), want, 0)

print('Step 2 -- years to detectability, paired, rho 0.80, stock 10.5656')
STOCK=mean(S1)
def mdd_rel(k,cv=CV,rho=0.80,alpha=0.10,beta=0.20):
    cvd=cv*math.sqrt(2*(1-rho)); df=k-1
    return (t2(alpha,df)+tone(beta,df))*cvd/math.sqrt(k)
for k,relw,absw,y3,y5,y10 in [(5,26.1,2.75,92,55,28),(10,16.3,1.72,57,34,17),
                              (15,12.9,1.36,45,27,14),(20,11.0,1.16,39,23,12),
                              (30, 8.8,0.93,31,19, 9),(50, 6.8,0.72,24,14, 7)]:
    r=mdd_rel(k); a=r*STOCK
    chk(f'  n={k} MDD %',    round(100*r,1), relw, 0.05)
    chk(f'  n={k} MDD kg',   round(a,2),     absw, 0)
    for rate,want in [(0.3,y3),(0.5,y5),(1.0,y10)]:
        chk(f'  n={k} yr @ {rate}', round(a/(rate/10)), want, 0)

print('Step 3 -- rho as intraclass correlation')
for sb,sw,want in [(0.30,0.15,0.80),(0.30,0.20,0.69),(0.25,0.25,0.50),(0.20,0.45,0.16)]:
    chk(f'  ICC({sb},{sw})', round(sb**2/(sb**2+sw**2),2), want, 0)
    tot={0.15:0.34,0.20:0.36,0.25:0.35,0.45:0.49}[sw]
    chk(f'  total CV({sb},{sw})', round(math.sqrt(sb**2+sw**2),2), tot, 0)

print('Step 3 -- paired vs independent at 10% change')
chk('  independent', n_indep(CV,0.10), 113, 0)
for rho,want in [(0.5,58),(0.7,35),(0.8,24),(0.9,13)]:
    chk(f'  paired rho={rho}', n_paired(CV,0.10,rho), want, 0)

print('Step 3 -- roots vs soil at 20% change')
for cv,rho,wp,wi in [(0.30,0.80,8,29),(0.30,0.60,13,29),(0.70,0.40,93,153),(0.70,0.20,123,153)]:
    chk(f'  cv={cv} rho={rho} paired', n_paired(cv,0.20,rho), wp, 0)
    chk(f'  cv={cv} independent',      n_indep(cv,0.20),      wi, 0)

# ---------------------------------------------------------------- ESM, plot GP-01
print('Step 4 -- equivalent soil mass, plot GP-01')
L=[(0,10,1.019,4.816),(10,20,1.182,3.003),(20,30,1.283,2.100),(30,60,1.359,1.205)]
m=lambda bd,th: bd*th*10.0                       # g/cm3 * cm -> kg/m2
for (top,bot,bd,pc),wm,wc in zip(L,[101.9,118.2,128.3,407.7],[4.908,3.550,2.694,4.913]):
    chk(f'  {top}-{bot} mass',   round(m(bd,bot-top),1), wm, 0.05)
    chk(f'  {top}-{bot} carbon', round(m(bd,bot-top)*pc/100,3), wc, 0)
M30=sum(m(bd,b-t) for t,b,bd,_ in L if b<=30)
C30=sum(m(bd,b-t)*pc/100 for t,b,bd,pc in L if b<=30)
chk('  mass to 30 cm',   round(M30,1), 348.4, 0)
chk('  carbon to 30 cm', round(C30,3), 11.151, 0)

def revisit(f):
    """uniform compression by factor f on depths; same soil, same carbon, BD x 1/f."""
    z=0; lay=[]
    for t,b,bd,pc in L:
        nt,nb=z,z+(b-t)*f; z=nb
        lay.append((nt,nb,m(bd,b-t),m(bd,b-t)*pc/100))
    cfix=mfix=0
    for nt,nb,mm,cc in lay:
        if nb<=30: cfix+=cc; mfix+=mm
        elif nt<30:
            fr=(30-nt)/(nb-nt); cfix+=cc*fr; mfix+=mm*fr
    acc=cesm=0; depth=0
    for nt,nb,mm,cc in lay:
        if acc+mm<=M30+1e-9: acc+=mm; cesm+=cc; depth=nb
        else:
            fr=(M30-acc)/mm; cesm+=cc*fr; depth=nt+(nb-nt)*fr; break
    return cfix, mfix, cesm, depth

cfix,mfix,cesm,dep = revisit(0.926)
chk('  compaction: BD rise %',    round(100*(1/0.926-1),0), 8, 0)
chk('  compaction: fixed-30 C',   round(cfix,3), 11.544, 0)
chk('  compaction: reported gain',round(cfix-C30,3), 0.393, 0)
chk('  compaction: gain %',       round(100*(cfix-C30)/C30,1), 3.5, 0)
chk('  compaction: fixed-30 mass',round(mfix,1), 381.0, 0)
chk('  compaction: extra mass',   round(mfix-M30,1), 32.6, 0)
chk('  compaction: ESM C',        round(cesm,3), 11.151, 0)
chk('  compaction: ESM change',   round(cesm-C30,6), 0.0, 1e-9)
chk('  compaction: ESM depth',    round(dep,2), 27.78, 0)

cfix,_,cesm,dep = revisit(1.074)
chk('  loosening: BD fall %',     round(100*(1-1/1.074),0), 7, 0)
chk('  loosening: fixed-30 C',    round(cfix,3), 10.594, 0)
chk('  loosening: reported loss', round(cfix-C30,3), -0.557, 0)
chk('  loosening: loss %',        round(100*(cfix-C30)/C30,1), -5.0, 0)
chk('  loosening: ESM change',    round(cesm-C30,6), 0.0, 1e-9)
chk('  loosening: ESM depth',     round(dep,2), 32.22, 0)

chk('  artefact vs detection limit (10 plots)',
    round(3.52/(100*mdd_rel(10))*3), 1, 0)   # "up to a third"

# ---------------------------------------------------------------- prose scan
print('Cross-check: figures present in the prose')
txt=open(os.path.join(GRASS,'05_Monitoring','README.md'),encoding='utf-8').read()
for s in ['−1.33 to +2.95','+0.81 kg C/m²','**14**','**30**','**41**','**446**','**113**',
          '**57**','16.3%','348.4','11.151','11.544','+0.393','10.594','−0.557',
          '**27.78 cm**','**32.22 cm**','381.0','32.6','**123**','**93**','**24**','**13**']:
    ok.append(s in txt)
    print(('  ok   ' if s in txt else ' FAIL ')+f'prose contains {s!r}')

print()
print(f'{sum(ok)}/{len(ok)} checks passed')
sys.exit(0 if all(ok) else 1)
