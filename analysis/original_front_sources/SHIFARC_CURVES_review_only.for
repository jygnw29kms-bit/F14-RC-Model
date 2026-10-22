      SUBROUTINE CURVES(ISHAPE,AA,BB,CC,XX,YY,TT,SS)
C***********************************************************************
C*****    CALCULATES POINTS AND SLOPES FROM INDIVIDUAL CURVE FITS  *****
C*****    WRITTEN BY A. VACHRIS AND L. YAEGER                      *****
C***********************************************************************
!!!      DOUBLE A,B,C,X,Y,T,S,FACT,RFACT 
      REAL*8 A,B,C,X,Y,T,S,FACT,RFACT 
      DATA ZERO/1.E-5/,BIGZRO/1.E-2/
      A=AA
      B=BB
      C=CC
      X=XX
C*****        FUNCTION VALUE = Y
C*****        FIRST DERIVATIVE = T = DY/DX
C*****        SECOND DERIVATIVE = S = D2Y/DX2 
      Y=0.D0
      T=0.D0
      S=0.D0
      IF(ISHAPE.EQ.0) GO TO 9000
      NSHAPE=IABS(ISHAPE) 
      SSHAPE=ISIGN(1,ISHAPE)
      GO TO (100,200,300,400,500,600,700,800,900), NSHAPE 
C        *
C       ***         LINE                A*X + B*Y = 0 
C        *
  100 IF(B.NE.0.)T=-A/B 
      Y=X*T 
      GO TO 9000
C        *
C       ***         CIRCLE              A*X + B*Y + X**2 + Y**2 = 0 
C        *
  200 SWGN=SIGN(1.,BB)
      IF(BB.EQ.0.) SWGN=SSHAPE
      FACT=B*B-4.*X*(X+A) 
      Y=(SWGN*DSQRT(FACT)-B)/2. 
      FACT=2.*Y+B 
      DUM=FACT
      IF(DUM.EQ.0.) FACT=SWGN*BIGZRO
      T=-(2.*X+A)/FACT
      S=-2.*(T*T+1.)/FACT 
      GO TO 9000
C        *
C       ***         X-ELLIPSE           A*X + B*Y + C*X**2 + Y**2 = 0 
C        *
  300 SWGN=SIGN(1.,BB)
      IF(BB.EQ.0.) SWGN=SSHAPE
      FACT=B*B-4.*X*(C*X+A) 
      Y=(SWGN*DSQRT(FACT)-B)/2. 
      FACT=2.*Y+B 
      DUM=FACT
      IF(DUM.EQ.0.) FACT=SWGN*BIGZRO
      T=-(2.*C*X+A)/FACT
      S=-2.*(C+T*T)/FACT
      GO TO 9000
C        *
C       ***         Y-ELLIPSE           A*X + B*Y + C*Y**2 + X**2 = 0 
C        *
  400 IF(ABS(CC).LT.ZERO) GO TO 600 
      SWGN=SIGN(1.,BB)
      IF(BB.EQ.0.) SWGN=SSHAPE
      FACT=B*B-4.*C*X*(X+A) 
      Y=(SWGN*DSQRT(FACT)-B)/(2.*C) 
      FACT=2.*C*Y+B 
      DUM=FACT
      IF(DUM.EQ.0.) FACT=SWGN*BIGZRO
      T=-(2.*X+A)/FACT
      S=-2.*(1.+C*T*T)/FACT 
      GO TO 9000
C        *
C       ***         X-PARABOLA          A*X + B*Y + Y**2 = 0
C        *
  500 SWGN=SIGN(1.,BB)
      IF(BB.EQ.0.) SWGN=SSHAPE
      FACT=B*B-4.*A*X 
      Y=(SWGN*DSQRT(FACT)-B)/2. 
      FACT=2.*Y+B 
      DUM=FACT
      IF(DUM.EQ.0.) FACT=SWGN*BIGZRO
      T=-A/FACT 
      S=-2.*T*T/FACT
      GO TO 9000
C        *
C       ***         Y-PARABOLA          A*X + B*Y + X**2 = 0
C        *
  600 Y=-X*(X+A)/B
      T=-(2.*X+A)/B 
      S=-2./B 
      GO TO 9000
C        *
C       ***         ROTATED X-PARABOLA  A*X + B*Y + C*X*Y + Y**2 = 0
C        *
  700 RFACT=B+C*X 
      SWGN=SIGN(1.,BB)
      IF(BB.EQ.0.) SWGN=SSHAPE
      FACT=RFACT*RFACT-4.*A*X 
      Y=(SWGN*DSQRT(FACT)-RFACT)/2. 
      FACT=RFACT+2.*Y 
      DUM=FACT
      IF(DUM.EQ.0.) FACT=SWGN*BIGZRO
      T=-(A+C*Y)/FACT 
      S=-2.*T*(C+T)/FACT
      GO TO 9000
C        *
C       ***         ROTATED Y-PARABOLA  A*X + B*Y + C*X*Y + X**2 = 0
C        *
  800 FACT=B+C*X
      Y=-X*(X+A)/FACT 
      T=-(A+C*Y+2.*X)/FACT
      S=-2.*(1.+T*C)/FACT 
      GO TO 9000
C        *
C       ***         CUBIC               A*X + B*Y + C*X**2 + X**3 = 0 
C        *
  900 Y=-X*(X*(X+C)+A)/B
      T=-(A+(2.*C+3.*X)*X)/B
      S=-2.*(3.*X+C)/B
 9000 YY=Y
      TT=T
      SS=S
      RETURN
      END Subroutine Curves

