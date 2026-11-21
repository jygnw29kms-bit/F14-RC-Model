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
      write(*,*) 'CHECK',1,r
      h=-0.607350367673
      call cscalc(433.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',2,r
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
      write(*,*) 'CHECK',3,r
      h=-0.347787638539
      call cscalc(433.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',4,r
      cp=0.
      cp(4,1)=75.000000000000
      cp(4,4)=-27.189252336449
      cp(4,7)=66.500000000000
      cp(4,10)=22.810747663551
      cp(4,13)=75.000000000000
      cp(4,16)=-27.189252336449
      cp(4,19)=66.500000000000
      cp(4,22)=22.810747663551
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=-0.347787638539
      call cscalc(433.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',5,r
      h=0.330441966559
      call cscalc(433.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',6,r
      cp=0.
      cp(5,1)=66.500000000000
      cp(5,4)=22.810747663551
      cp(5,7)=24.575862068966
      cp(5,10)=13.279713180793
      cp(5,13)=66.500000000000
      cp(5,16)=22.810747663551
      cp(5,19)=24.575862068966
      cp(5,22)=13.279713180793
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.330441966559
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',7,r
      h=0.495408807265
      call cscalc(433.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',8,r
      cp=0.
      cp(6,1)=24.575862068966
      cp(6,4)=13.279713180793
      cp(6,7)=9.043478260870
      cp(6,10)=33.528138967899
      cp(6,13)=20.608695652174
      cp(6,16)=27.648678698034
      cp(6,19)=20.608695652174
      cp(6,22)=27.648678698034
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=0.495408807265
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',9,r
      h=0.576601728263
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',10,r
      h=0.657794649261
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',11,r
      h=0.738987570259
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',12,r
      h=0.820180491258
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',13,r
      h=0.901373412256
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',14,r
      h=0.982566333254
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',15,r
      h=1.063759254252
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',16,r
      h=1.144952175251
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',17,r
      h=1.226145096249
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',18,r
      h=1.307338017247
      call cscalc(433.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',19,r
      cp=0.
      cp(7,1)=9.043478260870
      cp(7,4)=33.528138967899
      cp(7,7)=0.000000000000
      cp(7,10)=39.345230422172
      cp(7,13)=6.608695652174
      cp(7,16)=39.345230422172
      cp(7,19)=6.608695652174
      cp(7,22)=39.345230422172
      call csmcoe(7,3,1,0)
      icsash(7,1)=3
      h=1.307338017247
      call cscalc(433.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',20,r
      h=1.333683848202
      call cscalc(433.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',21,r
      h=1.360029679157
      call cscalc(433.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',22,r
      h=1.386375510111
      call cscalc(433.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',23,r
      h=1.412721341066
      call cscalc(433.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',24,r
      h=1.439067172021
      call cscalc(433.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',25,r
      h=1.465413002976
      call cscalc(433.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',26,r
      h=1.491758833931
      call cscalc(433.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',27,r
      h=1.518104664885
      call cscalc(433.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',28,r
      h=1.544450495840
      call cscalc(433.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',29,r
      h=1.570796326795
      call cscalc(433.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',30,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-31.672721962617
      cp(1,7)=43.142187500000
      cp(1,10)=-31.672721962617
      cp(1,13)=0.000000000000
      cp(1,16)=-31.672721962617
      cp(1,19)=43.142187500000
      cp(1,22)=-31.672721962617
      call csmcoe(1,1,1,0)
      icsash(1,1)=1
      h=-1.570796326795
      call cscalc(450.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',31,r
      h=-0.633277965649
      call cscalc(450.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',32,r
      cp=0.
      cp(2,1)=43.142187500000
      cp(2,4)=-31.672721962617
      cp(2,7)=72.476562500000
      cp(2,10)=-29.353971962617
      cp(2,13)=43.142187500000
      cp(2,16)=-31.672721962617
      cp(2,19)=72.476562500000
      cp(2,22)=-29.353971962617
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.633277965649
      call cscalc(450.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',33,r
      h=-0.384820704875
      call cscalc(450.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',34,r
      cp=0.
      cp(3,1)=72.476562500000
      cp(3,4)=-29.353971962617
      cp(3,7)=74.734375000000
      cp(3,10)=-25.502409462617
      cp(3,13)=75.318750000000
      cp(3,16)=-28.822721962617
      cp(3,19)=75.318750000000
      cp(3,22)=-28.822721962617
      call csmcoe(3,3,1,0)
      icsash(3,1)=3
      h=-0.384820704875
      call cscalc(450.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',35,r
      h=-0.379223655510
      call cscalc(450.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',36,r
      h=-0.373626606144
      call cscalc(450.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',37,r
      h=-0.368029556778
      call cscalc(450.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',38,r
      h=-0.362432507412
      call cscalc(450.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',39,r
      h=-0.356835458046
      call cscalc(450.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',40,r
      h=-0.351238408680
      call cscalc(450.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',41,r
      h=-0.345641359314
      call cscalc(450.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',42,r
      h=-0.340044309949
      call cscalc(450.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',43,r
      h=-0.334447260583
      call cscalc(450.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',44,r
      h=-0.328850211217
      call cscalc(450.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',45,r
      cp=0.
      cp(4,1)=74.734375000000
      cp(4,4)=-25.502409462617
      cp(4,7)=66.500000000000
      cp(4,10)=23.435090537383
      cp(4,13)=74.734375000000
      cp(4,16)=-25.502409462617
      cp(4,19)=66.500000000000
      cp(4,22)=23.435090537383
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=-0.328850211217
      call cscalc(450.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',46,r
      h=0.338817863598
      call cscalc(450.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',47,r
      cp=0.
      cp(5,1)=66.500000000000
      cp(5,4)=23.435090537383
      cp(5,7)=23.227586206897
      cp(5,10)=14.177924589107
      cp(5,13)=66.500000000000
      cp(5,16)=23.435090537383
      cp(5,19)=23.227586206897
      cp(5,22)=14.177924589107
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.338817863598
      call cscalc(450.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',48,r
      h=0.548025399848
      call cscalc(450.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',49,r
      cp=0.
      cp(6,1)=23.227586206897
      cp(6,4)=14.177924589107
      cp(6,7)=6.641304347826
      cp(6,10)=32.102549776514
      cp(6,13)=18.853260869565
      cp(6,16)=27.784821140831
      cp(6,19)=18.853260869565
      cp(6,22)=27.784821140831
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=0.548025399848
      call cscalc(450.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',50,r
      h=0.629902494355
      call cscalc(450.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',51,r
      h=0.711779588862
      call cscalc(450.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',52,r
      h=0.793656683368
      call cscalc(450.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',53,r
      h=0.875533777875
      call cscalc(450.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',54,r
      h=0.957410872382
      call cscalc(450.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',55,r
      h=1.039287966889
      call cscalc(450.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',56,r
      h=1.121165061396
      call cscalc(450.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',57,r
      h=1.203042155902
      call cscalc(450.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',58,r
      h=1.284919250409
      call cscalc(450.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',59,r
      h=1.366796344916
      call cscalc(450.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',60,r
      cp=0.
      cp(7,1)=6.641304347826
      cp(7,4)=32.102549776514
      cp(7,7)=0.000000000000
      cp(7,10)=36.374476313245
      cp(7,13)=4.853260869565
      cp(7,16)=36.374476313245
      cp(7,19)=4.853260869565
      cp(7,22)=36.374476313245
      call csmcoe(7,3,1,0)
      icsash(7,1)=3
      h=1.366796344916
      call cscalc(450.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',61,r
      h=1.387196343104
      call cscalc(450.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',62,r
      h=1.407596341292
      call cscalc(450.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',63,r
      h=1.427996339480
      call cscalc(450.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',64,r
      h=1.448396337668
      call cscalc(450.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',65,r
      h=1.468796335855
      call cscalc(450.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',66,r
      h=1.489196334043
      call cscalc(450.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',67,r
      h=1.509596332231
      call cscalc(450.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',68,r
      h=1.529996330419
      call cscalc(450.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',69,r
      h=1.550396328607
      call cscalc(450.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',70,r
      h=1.570796326795
      call cscalc(450.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',71,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-35.324883177570
      cp(1,7)=44.821875000000
      cp(1,10)=-35.324883177570
      cp(1,13)=0.000000000000
      cp(1,16)=-35.324883177570
      cp(1,19)=44.821875000000
      cp(1,22)=-35.324883177570
      call csmcoe(1,1,1,0)
      icsash(1,1)=1
      h=-1.570796326795
      call cscalc(475.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',72,r
      h=-0.667453115057
      call cscalc(475.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',73,r
      cp=0.
      cp(2,1)=44.821875000000
      cp(2,4)=-35.324883177570
      cp(2,7)=68.765625000000
      cp(2,10)=-32.537383177570
      cp(2,13)=44.821875000000
      cp(2,16)=-35.324883177570
      cp(2,19)=68.765625000000
      cp(2,22)=-32.537383177570
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.667453115057
      call cscalc(475.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',74,r
      h=-0.441948843660
      call cscalc(475.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',75,r
      cp=0.
      cp(3,1)=68.765625000000
      cp(3,4)=-32.537383177570
      cp(3,7)=74.343750000000
      cp(3,10)=-23.021758177570
      cp(3,13)=75.787500000000
      cp(3,16)=-31.224883177570
      cp(3,19)=75.787500000000
      cp(3,22)=-31.224883177570
      call csmcoe(3,3,1,0)
      icsash(3,1)=3
      h=-0.441948843660
      call cscalc(475.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',76,r
      h=-0.427784084262
      call cscalc(475.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',77,r
      h=-0.413619324865
      call cscalc(475.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',78,r
      h=-0.399454565467
      call cscalc(475.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',79,r
      h=-0.385289806069
      call cscalc(475.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',80,r
      h=-0.371125046671
      call cscalc(475.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',81,r
      h=-0.356960287273
      call cscalc(475.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',82,r
      h=-0.342795527875
      call cscalc(475.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',83,r
      h=-0.328630768478
      call cscalc(475.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',84,r
      h=-0.314466009080
      call cscalc(475.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',85,r
      h=-0.300301249682
      call cscalc(475.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',86,r
      cp=0.
      cp(4,1)=74.343750000000
      cp(4,4)=-23.021758177570
      cp(4,7)=66.500000000000
      cp(4,10)=24.353241822430
      cp(4,13)=74.343750000000
      cp(4,16)=-23.021758177570
      cp(4,19)=66.500000000000
      cp(4,22)=24.353241822430
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=-0.300301249682
      call cscalc(475.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',87,r
      h=0.351045858567
      call cscalc(475.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',88,r
      cp=0.
      cp(5,1)=66.500000000000
      cp(5,4)=24.353241822430
      cp(5,7)=21.244827586207
      cp(5,10)=15.498823718982
      cp(5,13)=66.500000000000
      cp(5,16)=24.353241822430
      cp(5,19)=21.244827586207
      cp(5,22)=15.498823718982
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.351045858567
      call cscalc(475.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',89,r
      h=0.630273680674
      call cscalc(475.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',90,r
      cp=0.
      cp(6,1)=21.244827586207
      cp(6,4)=15.498823718982
      cp(6,7)=3.108695652174
      cp(6,10)=30.006095083299
      cp(6,13)=16.271739130435
      cp(6,16)=27.985030615533
      cp(6,19)=16.271739130435
      cp(6,22)=27.985030615533
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=0.630273680674
      call cscalc(475.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',91,r
      h=0.714002561213
      call cscalc(475.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',92,r
      h=0.797731441751
      call cscalc(475.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',93,r
      h=0.881460322290
      call cscalc(475.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',94,r
      h=0.965189202829
      call cscalc(475.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',95,r
      h=1.048918083368
      call cscalc(475.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',96,r
      h=1.132646963907
      call cscalc(475.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',97,r
      h=1.216375844445
      call cscalc(475.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',98,r
      h=1.300104724984
      call cscalc(475.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',99,r
      h=1.383833605523
      call cscalc(475.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',100,r
      h=1.467562486062
      call cscalc(475.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',101,r
      cp=0.
      cp(7,1)=3.108695652174
      cp(7,4)=30.006095083299
      cp(7,7)=0.000000000000
      cp(7,10)=32.005720270706
      cp(7,13)=2.271739130435
      cp(7,16)=32.005720270706
      cp(7,19)=2.271739130435
      cp(7,22)=32.005720270706
      call csmcoe(7,3,1,0)
      icsash(7,1)=3
      h=1.467562486062
      call cscalc(475.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',102,r
      h=1.477885870135
      call cscalc(475.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',103,r
      h=1.488209254208
      call cscalc(475.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',104,r
      h=1.498532638282
      call cscalc(475.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',105,r
      h=1.508856022355
      call cscalc(475.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',106,r
      h=1.519179406428
      call cscalc(475.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',107,r
      h=1.529502790502
      call cscalc(475.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',108,r
      h=1.539826174575
      call cscalc(475.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',109,r
      h=1.550149558648
      call cscalc(475.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',110,r
      h=1.560472942722
      call cscalc(475.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',111,r
      h=1.570796326795
      call cscalc(475.00000000,1,7,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',112,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-38.538785046729
      cp(1,7)=46.300000000000
      cp(1,10)=-38.538785046729
      cp(1,13)=0.000000000000
      cp(1,16)=-38.538785046729
      cp(1,19)=46.300000000000
      cp(1,22)=-38.538785046729
      call csmcoe(1,1,1,0)
      icsash(1,1)=1
      h=-1.570796326795
      call cscalc(497.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',113,r
      h=-0.694170171750
      call cscalc(497.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',114,r
      cp=0.
      cp(2,1)=46.300000000000
      cp(2,4)=-38.538785046729
      cp(2,7)=65.500000000000
      cp(2,10)=-35.338785046729
      cp(2,13)=46.300000000000
      cp(2,16)=-38.538785046729
      cp(2,19)=65.500000000000
      cp(2,22)=-35.338785046729
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.694170171750
      call cscalc(497.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',115,r
      h=-0.494764218004
      call cscalc(497.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',116,r
      cp=0.
      cp(3,1)=65.500000000000
      cp(3,4)=-35.338785046729
      cp(3,7)=74.000000000000
      cp(3,10)=-20.838785046729
      cp(3,13)=76.200000000000
      cp(3,16)=-33.338785046729
      cp(3,19)=76.200000000000
      cp(3,22)=-33.338785046729
      call csmcoe(3,3,1,0)
      icsash(3,1)=3
      h=-0.494764218004
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',117,r
      h=-0.472737454847
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',118,r
      h=-0.450710691691
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',119,r
      h=-0.428683928535
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',120,r
      h=-0.406657165379
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',121,r
      h=-0.384630402223
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',122,r
      h=-0.362603639067
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',123,r
      h=-0.340576875910
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',124,r
      h=-0.318550112754
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',125,r
      h=-0.296523349598
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',126,r
      h=-0.274496586442
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',127,r
      cp=0.
      cp(4,1)=74.000000000000
      cp(4,4)=-20.838785046729
      cp(4,7)=66.500000000000
      cp(4,10)=25.161214953271
      cp(4,13)=74.000000000000
      cp(4,16)=-20.838785046729
      cp(4,19)=66.500000000000
      cp(4,22)=25.161214953271
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=-0.274496586442
      call cscalc(497.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',128,r
      h=0.361716781599
      call cscalc(497.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',129,r
      cp=0.
      cp(5,1)=66.500000000000
      cp(5,4)=25.161214953271
      cp(5,7)=19.500000000000
      cp(5,10)=16.661214953271
      cp(5,13)=66.500000000000
      cp(5,16)=25.161214953271
      cp(5,19)=19.500000000000
      cp(5,22)=16.661214953271
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.361716781599
      call cscalc(497.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',130,r
      h=0.707055251367
      call cscalc(497.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',131,r
      cp=0.
      cp(6,1)=19.500000000000
      cp(6,4)=16.661214953271
      cp(6,7)=0.000000000000
      cp(6,10)=28.161214953271
      cp(6,13)=14.000000000000
      cp(6,16)=28.161214953271
      cp(6,19)=14.000000000000
      cp(6,22)=28.161214953271
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=0.707055251367
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',132,r
      h=0.793429358909
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',133,r
      h=0.879803466452
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',134,r
      h=0.966177573995
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',135,r
      h=1.052551681538
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',136,r
      h=1.138925789081
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',137,r
      h=1.225299896624
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',138,r
      h=1.311674004166
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',139,r
      h=1.398048111709
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',140,r
      h=1.484422219252
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',141,r
      h=1.570796326795
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',142,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-38.538785046729
      cp(1,7)=46.300000000000
      cp(1,10)=-38.538785046729
      cp(1,13)=0.000000000000
      cp(1,16)=-38.538785046729
      cp(1,19)=46.300000000000
      cp(1,22)=-38.538785046729
      call csmcoe(1,1,1,0)
      icsash(1,1)=1
      h=-1.570796326795
      call cscalc(497.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',143,r
      h=-0.694170171750
      call cscalc(497.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',144,r
      cp=0.
      cp(2,1)=46.300000000000
      cp(2,4)=-38.538785046729
      cp(2,7)=65.500000000000
      cp(2,10)=-35.338785046729
      cp(2,13)=46.300000000000
      cp(2,16)=-38.538785046729
      cp(2,19)=65.500000000000
      cp(2,22)=-35.338785046729
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.694170171750
      call cscalc(497.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',145,r
      h=-0.494764218004
      call cscalc(497.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',146,r
      cp=0.
      cp(3,1)=65.500000000000
      cp(3,4)=-35.338785046729
      cp(3,7)=74.000000000000
      cp(3,10)=-20.838785046729
      cp(3,13)=76.200000000000
      cp(3,16)=-33.338785046729
      cp(3,19)=76.200000000000
      cp(3,22)=-33.338785046729
      call csmcoe(3,3,1,0)
      icsash(3,1)=3
      h=-0.494764218004
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',147,r
      h=-0.472737454847
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',148,r
      h=-0.450710691691
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',149,r
      h=-0.428683928535
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',150,r
      h=-0.406657165379
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',151,r
      h=-0.384630402223
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',152,r
      h=-0.362603639067
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',153,r
      h=-0.340576875910
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',154,r
      h=-0.318550112754
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',155,r
      h=-0.296523349598
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',156,r
      h=-0.274496586442
      call cscalc(497.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',157,r
      cp=0.
      cp(4,1)=74.000000000000
      cp(4,4)=-20.838785046729
      cp(4,7)=66.500000000000
      cp(4,10)=25.161214953271
      cp(4,13)=74.000000000000
      cp(4,16)=-20.838785046729
      cp(4,19)=66.500000000000
      cp(4,22)=25.161214953271
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=-0.274496586442
      call cscalc(497.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',158,r
      h=0.361716781599
      call cscalc(497.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',159,r
      cp=0.
      cp(5,1)=66.500000000000
      cp(5,4)=25.161214953271
      cp(5,7)=19.500000000000
      cp(5,10)=16.661214953271
      cp(5,13)=66.500000000000
      cp(5,16)=25.161214953271
      cp(5,19)=19.500000000000
      cp(5,22)=16.661214953271
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.361716781599
      call cscalc(497.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',160,r
      h=0.707055251367
      call cscalc(497.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',161,r
      cp=0.
      cp(6,1)=19.500000000000
      cp(6,4)=16.661214953271
      cp(6,7)=0.000000000000
      cp(6,10)=28.161214953271
      cp(6,13)=14.000000000000
      cp(6,16)=28.161214953271
      cp(6,19)=14.000000000000
      cp(6,22)=28.161214953271
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=0.707055251367
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',162,r
      h=0.793429358909
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',163,r
      h=0.879803466452
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',164,r
      h=0.966177573995
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',165,r
      h=1.052551681538
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',166,r
      h=1.138925789081
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',167,r
      h=1.225299896624
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',168,r
      h=1.311674004166
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',169,r
      h=1.398048111709
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',170,r
      h=1.484422219252
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',171,r
      h=1.570796326795
      call cscalc(497.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',172,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-40.375634178905
      cp(1,7)=46.985714285714
      cp(1,10)=-40.375634178905
      cp(1,13)=0.000000000000
      cp(1,16)=-40.375634178905
      cp(1,19)=46.985714285714
      cp(1,22)=-40.375634178905
      call csmcoe(1,1,1,0)
      icsash(1,1)=1
      h=-1.570796326795
      call cscalc(525.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',173,r
      h=-0.709878392236
      call cscalc(525.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',174,r
      cp=0.
      cp(2,1)=46.985714285714
      cp(2,4)=-40.375634178905
      cp(2,7)=62.928571428571
      cp(2,10)=-37.689919893191
      cp(2,13)=46.985714285714
      cp(2,16)=-40.375634178905
      cp(2,19)=62.928571428571
      cp(2,22)=-37.689919893191
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.709878392236
      call cscalc(525.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',175,r
      h=-0.539633657774
      call cscalc(525.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',176,r
      cp=0.
      cp(3,1)=62.928571428571
      cp(3,4)=-37.689919893191
      cp(3,7)=73.428571428571
      cp(3,10)=-13.189919893191
      cp(3,13)=77.057142857143
      cp(3,16)=-35.118491321762
      cp(3,19)=77.057142857143
      cp(3,22)=-35.118491321762
      call csmcoe(3,3,1,0)
      icsash(3,1)=3
      h=-0.539633657774
      call cscalc(525.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',177,r
      h=-0.503443672927
      call cscalc(525.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',178,r
      h=-0.467253688080
      call cscalc(525.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',179,r
      h=-0.431063703233
      call cscalc(525.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',180,r
      h=-0.394873718386
      call cscalc(525.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',181,r
      h=-0.358683733539
      call cscalc(525.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',182,r
      h=-0.322493748692
      call cscalc(525.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',183,r
      h=-0.286303763845
      call cscalc(525.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',184,r
      h=-0.250113778998
      call cscalc(525.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',185,r
      h=-0.213923794151
      call cscalc(525.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',186,r
      h=-0.177733809304
      call cscalc(525.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',187,r
      cp=0.
      cp(4,1)=73.428571428571
      cp(4,4)=-13.189919893191
      cp(4,7)=67.357142857143
      cp(4,10)=24.238651535381
      cp(4,13)=73.428571428571
      cp(4,16)=-13.189919893191
      cp(4,19)=67.357142857143
      cp(4,22)=24.238651535381
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=-0.177733809304
      call cscalc(525.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',188,r
      h=0.345425198162
      call cscalc(525.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',189,r
      cp=0.
      cp(5,1)=67.357142857143
      cp(5,4)=24.238651535381
      cp(5,7)=16.357142857143
      cp(5,10)=16.881508678238
      cp(5,13)=67.357142857143
      cp(5,16)=24.238651535381
      cp(5,19)=16.357142857143
      cp(5,22)=16.881508678238
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.345425198162
      call cscalc(525.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',190,r
      h=0.801172639881
      call cscalc(525.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',191,r
      cp=0.
      cp(6,1)=16.357142857143
      cp(6,4)=16.881508678238
      cp(6,7)=0.000000000000
      cp(6,10)=25.238651535381
      cp(6,13)=10.285714285714
      cp(6,16)=25.238651535381
      cp(6,19)=10.285714285714
      cp(6,22)=25.238651535381
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=0.801172639881
      call cscalc(525.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',192,r
      h=0.878135008573
      call cscalc(525.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',193,r
      h=0.955097377264
      call cscalc(525.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',194,r
      h=1.032059745956
      call cscalc(525.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',195,r
      h=1.109022114647
      call cscalc(525.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',196,r
      h=1.185984483338
      call cscalc(525.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',197,r
      h=1.262946852030
      call cscalc(525.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',198,r
      h=1.339909220721
      call cscalc(525.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',199,r
      h=1.416871589412
      call cscalc(525.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',200,r
      h=1.493833958104
      call cscalc(525.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',201,r
      h=1.570796326795
      call cscalc(525.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',202,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-42.733991000346
      cp(1,7)=48.037037037037
      cp(1,10)=-42.733991000346
      cp(1,13)=0.000000000000
      cp(1,16)=-42.733991000346
      cp(1,19)=48.037037037037
      cp(1,22)=-42.733991000346
      call csmcoe(1,1,1,0)
      icsash(1,1)=1
      h=-1.570796326795
      call cscalc(575.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',203,r
      h=-0.727042263940
      call cscalc(575.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',204,r
      cp=0.
      cp(2,1)=48.037037037037
      cp(2,4)=-42.733991000346
      cp(2,7)=58.851851851852
      cp(2,10)=-41.132139148494
      cp(2,13)=48.037037037037
      cp(2,16)=-42.733991000346
      cp(2,19)=58.851851851852
      cp(2,22)=-41.132139148494
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.727042263940
      call cscalc(575.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',205,r
      h=-0.609993947586
      call cscalc(575.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',206,r
      cp=0.
      cp(3,1)=58.851851851852
      cp(3,4)=-41.132139148494
      cp(3,7)=74.879629629630
      cp(3,10)=-7.252509518865
      cp(3,13)=78.398148148148
      cp(3,16)=-39.206213222568
      cp(3,19)=78.398148148148
      cp(3,22)=-39.206213222568
      call csmcoe(3,3,1,0)
      icsash(3,1)=3
      h=-0.609993947586
      call cscalc(575.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',207,r
      h=-0.558649992834
      call cscalc(575.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',208,r
      h=-0.507306038082
      call cscalc(575.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',209,r
      h=-0.455962083329
      call cscalc(575.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',210,r
      h=-0.404618128577
      call cscalc(575.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',211,r
      h=-0.353274173825
      call cscalc(575.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',212,r
      h=-0.301930219072
      call cscalc(575.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',213,r
      h=-0.250586264320
      call cscalc(575.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',214,r
      h=-0.199242309568
      call cscalc(575.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',215,r
      h=-0.147898354816
      call cscalc(575.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',216,r
      h=-0.096554400063
      call cscalc(575.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',217,r
      cp=0.
      cp(4,1)=74.879629629630
      cp(4,4)=-7.252509518865
      cp(4,7)=71.490740740741
      cp(4,10)=20.793786777432
      cp(4,13)=74.879629629630
      cp(4,16)=-7.252509518865
      cp(4,19)=71.490740740741
      cp(4,22)=20.793786777432
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=-0.096554400063
      call cscalc(575.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',218,r
      h=0.283050394185
      call cscalc(575.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',219,r
      cp=0.
      cp(5,1)=71.490740740741
      cp(5,4)=20.793786777432
      cp(5,7)=12.388888888889
      cp(5,10)=16.710453444098
      cp(5,13)=71.490740740741
      cp(5,16)=20.793786777432
      cp(5,19)=12.388888888889
      cp(5,22)=16.710453444098
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.283050394185
      call cscalc(575.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',220,r
      h=0.932831294404
      call cscalc(575.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',221,r
      cp=0.
      cp(6,1)=12.388888888889
      cp(6,4)=16.710453444098
      cp(6,7)=0.000000000000
      cp(6,10)=20.562305295950
      cp(6,13)=6.157407407407
      cp(6,16)=20.562305295950
      cp(6,19)=6.157407407407
      cp(6,22)=20.562305295950
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=0.932831294404
      call cscalc(575.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',222,r
      h=0.996627797644
      call cscalc(575.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',223,r
      h=1.060424300883
      call cscalc(575.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',224,r
      h=1.124220804122
      call cscalc(575.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',225,r
      h=1.188017307361
      call cscalc(575.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',226,r
      h=1.251813810600
      call cscalc(575.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',227,r
      h=1.315610313839
      call cscalc(575.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',228,r
      h=1.379406817078
      call cscalc(575.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',229,r
      h=1.443203320317
      call cscalc(575.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',230,r
      h=1.506999823556
      call cscalc(575.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',231,r
      h=1.570796326795
      call cscalc(575.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',232,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-43.137850467290
      cp(1,7)=49.000000000000
      cp(1,10)=-43.137850467290
      cp(1,13)=0.000000000000
      cp(1,16)=-43.137850467290
      cp(1,19)=49.000000000000
      cp(1,22)=-43.137850467290
      call csmcoe(1,1,1,0)
      icsash(1,1)=1
      h=-1.570796326795
      call cscalc(625.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',233,r
      h=-0.721860119936
      call cscalc(625.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',234,r
      cp=0.
      cp(2,1)=49.000000000000
      cp(2,4)=-43.137850467290
      cp(2,7)=57.250000000000
      cp(2,10)=-42.637850467290
      cp(2,13)=49.000000000000
      cp(2,16)=-43.137850467290
      cp(2,19)=57.250000000000
      cp(2,22)=-42.637850467290
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.721860119936
      call cscalc(625.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',235,r
      h=-0.640142890479
      call cscalc(625.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',236,r
      cp=0.
      cp(3,1)=57.250000000000
      cp(3,4)=-42.637850467290
      cp(3,7)=77.750000000000
      cp(3,10)=-6.887850467290
      cp(3,13)=80.250000000000
      cp(3,16)=-41.387850467290
      cp(3,19)=80.250000000000
      cp(3,22)=-41.387850467290
      call csmcoe(3,3,1,0)
      icsash(3,1)=3
      h=-0.640142890479
      call cscalc(625.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',237,r
      h=-0.584964506138
      call cscalc(625.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',238,r
      h=-0.529786121798
      call cscalc(625.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',239,r
      h=-0.474607737458
      call cscalc(625.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',240,r
      h=-0.419429353118
      call cscalc(625.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',241,r
      h=-0.364250968777
      call cscalc(625.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',242,r
      h=-0.309072584437
      call cscalc(625.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',243,r
      h=-0.253894200097
      call cscalc(625.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',244,r
      h=-0.198715815757
      call cscalc(625.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',245,r
      h=-0.143537431416
      call cscalc(625.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',246,r
      h=-0.088359047076
      call cscalc(625.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',247,r
      cp=0.
      cp(4,1)=77.750000000000
      cp(4,4)=-6.887850467290
      cp(4,7)=75.750000000000
      cp(4,10)=16.862149532710
      cp(4,13)=77.750000000000
      cp(4,16)=-6.887850467290
      cp(4,19)=75.750000000000
      cp(4,22)=16.862149532710
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=-0.088359047076
      call cscalc(625.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',248,r
      h=0.219031426795
      call cscalc(625.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',249,r
      cp=0.
      cp(5,1)=75.750000000000
      cp(5,4)=16.862149532710
      cp(5,7)=5.500000000000
      cp(5,10)=15.112149532710
      cp(5,13)=75.750000000000
      cp(5,16)=16.862149532710
      cp(5,19)=5.500000000000
      cp(5,22)=15.112149532710
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.219031426795
      call cscalc(625.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',250,r
      h=1.221752248395
      call cscalc(625.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',251,r
      cp=0.
      cp(6,1)=5.500000000000
      cp(6,4)=15.112149532710
      cp(6,7)=0.000000000000
      cp(6,10)=16.112149532710
      cp(6,13)=2.500000000000
      cp(6,16)=16.112149532710
      cp(6,19)=2.500000000000
      cp(6,22)=16.112149532710
      call csmcoe(6,3,1,0)
      icsash(6,1)=3
      h=1.221752248395
      call cscalc(625.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',252,r
      h=1.256656656235
      call cscalc(625.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',253,r
      h=1.291561064075
      call cscalc(625.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',254,r
      h=1.326465471915
      call cscalc(625.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',255,r
      h=1.361369879755
      call cscalc(625.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',256,r
      h=1.396274287595
      call cscalc(625.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',257,r
      h=1.431178695435
      call cscalc(625.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',258,r
      h=1.466083103275
      call cscalc(625.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',259,r
      h=1.500987511115
      call cscalc(625.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',260,r
      h=1.535891918955
      call cscalc(625.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',261,r
      h=1.570796326795
      call cscalc(625.00000000,1,6,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',262,r
      cp=0.
      cp(1,1)=0.000000000000
      cp(1,4)=-42.696261682243
      cp(1,7)=49.500000000000
      cp(1,10)=-42.696261682243
      cp(1,13)=0.000000000000
      cp(1,16)=-42.696261682243
      cp(1,19)=49.500000000000
      cp(1,22)=-42.696261682243
      call csmcoe(1,1,1,0)
      icsash(1,1)=1
      h=-1.570796326795
      call cscalc(650.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',263,r
      h=-0.711735439999
      call cscalc(650.00000000,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',264,r
      cp=0.
      cp(2,1)=49.500000000000
      cp(2,4)=-42.696261682243
      cp(2,7)=57.500000000000
      cp(2,10)=-42.696261682243
      cp(2,13)=49.500000000000
      cp(2,16)=-42.696261682243
      cp(2,19)=57.500000000000
      cp(2,22)=-42.696261682243
      call csmcoe(2,1,1,0)
      icsash(2,1)=1
      h=-0.711735439999
      call cscalc(650.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',265,r
      h=-0.638711960874
      call cscalc(650.00000000,1,2,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',266,r
      cp=0.
      cp(3,1)=57.500000000000
      cp(3,4)=-42.696261682243
      cp(3,7)=79.000000000000
      cp(3,10)=-6.696261682243
      cp(3,13)=81.500000000000
      cp(3,16)=-41.196261682243
      cp(3,19)=81.500000000000
      cp(3,22)=-41.196261682243
      call csmcoe(3,3,1,0)
      icsash(3,1)=3
      h=-0.638711960874
      call cscalc(650.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',267,r
      h=-0.583296832522
      call cscalc(650.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',268,r
      h=-0.527881704170
      call cscalc(650.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',269,r
      h=-0.472466575817
      call cscalc(650.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',270,r
      h=-0.417051447465
      call cscalc(650.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',271,r
      h=-0.361636319113
      call cscalc(650.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',272,r
      h=-0.306221190760
      call cscalc(650.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',273,r
      h=-0.250806062408
      call cscalc(650.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',274,r
      h=-0.195390934056
      call cscalc(650.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',275,r
      h=-0.139975805703
      call cscalc(650.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',276,r
      h=-0.084560677351
      call cscalc(650.00000000,1,3,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',277,r
      cp=0.
      cp(4,1)=79.000000000000
      cp(4,4)=-6.696261682243
      cp(4,7)=77.000000000000
      cp(4,10)=15.303738317757
      cp(4,13)=79.000000000000
      cp(4,16)=-6.696261682243
      cp(4,19)=77.000000000000
      cp(4,22)=15.303738317757
      call csmcoe(4,1,1,0)
      icsash(4,1)=1
      h=-0.084560677351
      call cscalc(650.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',278,r
      h=0.196193202407
      call cscalc(650.00000000,1,4,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',279,r
      cp=0.
      cp(5,1)=77.000000000000
      cp(5,4)=15.303738317757
      cp(5,7)=0.000000000000
      cp(5,10)=13.803738317757
      cp(5,13)=77.000000000000
      cp(5,16)=15.303738317757
      cp(5,19)=0.000000000000
      cp(5,22)=13.803738317757
      call csmcoe(5,1,1,0)
      icsash(5,1)=1
      h=0.196193202407
      call cscalc(650.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',280,r
      h=1.570796326795
      call cscalc(650.00000000,1,5,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',281,r
      end
