"""Two-sided Student-t critical value, no scipy. Matches Excel TINV(alpha, df)."""
import math

def _betacf(a,b,x,itmax=300,eps=3e-16):
    qab=a+b; qap=a+1.0; qam=a-1.0
    c=1.0; d=1.0-qab*x/qap
    if abs(d)<1e-30: d=1e-30
    d=1.0/d; h=d
    for m in range(1,itmax+1):
        m2=2*m
        aa=m*(b-m)*x/((qam+m2)*(a+m2))
        d=1.0+aa*d
        if abs(d)<1e-30: d=1e-30
        c=1.0+aa/c
        if abs(c)<1e-30: c=1e-30
        d=1.0/d; h*=d*c
        aa=-(a+m)*(qab+m)*x/((a+m2)*(qap+m2))
        d=1.0+aa*d
        if abs(d)<1e-30: d=1e-30
        c=1.0+aa/c
        if abs(c)<1e-30: c=1e-30
        d=1.0/d; de=d*c; h*=de
        if abs(de-1.0)<eps: break
    return h

def betainc(a,b,x):
    """Regularized incomplete beta I_x(a,b)."""
    if x<=0.0: return 0.0
    if x>=1.0: return 1.0
    lbeta=math.lgamma(a+b)-math.lgamma(a)-math.lgamma(b)
    front=math.exp(lbeta+a*math.log(x)+b*math.log(1.0-x))
    if x < (a+1.0)/(a+b+2.0):
        return front*_betacf(a,b,x)/a
    return 1.0-math.exp(lbeta+b*math.log(1.0-x)+a*math.log(x))*_betacf(b,a,1.0-x)/b

def t_two_sided_p(t,df):
    """P(|T| > t) for Student-t with df degrees of freedom."""
    x=df/(df+t*t)
    return betainc(df/2.0,0.5,x)

def tinv(alpha,df):
    """Two-sided critical t: the t with P(|T|>t)=alpha. Excel TINV(alpha, df)."""
    lo,hi=0.0,1000.0
    for _ in range(200):
        mid=(lo+hi)/2.0
        if t_two_sided_p(mid,df)>alpha: lo=mid
        else: hi=mid
    return (lo+hi)/2.0

if __name__=="__main__":
    # validated against published tables
    for df,want in [(1,6.3138),(2,2.9200),(3,2.3534),(4,2.1318),(5,2.0150),(9,1.8331),
                    (10,1.8125),(19,1.7291),(29,1.6991),(42,1.6819),(44,1.6802),(49,1.6766),(120,1.6577)]:
        got=tinv(0.10,df)
        flag="OK " if abs(got-want)<0.0006 else "BAD"
        print(f"{flag} df={df:>4} tinv(0.10)={got:.5f}  table={want}")
