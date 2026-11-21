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
      call cscalc(414.50000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',1,r
      h=-1.371933323338
      call cscalc(414.50000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',2,r
      h=-1.189313095294
      call cscalc(414.50000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',3,r
      h=-1.032732684766
      call cscalc(414.50000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',4,r
      h=-0.904462247760
      call cscalc(414.50000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',5,r
      h=-0.802112400580
      call cscalc(414.50000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',6,r
      h=-0.721678822816
      call cscalc(414.50000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',7,r
      h=-0.659263780061
      call cscalc(414.50000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',8,r
      h=-0.611728986580
      call cscalc(414.50000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',9,r
      h=-0.576830138836
      call cscalc(414.50000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',10,r
      h=-0.553182421581
      call cscalc(414.50000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',11,r
      cp=0.
      cp(2,1)=29.500000000000
      cp(2,4)=-18.216028037383
      cp(2,7)=73.172839506173
      cp(2,10)=-18.581213222568
      cp(2,13)=29.500000000000
      cp(2,16)=-18.216028037383
      cp(2,19)=73.172839506173
      cp(2,22)=-18.581213222568
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.553182421581
      call cscalc(414.50000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',12,r
      h=-0.248679625662
      call cscalc(414.50000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',13,r
      cp=0.
      cp(3,1)=73.172839506173
      cp(3,4)=-18.581213222568
      cp(3,7)=66.500000000000
      cp(3,10)=21.369404061382
      cp(3,13)=73.172839506173
      cp(3,16)=-18.581213222568
      cp(3,19)=66.500000000000
      cp(3,22)=21.369404061382
      call csmcoe(3,1,1,0)
      icsash(3,1)=1
      h=-0.248679625662
      call cscalc(414.50000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',14,r
      h=0.310922009174
      call cscalc(414.50000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',15,r
      cp=0.
      cp(4,1)=66.500000000000
      cp(4,4)=21.369404061382
      cp(4,7)=26.043103448276
      cp(4,10)=12.302247824686
      cp(4,13)=66.500000000000
      cp(4,16)=21.369404061382
      cp(4,19)=26.043103448276
      cp(4,22)=12.302247824686
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=0.310922009174
      call cscalc(414.50000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',16,r
      h=0.441308689770
      call cscalc(414.50000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',17,r
      cp=0.
      cp(5,1)=26.043103448276
      cp(5,4)=12.302247824686
      cp(5,7)=11.657608695652
      cp(5,10)=35.079515440878
      cp(5,13)=22.519021739130
      cp(5,16)=27.500523686755
      cp(5,19)=22.519021739130
      cp(5,22)=27.500523686755
      call csmcoe(5,3,1,0)
      icsash(5,1)=3
      h=0.441308689770
      call cscalc(414.50000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',18,r
      h=0.539718159584
      call cscalc(414.50000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',19,r
      h=0.633965718842
      call cscalc(414.50000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',20,r
      h=0.723938229985
      call cscalc(414.50000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',21,r
      h=0.809687904735
      call cscalc(414.50000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',22,r
      h=0.891392188460
      call cscalc(414.50000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',23,r
      h=0.969315877641
      call cscalc(414.50000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',24,r
      h=1.043779064678
      call cscalc(414.50000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',25,r
      h=1.115132164449
      call cscalc(414.50000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',26,r
      h=1.183737785344
      call cscalc(414.50000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',27,r
      h=1.249958457031
      call cscalc(414.50000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',28,r
      cp=0.
      cp(6,1)=11.657608695652
      cp(6,4)=35.079515440878
      cp(6,7)=0.000000000000
      cp(6,10)=42.578109893651
      cp(6,13)=8.519021739130
      cp(6,16)=42.578109893651
      cp(6,19)=8.519021739130
      cp(6,22)=42.578109893651
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=1.249958457031
      call cscalc(414.50000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',29,r
      h=1.276419616806
      call cscalc(414.50000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',30,r
      h=1.304799136576
      call cscalc(414.50000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',31,r
      h=1.334799917993
      call cscalc(414.50000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',32,r
      h=1.366158363780
      call cscalc(414.50000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',33,r
      h=1.398637692948
      call cscalc(414.50000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',34,r
      h=1.432022323408
      call cscalc(414.50000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',35,r
      h=1.466113124913
      call cscalc(414.50000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',36,r
      h=1.500723360460
      call cscalc(414.50000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',37,r
      h=1.535675152463
      call cscalc(414.50000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',38,r
      h=1.570796326795
      call cscalc(414.50000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',39,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-22.843946997824
      cp(1,7)=34.890000000000
      cp(1,10)=-20.586021361816
      cp(1,13)=34.890000000000
      cp(1,16)=-22.843946997824
      cp(1,19)=34.890000000000
      cp(1,22)=-22.843946997824
      call csmcoe(1,3,1,0)
      icsash(1,1)=3
      h=-1.570796326795
      call cscalc(420.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',40,r
      h=-1.335992331980
      call cscalc(420.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',41,r
      h=-1.127950376507
      call cscalc(420.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',42,r
      h=-0.959439973978
      call cscalc(420.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',43,r
      h=-0.829750924915
      call cscalc(420.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',44,r
      h=-0.732339152498
      call cscalc(420.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',45,r
      h=-0.660141300930
      call cscalc(420.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',46,r
      h=-0.607481266593
      call cscalc(420.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',47,r
      h=-0.570318386938
      call cscalc(420.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',48,r
      h=-0.546011715872
      call cscalc(420.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',49,r
      h=-0.533053698719
      call cscalc(420.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',50,r
      cp=0.
      cp(2,1)=34.890000000000
      cp(2,4)=-20.586021361816
      cp(2,7)=73.716049382716
      cp(2,10)=-21.140359986154
      cp(2,13)=34.890000000000
      cp(2,16)=-20.586021361816
      cp(2,19)=73.716049382716
      cp(2,22)=-21.140359986154
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.533053698719
      call cscalc(420.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',51,r
      h=-0.279285558693
      call cscalc(420.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',52,r
      cp=0.
      cp(3,1)=73.716049382716
      cp(3,4)=-21.140359986154
      cp(3,7)=66.500000000000
      cp(3,10)=21.797911618784
      cp(3,13)=73.716049382716
      cp(3,16)=-21.140359986154
      cp(3,19)=66.500000000000
      cp(3,22)=21.797911618784
      call csmcoe(3,1,1,0)
      icsash(3,1)=1
      h=-0.279285558693
      call cscalc(420.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',53,r
      h=0.316751610120
      call cscalc(420.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',54,r
      cp=0.
      cp(4,1)=66.500000000000
      cp(4,4)=21.797911618784
      cp(4,7)=25.606896551724
      cp(4,10)=12.592845633258
      cp(4,13)=66.500000000000
      cp(4,16)=21.797911618784
      cp(4,19)=25.606896551724
      cp(4,22)=12.592845633258
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=0.316751610120
      call cscalc(420.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',55,r
      h=0.457046428067
      call cscalc(420.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',56,r
      cp=0.
      cp(5,1)=25.606896551724
      cp(5,4)=12.592845633258
      cp(5,7)=10.880434782609
      cp(5,10)=34.618295408371
      cp(5,13)=21.951086956522
      cp(5,16)=27.544569771189
      cp(5,19)=21.951086956522
      cp(5,22)=27.544569771189
      call csmcoe(5,3,1,0)
      icsash(5,1)=3
      h=0.457046428067
      call cscalc(420.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',57,r
      h=0.554723868215
      call cscalc(420.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',58,r
      h=0.648367119633
      call cscalc(420.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',59,r
      h=0.737903548078
      call cscalc(420.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',60,r
      h=0.823408640443
      call cscalc(420.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',61,r
      h=0.905069482902
      call cscalc(420.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',62,r
      h=0.983150828564
      call cscalc(420.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',63,r
      h=1.057966613600
      call cscalc(420.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',64,r
      h=1.129857843378
      call cscalc(420.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',65,r
      h=1.199176554073
      call cscalc(420.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',66,r
      h=1.266274951866
      call cscalc(420.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',67,r
      cp=0.
      cp(6,1)=10.880434782609
      cp(6,4)=34.618295408371
      cp(6,7)=0.000000000000
      cp(6,10)=41.616983564293
      cp(6,13)=7.951086956522
      cp(6,16)=41.616983564293
      cp(6,19)=7.951086956522
      cp(6,22)=41.616983564293
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=1.266274951866
      call cscalc(420.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',68,r
      h=1.291037744534
      call cscalc(420.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',69,r
      h=1.317734603101
      call cscalc(420.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',70,r
      h=1.346070335423
      call cscalc(420.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',71,r
      h=1.375781370423
      call cscalc(420.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',72,r
      h=1.406629721935
      call cscalc(420.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',73,r
      h=1.438397811316
      call cscalc(420.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',74,r
      h=1.470884015081
      call cscalc(420.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',75,r
      h=1.503898800602
      call cscalc(420.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',76,r
      h=1.537261318296
      call cscalc(420.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',77,r
      h=1.570796326795
      call cscalc(420.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',78,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-22.740560747664
      cp(1,7)=39.790000000000
      cp(1,10)=-22.740560747664
      cp(1,13)=0.000000000000
      cp(1,16)=-22.740560747664
      cp(1,19)=39.790000000000
      cp(1,22)=-22.740560747664
      call csmcoe(1,1,1,0)
      icsash(1,1)=1
      h=-1.570796326795
      call cscalc(425.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',79,r
      h=-0.519210865900
      call cscalc(425.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',80,r
      cp=0.
      cp(2,1)=39.790000000000
      cp(2,4)=-22.740560747664
      cp(2,7)=74.209876543210
      cp(2,10)=-23.466857043960
      cp(2,13)=39.790000000000
      cp(2,16)=-22.740560747664
      cp(2,19)=74.209876543210
      cp(2,22)=-23.466857043960
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.519210865900
      call cscalc(425.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',81,r
      h=-0.306272880277
      call cscalc(425.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',82,r
      cp=0.
      cp(3,1)=74.209876543210
      cp(3,4)=-23.466857043960
      cp(3,7)=66.500000000000
      cp(3,10)=22.187463943694
      cp(3,13)=74.209876543210
      cp(3,16)=-23.466857043960
      cp(3,19)=66.500000000000
      cp(3,22)=22.187463943694
      call csmcoe(3,1,1,0)
      icsash(3,1)=1
      h=-0.306272880277
      call cscalc(425.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',83,r
      h=0.322031994891
      call cscalc(425.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',84,r
      cp=0.
      cp(4,1)=66.500000000000
      cp(4,4)=22.187463943694
      cp(4,7)=25.210344827586
      cp(4,10)=12.857025459233
      cp(4,13)=66.500000000000
      cp(4,16)=22.187463943694
      cp(4,19)=25.210344827586
      cp(4,22)=12.857025459233
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=0.322031994891
      call cscalc(425.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',85,r
      h=0.471607685486
      call cscalc(425.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',86,r
      cp=0.
      cp(5,1)=25.210344827586
      cp(5,4)=12.857025459233
      cp(5,7)=10.173913043478
      cp(5,10)=34.199004469728
      cp(5,13)=21.434782608696
      cp(5,16)=27.584611666130
      cp(5,19)=21.434782608696
      cp(5,22)=27.584611666130
      call csmcoe(5,3,1,0)
      icsash(5,1)=3
      h=0.471607685486
      call cscalc(425.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',87,r
      h=0.568600677193
      call cscalc(425.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',88,r
      h=0.661689684392
      call cscalc(425.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',89,r
      h=0.750837291740
      call cscalc(425.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',90,r
      h=0.836138591050
      call cscalc(425.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',91,r
      h=0.917788078173
      call cscalc(425.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',92,r
      h=0.996049329989
      call cscalc(425.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',93,r
      h=1.071229725563
      call cscalc(425.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',94,r
      h=1.143660876026
      call cscalc(425.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',95,r
      h=1.213684437602
      call cscalc(425.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',96,r
      h=1.281642496935
      call cscalc(425.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',97,r
      cp=0.
      cp(6,1)=10.173913043478
      cp(6,4)=34.199004469728
      cp(6,7)=0.000000000000
      cp(6,10)=40.743232355785
      cp(6,13)=7.434782608696
      cp(6,16)=40.743232355785
      cp(6,19)=7.434782608696
      cp(6,22)=40.743232355785
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=1.281642496935
      call cscalc(425.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',98,r
      h=1.304831968782
      call cscalc(425.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',99,r
      h=1.329960498307
      call cscalc(425.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',100,r
      h=1.356736648515
      call cscalc(425.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',101,r
      h=1.384898498941
      call cscalc(425.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',102,r
      h=1.414208275810
      call cscalc(425.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',103,r
      h=1.444447642182
      call cscalc(425.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',104,r
      h=1.475413571379
      call cscalc(425.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',105,r
      h=1.506914708550
      call cscalc(425.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',106,r
      h=1.538768119558
      call cscalc(425.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',107,r
      h=1.570796326795
      call cscalc(425.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',108,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-25.964906542056
      cp(1,7)=40.895000000000
      cp(1,10)=-25.964906542056
      cp(1,13)=0.000000000000
      cp(1,16)=-25.964906542056
      cp(1,19)=40.895000000000
      cp(1,22)=-25.964906542056
      call csmcoe(1,1,1,0)
      icsash(1,1)=1
      h=-1.570796326795
      call cscalc(429.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',109,r
      h=-0.565698456787
      call cscalc(429.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',110,r
      cp=0.
      cp(2,1)=40.895000000000
      cp(2,4)=-25.964906542056
      cp(2,7)=74.604938271605
      cp(2,10)=-25.328054690204
      cp(2,13)=40.895000000000
      cp(2,16)=-25.964906542056
      cp(2,19)=74.604938271605
      cp(2,22)=-25.328054690204
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.565698456787
      call cscalc(429.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',111,r
      h=-0.327286380940
      call cscalc(429.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',112,r
      cp=0.
      cp(3,1)=74.604938271605
      cp(3,4)=-25.328054690204
      cp(3,7)=66.500000000000
      cp(3,10)=22.499105803623
      cp(3,13)=74.604938271605
      cp(3,16)=-25.328054690204
      cp(3,19)=66.500000000000
      cp(3,22)=22.499105803623
      call csmcoe(3,1,1,0)
      icsash(3,1)=1
      h=-0.327286380940
      call cscalc(429.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',113,r
      h=0.326242963040
      call cscalc(429.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',114,r
      cp=0.
      cp(4,1)=66.500000000000
      cp(4,4)=22.499105803623
      cp(4,7)=24.893103448276
      cp(4,10)=13.068369320013
      cp(4,13)=66.500000000000
      cp(4,16)=22.499105803623
      cp(4,19)=24.893103448276
      cp(4,22)=13.068369320013
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=0.326242963040
      call cscalc(429.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',115,r
      h=0.483430940902
      call cscalc(429.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',116,r
      cp=0.
      cp(5,1)=24.893103448276
      cp(5,4)=13.068369320013
      cp(5,7)=9.608695652174
      cp(5,10)=33.863571718813
      cp(5,13)=21.021739130435
      cp(5,16)=27.616645182082
      cp(5,19)=21.021739130435
      cp(5,22)=27.616645182082
      call csmcoe(5,3,1,0)
      icsash(5,1)=3
      h=0.483430940902
      call cscalc(429.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',117,r
      h=0.579863162515
      call cscalc(429.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',118,r
      h=0.672505804477
      call cscalc(429.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',119,r
      h=0.761348410282
      call cscalc(429.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',120,r
      h=0.846500606500
      call cscalc(429.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',121,r
      h=0.928161820231
      call cscalc(429.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',122,r
      h=1.006593842212
      call cscalc(429.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',123,r
      h=1.082098074434
      call cscalc(429.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',124,r
      h=1.154997951417
      call cscalc(429.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',125,r
      h=1.225626197724
      call cscalc(429.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',126,r
      h=1.294316183138
      call cscalc(429.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',127,r
      cp=0.
      cp(6,1)=9.608695652174
      cp(6,4)=33.863571718813
      cp(6,7)=0.000000000000
      cp(6,10)=40.044231388978
      cp(6,13)=7.021739130435
      cp(6,16)=40.044231388978
      cp(6,19)=7.021739130435
      cp(6,22)=40.044231388978
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=1.294316183138
      call cscalc(429.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',128,r
      h=1.316228275573
      call cscalc(429.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',129,r
      h=1.340076143722
      call cscalc(429.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',130,r
      h=1.365572859462
      call cscalc(429.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',131,r
      h=1.392459058513
      call cscalc(429.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',132,r
      h=1.420498149680
      call cscalc(429.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',133,r
      h=1.449472022464
      call cscalc(429.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',134,r
      h=1.479177220171
      call cscalc(429.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',135,r
      h=1.509421516553
      call cscalc(429.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',136,r
      h=1.540020820367
      call cscalc(429.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',137,r
      h=1.570796326795
      call cscalc(429.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',138,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-29.189252336449
      cp(1,7)=42.000000000000
      cp(1,10)=-29.189252336449
      cp(1,13)=0.000000000000
      cp(1,16)=-29.189252336449
      cp(1,19)=42.000000000000
      cp(1,22)=-29.189252336449
      call csmcoe(1,1,1,0)
      icsash(1,1)=1
      h=-1.570796326795
      call cscalc(433.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',139,r
      h=-0.607350367673
      call cscalc(433.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',140,r
      cp=0.
      cp(2,1)=42.000000000000
      cp(2,4)=-29.189252336449
      cp(2,7)=75.000000000000
      cp(2,10)=-27.189252336449
      cp(2,13)=42.000000000000
      cp(2,16)=-29.189252336449
      cp(2,19)=75.000000000000
      cp(2,22)=-27.189252336449
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.607350367673
      call cscalc(433.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',141,r
      h=-0.347787638539
      call cscalc(433.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',142,r
      cp=0.
      cp(3,1)=75.000000000000
      cp(3,4)=-27.189252336449
      cp(3,7)=66.500000000000
      cp(3,10)=22.810747663551
      cp(3,13)=75.000000000000
      cp(3,16)=-27.189252336449
      cp(3,19)=66.500000000000
      cp(3,22)=22.810747663551
      call csmcoe(3,1,1,0)
      icsash(3,1)=1
      h=-0.347787638539
      call cscalc(433.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',143,r
      h=0.330441966559
      call cscalc(433.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',144,r
      cp=0.
      cp(4,1)=66.500000000000
      cp(4,4)=22.810747663551
      cp(4,7)=24.575862068966
      cp(4,10)=13.279713180793
      cp(4,13)=66.500000000000
      cp(4,16)=22.810747663551
      cp(4,19)=24.575862068966
      cp(4,22)=13.279713180793
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=0.330441966559
      call cscalc(433.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',145,r
      h=0.495408807265
      call cscalc(433.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',146,r
      cp=0.
      cp(5,1)=24.575862068966
      cp(5,4)=13.279713180793
      cp(5,7)=9.043478260870
      cp(5,10)=33.528138967899
      cp(5,13)=20.608695652174
      cp(5,16)=27.648678698034
      cp(5,19)=20.608695652174
      cp(5,22)=27.648678698034
      call csmcoe(5,3,1,0)
      icsash(5,1)=3
      h=0.495408807265
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',147,r
      h=0.591268347782
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',148,r
      h=0.683462301368
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',149,r
      h=0.772005992199
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',150,r
      h=0.857022490492
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',151,r
      h=0.938715210101
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',152,r
      h=1.017343344475
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',153,r
      h=1.093201599671
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',154,r
      h=1.166604563848
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',155,r
      h=1.237875374303
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',156,r
      h=1.307338017247
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',157,r
      cp=0.
      cp(6,1)=9.043478260870
      cp(6,4)=33.528138967899
      cp(6,7)=0.000000000000
      cp(6,10)=39.345230422172
      cp(6,13)=6.608695652174
      cp(6,16)=39.345230422172
      cp(6,19)=6.608695652174
      cp(6,22)=39.345230422172
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=1.307338017247
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',158,r
      h=1.327957447979
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',159,r
      h=1.350502117902
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',160,r
      h=1.374691035132
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',161,r
      h=1.400268587381
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',162,r
      h=1.427000364029
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',163,r
      h=1.454669316068
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',164,r
      h=1.483072262045
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',165,r
      h=1.512016710243
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',166,r
      h=1.541317946555
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',167,r
      h=1.570796326795
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',168,r
      end
