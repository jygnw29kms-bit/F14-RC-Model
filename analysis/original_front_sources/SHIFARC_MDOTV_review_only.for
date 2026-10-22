      SUBROUTINE MDOTV(A,B,C,NRA,N) 
C***********************************************************************
C*****    PERFORMS MATRIX MULTIPLICATION OF A VECTOR               *****
C*****    WRITTEN BY A. VACHRIS AND L. YAEGER                      *****
C***********************************************************************
      DIMENSION A(NRA,1),B(1),C(1)
!!!      DOUBLE SUM
      REAL*8 sum
      DO 100 I=1,N
      SUM=0.D0
      DO 200 J=1,N
  200 SUM=SUM+A(I,J)*B(J) 
  100 C(I)=SUM
      RETURN
      END Subroutine MdotV

