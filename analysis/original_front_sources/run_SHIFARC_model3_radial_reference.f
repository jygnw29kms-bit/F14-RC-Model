      program test_radius
      real cp(10,24),w(4,10),wx(5,10),wxx(4,10)
      integer ib(6,10)
      common /cpoint/ cp,ib
      common /wvalue/ w,wx,wxx
      common /write/ iread,irite,icrite,itape,iplot
      COMMON/CSCONF/KNTCSM,KNTCSA(10),ICSASQ(10,10),ICSASH(10,10),
     1ICSATY(10,10),ICSAFR(10,10),ICSACP(3,10,10),ICSACC(2,10,10),
     2XCSMS1(10),XCSMS2(10),IZCDEX,IZBDEX(10),IZTDEX(10), 
     3NCSM,ICSMX(10),ISPEC(2,10,10),IN(10),IUORDR(10) 
      irite=6
      icrite=6
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-24.250000000000
      cp(1,7)=31.000000000000
      cp(1,10)=-15.500000000000
      cp(1,13)=31.000000000000
      cp(1,16)=-24.250000000000
      cp(1,19)=31.000000000000
      cp(1,22)=-24.250000000000
      call csmcoe(1,3,1,0)
      icsash(1,1)=3
      h=-1.570796326795
      call cscalc(352.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',1,r
      h=-1.372563968767
      call cscalc(352.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',2,r
      h=-1.188451887238
      call cscalc(352.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',3,r
      h=-1.027354792967
      call cscalc(352.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',4,r
      h=-0.891797040853
      call cscalc(352.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',5,r
      h=-0.780052209383
      call cscalc(352.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',6,r
      h=-0.688672318805
      call cscalc(352.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',7,r
      h=-0.614060957628
      call cscalc(352.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',8,r
      h=-0.553146107690
      call cscalc(352.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',9,r
      h=-0.503562962980
      call cscalc(352.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',10,r
      h=-0.463647609001
      call cscalc(352.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',11,r
      cp=0.
      cp(2,1)=31.000000000000
      cp(2,4)=-15.500000000000
      cp(2,7)=31.000000000000
      cp(2,10)=4.000000000000
      cp(2,13)=31.000000000000
      cp(2,16)=-15.500000000000
      cp(2,19)=31.000000000000
      cp(2,22)=4.000000000000
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.463647609001
      call cscalc(352.,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',12,r
      h=0.128323227686
      call cscalc(352.,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',13,r
      cp=0.
      cp(3,1)=31.000000000000
      cp(3,4)=4.000000000000
      cp(3,7)=67.000000000000
      cp(3,10)=10.500000000000
      cp(3,13)=31.000000000000
      cp(3,16)=4.000000000000
      cp(3,19)=67.000000000000
      cp(3,22)=10.500000000000
      call csmcoe(3,1,1,0)
      icsash(3,1)=1
      h=0.128323227686
      call cscalc(352.,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',14,r
      h=0.155452011640
      call cscalc(352.,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',15,r
      cp=0.
      cp(4,1)=67.000000000000
      cp(4,4)=10.500000000000
      cp(4,7)=66.500000000000
      cp(4,10)=16.500000000000
      cp(4,13)=67.000000000000
      cp(4,16)=10.500000000000
      cp(4,19)=66.500000000000
      cp(4,22)=16.500000000000
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=0.155452011640
      call cscalc(352.,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',16,r
      h=0.243208753471
      call cscalc(352.,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',17,r
      cp=0.
      cp(5,1)=66.500000000000
      cp(5,4)=16.500000000000
      cp(5,7)=31.000000000000
      cp(5,10)=9.000000000000
      cp(5,13)=66.500000000000
      cp(5,16)=16.500000000000
      cp(5,19)=31.000000000000
      cp(5,22)=9.000000000000
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.243208753471
      call cscalc(352.,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',18,r
      h=0.282554952470
      call cscalc(352.,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',19,r
      cp=0.
      cp(6,1)=31.000000000000
      cp(6,4)=9.000000000000
      cp(6,7)=16.000000000000
      cp(6,10)=37.500000000000
      cp(6,13)=31.000000000000
      cp(6,16)=27.000000000000
      cp(6,19)=31.000000000000
      cp(6,22)=27.000000000000
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=0.282554952470
      call cscalc(352.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',20,r
      h=0.380113674222
      call cscalc(352.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',21,r
      h=0.475054501476
      call cscalc(352.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',22,r
      h=0.567638896001
      call cscalc(352.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',23,r
      h=0.658110125928
      call cscalc(352.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',24,r
      h=0.746690527084
      call cscalc(352.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',25,r
      h=0.833580555156
      call cscalc(352.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',26,r
      h=0.918959050341
      call cscalc(352.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',27,r
      h=1.002984290962
      call cscalc(352.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',28,r
      h=1.085795535502
      call cscalc(352.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',29,r
      h=1.167514845076
      call cscalc(352.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',30,r
      cp=0.
      cp(7,1)=16.000000000000
      cp(7,4)=37.500000000000
      cp(7,7)=0.000000000000
      cp(7,10)=53.500000000000
      cp(7,13)=16.000000000000
      cp(7,16)=53.500000000000
      cp(7,19)=16.000000000000
      cp(7,22)=53.500000000000
      call csmcoe(7,3,1,0)
      icsash(7,1)=3
      h=1.167514845076
      call cscalc(352.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',31,r
      h=1.194567759178
      call cscalc(352.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',32,r
      h=1.226556073628
      call cscalc(352.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',33,r
      h=1.262478599036
      call cscalc(352.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',34,r
      h=1.301528154646
      call cscalc(352.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',35,r
      h=1.343044499878
      call cscalc(352.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',36,r
      h=1.386477669450
      call cscalc(352.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',37,r
      h=1.431359427508
      call cscalc(352.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',38,r
      h=1.477280769425
      call cscalc(352.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',39,r
      h=1.523873759566
      call cscalc(352.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',40,r
      h=1.570796326795
      call cscalc(352.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',41,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-23.877809499424
      cp(1,7)=30.568000000000
      cp(1,10)=-16.282216074766
      cp(1,13)=30.568000000000
      cp(1,16)=-23.877809499424
      cp(1,19)=30.568000000000
      cp(1,22)=-23.877809499424
      call csmcoe(1,3,1,0)
      icsash(1,1)=3
      h=-1.570796326795
      call cscalc(370.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',42,r
      h=-1.372389085052
      call cscalc(370.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',43,r
      h=-1.188691620205
      call cscalc(370.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',44,r
      h=-1.028859195353
      call cscalc(370.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',45,r
      h=-0.895357704701
      call cscalc(370.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',46,r
      h=-0.786282688632
      call cscalc(370.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',47,r
      h=-0.698032826624
      call cscalc(370.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',48,r
      h=-0.626928685677
      call cscalc(370.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',49,r
      h=-0.569883273198
      call cscalc(370.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',50,r
      h=-0.524573676012
      call cscalc(370.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',51,r
      h=-0.489429522917
      call cscalc(370.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',52,r
      cp=0.
      cp(2,1)=30.568000000000
      cp(2,4)=-16.282216074766
      cp(2,7)=30.568000000000
      cp(2,10)=-2.398216074766
      cp(2,13)=30.568000000000
      cp(2,16)=-16.282216074766
      cp(2,19)=30.568000000000
      cp(2,22)=-2.398216074766
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.489429522917
      call cscalc(370.,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',53,r
      h=-0.078294741654
      call cscalc(370.,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',54,r
      cp=0.
      cp(3,1)=30.568000000000
      cp(3,4)=-2.398216074766
      cp(3,7)=68.777777777778
      cp(3,10)=2.124610591900
      cp(3,13)=30.568000000000
      cp(3,16)=-2.398216074766
      cp(3,19)=68.777777777778
      cp(3,22)=2.124610591900
      call csmcoe(3,1,1,0)
      icsash(3,1)=1
      h=-0.078294741654
      call cscalc(370.,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',55,r
      h=0.030881125323
      call cscalc(370.,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',56,r
      cp=0.
      cp(4,1)=68.777777777778
      cp(4,4)=2.124610591900
      cp(4,7)=66.500000000000
      cp(4,10)=17.902388369678
      cp(4,13)=68.777777777778
      cp(4,16)=2.124610591900
      cp(4,19)=66.500000000000
      cp(4,22)=17.902388369678
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=0.030881125323
      call cscalc(370.,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',57,r
      h=0.262974291598
      call cscalc(370.,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',58,r
      cp=0.
      cp(5,1)=66.500000000000
      cp(5,4)=17.902388369678
      cp(5,7)=29.572413793103
      cp(5,10)=9.951047373510
      cp(5,13)=66.500000000000
      cp(5,16)=17.902388369678
      cp(5,19)=29.572413793103
      cp(5,22)=9.951047373510
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.262974291598
      call cscalc(370.,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',59,r
      h=0.324595719479
      call cscalc(370.,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',60,r
      cp=0.
      cp(6,1)=29.572413793103
      cp(6,4)=9.951047373510
      cp(6,7)=14.981132075472
      cp(6,10)=36.948509962969
      cp(6,13)=28.452830188679
      cp(6,16)=27.144150821785
      cp(6,19)=28.452830188679
      cp(6,22)=27.144150821785
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=0.324595719479
      call cscalc(370.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',61,r
      h=0.422551031652
      call cscalc(370.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',62,r
      h=0.517490814997
      call cscalc(370.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',63,r
      h=0.609507633628
      call cscalc(370.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',64,r
      h=0.698734465401
      call cscalc(370.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',65,r
      h=0.785333628420
      call cscalc(370.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',66,r
      h=0.869487266137
      call cscalc(370.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',67,r
      h=0.951389552940
      call cscalc(370.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',68,r
      h=1.031240570550
      call cscalc(370.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',69,r
      h=1.109241683150
      call cscalc(370.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',70,r
      h=1.185592183420
      call cscalc(370.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',71,r
      cp=0.
      cp(7,1)=14.981132075472
      cp(7,4)=36.948509962969
      cp(7,7)=0.000000000000
      cp(7,10)=50.354495649372
      cp(7,13)=13.792452830189
      cp(7,16)=50.354495649372
      cp(7,19)=13.792452830189
      cp(7,22)=50.354495649372
      call csmcoe(7,3,1,0)
      icsash(7,1)=3
      h=1.185592183420
      call cscalc(370.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',72,r
      h=1.212843310205
      call cscalc(370.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',73,r
      h=1.244168184723
      call cscalc(370.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',74,r
      h=1.278803197320
      call cscalc(370.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',75,r
      h=1.316115616800
      call cscalc(370.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',76,r
      h=1.355573308817
      call cscalc(370.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',77,r
      h=1.396720651432
      call cscalc(370.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',78,r
      h=1.439159377263
      call cscalc(370.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',79,r
      h=1.482533166104
      call cscalc(370.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',80,r
      h=1.526514983518
      call cscalc(370.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',81,r
      h=1.570796326795
      call cscalc(370.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',82,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-23.464264498784
      cp(1,7)=30.088000000000
      cp(1,10)=-17.151345046729
      cp(1,13)=30.088000000000
      cp(1,16)=-23.464264498784
      cp(1,19)=30.088000000000
      cp(1,22)=-23.464264498784
      call csmcoe(1,3,1,0)
      icsash(1,1)=3
      h=-1.570796326795
      call cscalc(390.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',83,r
      h=-1.372188505702
      call cscalc(390.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',84,r
      h=-1.188965713425
      call cscalc(390.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',85,r
      h=-1.030572239266
      call cscalc(390.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',86,r
      h=-0.899395422962
      call cscalc(390.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',87,r
      h=-0.793321032455
      call cscalc(390.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',88,r
      h=-0.708571062520
      call cscalc(390.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',89,r
      h=-0.641370569793
      call cscalc(390.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',90,r
      h=-0.588612487575
      call cscalc(390.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',91,r
      h=-0.548014335698
      call cscalc(390.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',92,r
      h=-0.518098255499
      call cscalc(390.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',93,r
      cp=0.
      cp(2,1)=30.088000000000
      cp(2,4)=-17.151345046729
      cp(2,7)=30.088000000000
      cp(2,10)=-9.507345046729
      cp(2,13)=30.088000000000
      cp(2,16)=-17.151345046729
      cp(2,19)=30.088000000000
      cp(2,22)=-9.507345046729
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.518098255499
      call cscalc(390.,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',94,r
      h=-0.306056305849
      call cscalc(390.,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',95,r
      cp=0.
      cp(3,1)=30.088000000000
      cp(3,4)=-9.507345046729
      cp(3,7)=70.753086419753
      cp(3,10)=-7.181377639322
      cp(3,13)=30.088000000000
      cp(3,16)=-9.507345046729
      cp(3,19)=70.753086419753
      cp(3,22)=-7.181377639322
      call csmcoe(3,1,1,0)
      icsash(3,1)=1
      h=-0.306056305849
      call cscalc(390.,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',96,r
      h=-0.101152731163
      call cscalc(390.,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',97,r
      cp=0.
      cp(4,1)=70.753086419753
      cp(4,4)=-7.181377639322
      cp(4,7)=66.500000000000
      cp(4,10)=19.460597669320
      cp(4,13)=70.753086419753
      cp(4,16)=-7.181377639322
      cp(4,19)=66.500000000000
      cp(4,22)=19.460597669320
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=-0.101152731163
      call cscalc(390.,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',98,r
      h=0.284691420111
      call cscalc(390.,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',99,r
      cp=0.
      cp(5,1)=66.500000000000
      cp(5,4)=19.460597669320
      cp(5,7)=27.986206896552
      cp(5,10)=11.007766677409
      cp(5,13)=66.500000000000
      cp(5,16)=19.460597669320
      cp(5,19)=27.986206896552
      cp(5,22)=11.007766677409
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.284691420111
      call cscalc(390.,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',100,r
      h=0.374741697582
      call cscalc(390.,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',101,r
      cp=0.
      cp(6,1)=27.986206896552
      cp(6,4)=11.007766677409
      cp(6,7)=13.849056603774
      cp(6,10)=36.335743255158
      cp(6,13)=25.622641509434
      cp(6,16)=27.304318401547
      cp(6,19)=25.622641509434
      cp(6,22)=27.304318401547
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=0.374741697582
      call cscalc(390.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',102,r
      h=0.473478345988
      call cscalc(390.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',103,r
      h=0.568543140268
      call cscalc(390.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',104,r
      h=0.659858033016
      call cscalc(390.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',105,r
      h=0.747466249632
      call cscalc(390.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',106,r
      h=0.831505547795
      call cscalc(390.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',107,r
      h=0.912182377751
      call cscalc(390.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',108,r
      h=0.989749286429
      call cscalc(390.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',109,r
      h=1.064486578660
      call cscalc(390.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',110,r
      h=1.136688328201
      call cscalc(390.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',111,r
      h=1.206652303303
      call cscalc(390.,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',112,r
      cp=0.
      cp(7,1)=13.849056603774
      cp(7,4)=36.335743255158
      cp(7,7)=0.000000000000
      cp(7,10)=46.859490815340
      cp(7,13)=11.339622641509
      cp(7,16)=46.859490815340
      cp(7,19)=11.339622641509
      cp(7,22)=46.859490815340
      call csmcoe(7,3,1,0)
      icsash(7,1)=3
      h=1.206652303303
      call cscalc(390.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',113,r
      h=1.234742539744
      call cscalc(390.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',114,r
      h=1.265749597426
      call cscalc(390.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',115,r
      h=1.299177008482
      call cscalc(390.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',116,r
      h=1.334599556615
      call cscalc(390.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',117,r
      h=1.371647550103
      call cscalc(390.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',118,r
      h=1.409994105090
      call cscalc(390.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',119,r
      h=1.449344822088
      call cscalc(390.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',120,r
      h=1.489429305874
      call cscalc(390.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',121,r
      h=1.529994056395
      call cscalc(390.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',122,r
      h=1.570796326795
      call cscalc(390.,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',123,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-22.957671873000
      cp(1,7)=29.500000000000
      cp(1,10)=-18.216028037383
      cp(1,13)=29.500000000000
      cp(1,16)=-22.957671873000
      cp(1,19)=29.500000000000
      cp(1,22)=-22.957671873000
      call csmcoe(1,3,1,0)
      icsash(1,1)=3
      h=-1.570796326795
      call cscalc(414.5,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',124,r
      h=-1.371933323338
      call cscalc(414.5,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',125,r
      h=-1.189313095294
      call cscalc(414.5,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',126,r
      h=-1.032732684766
      call cscalc(414.5,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',127,r
      h=-0.904462247760
      call cscalc(414.5,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',128,r
      h=-0.802112400580
      call cscalc(414.5,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',129,r
      h=-0.721678822816
      call cscalc(414.5,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',130,r
      h=-0.659263780061
      call cscalc(414.5,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',131,r
      h=-0.611728986580
      call cscalc(414.5,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',132,r
      h=-0.576830138836
      call cscalc(414.5,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',133,r
      h=-0.553182421581
      call cscalc(414.5,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',134,r
      cp=0.
      cp(3,1)=29.500000000000
      cp(3,4)=-18.216028037383
      cp(3,7)=73.172839506173
      cp(3,10)=-18.581213222568
      cp(3,13)=29.500000000000
      cp(3,16)=-18.216028037383
      cp(3,19)=73.172839506173
      cp(3,22)=-18.581213222568
      call csmcoe(3,1,1,0)
      icsash(3,1)=1
      h=-0.553182421581
      call cscalc(414.5,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',135,r
      h=-0.248679625662
      call cscalc(414.5,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',136,r
      cp=0.
      cp(4,1)=73.172839506173
      cp(4,4)=-18.581213222568
      cp(4,7)=66.500000000000
      cp(4,10)=21.369404061382
      cp(4,13)=73.172839506173
      cp(4,16)=-18.581213222568
      cp(4,19)=66.500000000000
      cp(4,22)=21.369404061382
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=-0.248679625662
      call cscalc(414.5,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',137,r
      h=0.310922009174
      call cscalc(414.5,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',138,r
      cp=0.
      cp(5,1)=66.500000000000
      cp(5,4)=21.369404061382
      cp(5,7)=26.043103448276
      cp(5,10)=12.302247824686
      cp(5,13)=66.500000000000
      cp(5,16)=21.369404061382
      cp(5,19)=26.043103448276
      cp(5,22)=12.302247824686
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.310922009174
      call cscalc(414.5,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',139,r
      h=0.441308689770
      call cscalc(414.5,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',140,r
      cp=0.
      cp(6,1)=26.043103448276
      cp(6,4)=12.302247824686
      cp(6,7)=11.657608695652
      cp(6,10)=35.079515440878
      cp(6,13)=22.519021739130
      cp(6,16)=27.500523686755
      cp(6,19)=22.519021739130
      cp(6,22)=27.500523686755
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=0.441308689770
      call cscalc(414.5,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',141,r
      h=0.539718159584
      call cscalc(414.5,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',142,r
      h=0.633965718842
      call cscalc(414.5,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',143,r
      h=0.723938229985
      call cscalc(414.5,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',144,r
      h=0.809687904735
      call cscalc(414.5,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',145,r
      h=0.891392188460
      call cscalc(414.5,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',146,r
      h=0.969315877641
      call cscalc(414.5,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',147,r
      h=1.043779064678
      call cscalc(414.5,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',148,r
      h=1.115132164449
      call cscalc(414.5,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',149,r
      h=1.183737785344
      call cscalc(414.5,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',150,r
      h=1.249958457031
      call cscalc(414.5,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',151,r
      cp=0.
      cp(7,1)=11.657608695652
      cp(7,4)=35.079515440878
      cp(7,7)=0.000000000000
      cp(7,10)=42.578109893651
      cp(7,13)=8.519021739130
      cp(7,16)=42.578109893651
      cp(7,19)=8.519021739130
      cp(7,22)=42.578109893651
      call csmcoe(7,3,1,0)
      icsash(7,1)=3
      h=1.249958457031
      call cscalc(414.5,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',152,r
      h=1.276419616806
      call cscalc(414.5,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',153,r
      h=1.304799136576
      call cscalc(414.5,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',154,r
      h=1.334799917993
      call cscalc(414.5,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',155,r
      h=1.366158363780
      call cscalc(414.5,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',156,r
      h=1.398637692948
      call cscalc(414.5,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',157,r
      h=1.432022323408
      call cscalc(414.5,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',158,r
      h=1.466113124913
      call cscalc(414.5,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',159,r
      h=1.500723360460
      call cscalc(414.5,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',160,r
      h=1.535675152463
      call cscalc(414.5,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',161,r
      h=1.570796326795
      call cscalc(414.5,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',162,r
      end

