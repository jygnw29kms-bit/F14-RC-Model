      SUBROUTINE KRVDEF(ISHAPE,IFREE,XX,YY,COEFS,NG)
C***********************************************************************
C*****    CALCULATES COEFFICIENTS FOR CURVE FITS                   *****
C*****    WRITTEN BY A. VACHRIS AND L. YAEGER                      *****
C***********************************************************************
      DIMENSION XX(5),YY(5),COEFS(1)
      ISET=0
      ISHAPO=0
      ZERO=1.E-6
      A=0.
      B=0.
      C=0.
      COEFS(1)=0. 
      COEFS(2)=0. 
      COEFS(3)=0. 
      NG=0
      IF(ISHAPE.EQ.0) GO TO 8000
      IF(ISHAPE.EQ.11) GO TO 8000 
      X2=XX(2)-XX(1)
      Y2=YY(2)-YY(1)
      X31=XX(3)-XX(1) 
      X42=XX(4)-XX(2) 
      Y31=YY(3)-YY(1) 
      Y42=YY(4)-YY(2) 
      INFT1=0 
      INFT2=0 
      T1=1.E+10 
      T2=1.E+10 
      IF(ABS(X31).LT.ZERO) INFT1=1
      IF(ABS(X42).LT.ZERO) INFT2=1
      IF(INFT1.EQ.0) T1=Y31/X31 
      IF(INFT2.EQ.0) T2=Y42/X42 
      FX2=0.
      FY2=0.
      GX2=0.
      GY2=0.
      PX2X2=X2*X2 
      SX2X2=X2+X2 
      PY2Y2=Y2*Y2 
      SY2Y2=Y2+Y2 
      PX2Y2=X2*Y2 
    1 GO TO (10,20,30,40,50,60,70,80,90),ISHAPE 
C        *
C       ***         LINE                A*X + B*Y = 0 
C        *
   10 A=Y2
      B=-X2 
      GO TO 8000
C        *
C       ***         CIRCLE              A*X + B*Y + X**2 + Y**2 = 0 
C        *
   20 F2=PX2X2+PY2Y2
      FX2=SX2X2 
      FY2=SY2Y2 
      GO TO 1000
C        *
C       ***         X-ELLIPSE           A*X + B*Y + C*X**2 + Y**2 = 0 
C        *
   30 F2=PY2Y2
      FY2=SY2Y2 
      G2=PX2X2
      GX2=SX2X2 
      GO TO 3000
C        *
C       ***         Y-ELLIPSE           A*X + B*Y + C*Y**2 + X**2 = 0 
C        *
   40 F2=PX2X2
      FX2=SX2X2 
      G2=PY2Y2
      GY2=SY2Y2 
      GO TO 3000
C        *
C       ***         X-PARABOLA          A*X + B*Y + Y**2 = 0
C        *
   50 F2=PY2Y2
      FY2=SY2Y2 
      GO TO 1000
C        *
C       ***         Y-PARABOLA          A*X + B*Y + X**2 = 0
C        *
   60 F2=PX2X2
      FX2=SX2X2 
      GO TO 1000
C        *
C       ***         ROTATED X-PARABOLA  A*X + B*Y + C*X*Y + Y**2 = 0
C        *
   70 F2=PY2Y2
      FY2=SY2Y2 
      G2=PX2Y2
      GX2=Y2
      GY2=X2
      GO TO 3000
C        *
C       ***         ROTATED Y-PARABOLA  A*X + B*Y + C*X*Y + X**2 = 0
C        *
   80 F2=PX2X2
      FX2=SX2X2 
      G2=PX2Y2
      GX2=Y2
      GY2=X2
      GO TO 3000
C        *
C       ***         CUBIC               A*X + B*Y + C*X**2 + X**3 = 0 
C        *
   90 F2=PX2X2*X2 
      FX2=3.*PX2X2
      G2=PX2X2
      GX2=SX2X2 
      GO TO 3000
C.....  COEFFICIENTS FOR GROUP 1 FUNCTIONS
 1000 IF(IFREE.EQ.0) GO TO 9000 
      TBAR=Y2/X2
      FBAR=F2/X2
      IF(IFREE.EQ.5) GO TO 1500 
      IF(IFREE.EQ.6) GO TO 1600 
 1500 IF(INFT2.EQ.1) GO TO 1520 
      FSTAR=FY2*T2+FX2
      T1INF=FSTAR-FBAR
      IF(ABS(T1INF).GT.ZERO) GO TO 1510 
      INFT1=1 
      GO TO 2100
 1510 T1=(TBAR*FSTAR-FBAR*T2)/T1INF 
      GO TO 2000
 1520 T1INF=FY2 
      IF(ABS(T1INF).GT.ZERO) GO TO 1530 
      INFT1=1 
      GO TO 2900
 1530 T1=(FY2*TBAR-FBAR)/T1INF
      GO TO 2200
 1600 IF(INFT1.EQ.1) GO TO 1620 
      T2INF=FBAR+(T1-TBAR)*FY2
      IF(ABS(T2INF).GT.ZERO) GO TO 1610 
      INFT2=1 
      GO TO 2200
 1610 T2=(FBAR*T1+(TBAR-T1)*FX2)/T2INF
      GO TO 2000
 1620 T2INF=FY2 
      IF(ABS(T2INF).GT.ZERO) GO TO 1630 
      INFT2=1 
      GO TO 2900
 1630 T2=(FBAR-FX2)/T2INF 
      GO TO 2100
 2000 TEST=T2-T1
      IF(ABS(TEST).LT.ZERO) GO TO 2800
      B=-(FY2*T2+FX2)/TEST
      A=-B*T1 
      GO TO 8000
 2100 B=0.
      A=-FBAR 
      GO TO 8000
 2200 B=-FY2
      A=-B*T1 
      GO TO 8000
 2800 A=Y31 
      B=-X31
      GO TO 8000
 2900 A=0.
      B=0.
      GO TO 9000
C.....   COEFFICIENTS FOR GROUP 2 FUNCTIONS 
 3000 IF(IFREE.GT.0) GO TO 9000 
      FBAR=F2/X2
      GBAR=G2/X2
      TBAR=Y2/X2
      IF(INFT2.EQ.1) GO TO 4200 
      FSTAR=FY2*T2+FX2
      GSTAR=GY2*T2+GX2
      IF(INFT1.EQ.1) GO TO 4100 
      TEST=T2-T1
      IF(ABS(TEST).LT.ZERO) GO TO 4800
      FCOMP=FBAR*TEST+(T1-TBAR)*FSTAR 
      GCOMP=GBAR*TEST+(T1-TBAR)*GSTAR 
      IF(ABS(GCOMP).LT.ZERO) GO TO 4500 
 4000 C=-FCOMP/GCOMP
      B=-(C*GSTAR+FSTAR)/TEST 
      A=-B*T1 
      GO TO 8000
 4800 IF(ISHAPE.NE.9.OR.T1.EQ.1.E+10) GO TO 9000
      C=-3.*X2/2. 
      B=F2/(2.*(Y2-X2*T1))
      A=-B*T1 
      GO TO 8000
 4100 B=0.
      CINF=GBAR-GSTAR 
      IF(ABS(CINF).LT.ZERO) GO TO 4510
      C=-(FBAR-FSTAR)/CINF
      A=-(C*GBAR+FBAR)
      GO TO 8000
 4200 CINF=GBAR-(TBAR-T1)*GY2 
      IF(ABS(CINF).LT.ZERO) GO TO 4520
      C=-(FBAR-(TBAR-T1)*FY2)/CINF
      B=-(C*GY2+FY2)
      A=-B*T1 
 8000 COEFS(1)=A
      COEFS(2)=B
      COEFS(3)=C
      IF(ISHAPE.NE.0.AND.ISHAPE.NE.11)ISHAPE=ISHAPE*SIGN(1.,Y2) 
      RETURN
 4500 CONTINUE
 4510 CONTINUE
 4520 CONTINUE
      ISET=ISET+1 
      IF(ISET.GT.1) GO TO 8999
      IF(ISET.EQ.1) ISHAPO=ISHAPE 
      GO TO(8999,8999,4530,4540,8999,8999,4570,4580,8999),ISHAPO
 4530 IF(ISET.EQ.1) ISHAPE=4
      GO TO 1 
 4540 IF(ISET.EQ.1) ISHAPE=3
      GO TO 1 
 4570 IF(ISET.EQ.1) ISHAPE=8
      GO TO 1 
 4580 IF(ISET.EQ.1) ISHAPE=7
      GO TO 1 
 8999 ISHAPE=11 
 9000 NG=1
      RETURN
      END Subroutine Krvdef

