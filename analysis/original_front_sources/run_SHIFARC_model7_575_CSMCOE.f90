program test_csmcoe
 implicit none
 real cp(10,24),w(4,10),wx(5,10),wxx(4,10)
 integer ib(6,10)
 common /cpoint/ cp,ib
 common /wvalue/ w,wx,wxx
 cp=0.
 cp(1,1)=12.388888888889
 cp(1,4)=163.231481481481
 cp(1,7)=0.000000000000
 cp(1,10)=167.083333333333
 cp(1,13)=6.157407407407
 cp(1,16)=167.083333333333
 cp(1,19)=6.157407407407
 cp(1,22)=167.083333333333
 call csmcoe(1,3,1,0)
 write(*,*) 'RESULT',w(:,1)
end program
