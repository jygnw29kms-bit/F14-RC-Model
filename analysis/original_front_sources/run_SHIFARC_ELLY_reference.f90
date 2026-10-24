program test_elly
 implicit none
 real xx(5),yy(5),coefs(3),u,v,t,s
 integer shape,ng,i
 xx=[313.,352.,331.,331.,0.]
 yy=[203.,199.5,203.,203.,0.]
 shape=4
 call krvdef(shape,0,xx,yy,coefs,ng)
 write(*,*) 'COEFFICIENTS',shape,ng,coefs
 if(ng/=0) stop 1
 do i=0,100
  u=39.*real(i)/100.
  call curves(shape,coefs(1),coefs(2),coefs(3),u,v,t,s)
  write(*,'(I4,4ES24.15)')i,u,v,t,s
 end do
end program
