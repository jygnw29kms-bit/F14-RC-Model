      SUBROUTINE VDOTV(A,B,D,N) 
C***********************************************************************
C*****    COMPUTES VECTOR DOT PRODUCT                              *****
C*****    WRITTEN BY A. VACHRIS AND L. YAEGER                      *****
C***********************************************************************
      DIMENSION A(1),B(1) 
!!!      DOUBLE C
      REAL*8 c
      C=0.D0
      DO 100 I=1,N
  100 C=C+A(I)*B(I) 
      D=C 
      RETURN
      END Subroutine VdotV

