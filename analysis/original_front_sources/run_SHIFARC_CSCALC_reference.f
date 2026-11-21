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
       cp(1,1)=24.103886347707
       cp(1,4)=1.038444567016
       cp(1,7)=4.843750000000
       cp(1,10)=32.352220077220
       cp(1,13)=24.103886347707
       cp(1,16)=28.914720077220
       cp(1,19)=24.103886347707
       cp(1,22)=28.914720077220
       call csmcoe(1,3,1,0)
       icsash(1,1)=3
       h=0.043055414138
       call cscalc(210.,1,1,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',1,0,r
       h=0.229960770656
       call cscalc(210.,1,1,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',1,10,r
       h=0.408740546448
       call cscalc(210.,1,1,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',1,20,r
       h=0.575381760534
       call cscalc(210.,1,1,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',1,30,r
       h=0.728192286844
       call cscalc(210.,1,1,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',1,40,r
       h=0.867395329753
       call cscalc(210.,1,1,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',1,50,r
       h=0.994414356136
       call cscalc(210.,1,1,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',1,60,r
       h=1.111247187496
       call cscalc(210.,1,1,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',1,70,r
       h=1.220066125711
       call cscalc(210.,1,1,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',1,80,r
       h=1.323021393774
       call cscalc(210.,1,1,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',1,90,r
       h=1.422180966418
       call cscalc(210.,1,1,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',1,100,r
       cp=0.
       cp(2,1)=4.843750000000
       cp(2,4)=32.352220077220
       cp(2,7)=0.000000000000
       cp(2,10)=35.845275632776
       cp(2,13)=3.906250000000
       cp(2,16)=35.845275632776
       cp(2,19)=3.906250000000
       cp(2,22)=35.845275632776
       call csmcoe(2,3,1,0)
       icsash(2,1)=3
       h=1.422180966418
       call cscalc(210.,1,2,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',2,0,r
       h=1.430754251600
       call cscalc(210.,1,2,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',2,10,r
       h=1.441336045008
       call cscalc(210.,1,2,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',2,20,r
       h=1.453694000170
       call cscalc(210.,1,2,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',2,30,r
       h=1.467595998958
       call cscalc(210.,1,2,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',2,40,r
       h=1.482812189778
       call cscalc(210.,1,2,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',2,50,r
       h=1.499116026989
       call cscalc(210.,1,2,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',2,60,r
       h=1.516284576386
       call cscalc(210.,1,2,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',2,70,r
       h=1.534098296664
       call cscalc(210.,1,2,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',2,80,r
       h=1.552340458799
       call cscalc(210.,1,2,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',2,90,r
       h=1.570796326795
       call cscalc(210.,1,2,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',2,100,r
       cp=0.
       cp(3,1)=25.104592266788
       cp(3,4)=1.599117484832
       cp(3,7)=14.531250000000
       cp(3,10)=30.540444015444
       cp(3,13)=25.104592266788
       cp(3,16)=20.227944015444
       cp(3,19)=25.104592266788
       cp(3,22)=20.227944015444
       call csmcoe(3,3,1,0)
       icsash(3,1)=3
       h=0.063612263926
       call cscalc(220.,1,3,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',3,0,r
       h=0.197999062203
       call cscalc(220.,1,3,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',3,10,r
       h=0.328288654338
       call cscalc(220.,1,3,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',3,20,r
       h=0.452659713488
       call cscalc(220.,1,3,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',3,30,r
       h=0.569962345881
       call cscalc(220.,1,3,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',3,40,r
       h=0.679701603877
       call cscalc(220.,1,3,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',3,50,r
       h=0.781917452289
       call cscalc(220.,1,3,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',3,60,r
       h=0.877027143583
       call cscalc(220.,1,3,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',3,70,r
       h=0.965677934504
       call cscalc(220.,1,3,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',3,80,r
       h=1.048632746656
       call cscalc(220.,1,3,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',3,90,r
       h=1.126692614784
       call cscalc(220.,1,3,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',3,100,r
       cp=0.
       cp(4,1)=14.531250000000
       cp(4,4)=30.540444015444
       cp(4,7)=0.000000000000
       cp(4,10)=41.019610682111
       cp(4,13)=11.718750000000
       cp(4,16)=41.019610682111
       cp(4,19)=11.718750000000
       cp(4,22)=41.019610682111
       call csmcoe(4,3,1,0)
       icsash(4,1)=3
       h=1.126692614784
       call cscalc(220.,1,4,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',4,0,r
       h=1.163518050762
       call cscalc(220.,1,4,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',4,10,r
       h=1.202989776948
       call cscalc(220.,1,4,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',4,20,r
       h=1.244658244938
       call cscalc(220.,1,4,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',4,30,r
       h=1.288142667845
       call cscalc(220.,1,4,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',4,40,r
       h=1.333112986379
       call cscalc(220.,1,4,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',4,50,r
       h=1.379276365113
       call cscalc(220.,1,4,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',4,60,r
       h=1.426366983057
       call cscalc(220.,1,4,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',4,70,r
       h=1.474138209004
       call cscalc(220.,1,4,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',4,80,r
       h=1.522356476816
       call cscalc(220.,1,4,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',4,90,r
       h=1.570796326795
       call cscalc(220.,1,4,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',4,100,r
       cp=0.
       cp(5,1)=27.570030222164
       cp(5,4)=3.281136238279
       cp(5,7)=15.733870967742
       cp(5,10)=33.407535184955
       cp(5,13)=27.570030222164
       cp(5,16)=21.050726517139
       cp(5,19)=27.570030222164
       cp(5,22)=21.050726517139
       call csmcoe(5,3,1,0)
       icsash(5,1)=3
       h=0.118453829203
       call cscalc(250.,1,5,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',5,0,r
       h=0.237340014687
       call cscalc(250.,1,5,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',5,10,r
       h=0.353040259257
       call cscalc(250.,1,5,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',5,20,r
       h=0.464942783541
       call cscalc(250.,1,5,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',5,30,r
       h=0.572657436559
       call cscalc(250.,1,5,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',5,40,r
       h=0.675999662209
       call cscalc(250.,1,5,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',5,50,r
       h=0.774958163166
       call cscalc(250.,1,5,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',5,60,r
       h=0.869655719834
       call cscalc(250.,1,5,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',5,70,r
       h=0.960310425598
       call cscalc(250.,1,5,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',5,80,r
       h=1.047201720519
       call cscalc(250.,1,5,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',5,90,r
       h=1.130643099333
       call cscalc(250.,1,5,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',5,100,r
       cp=0.
       cp(6,1)=15.733870967742
       cp(6,4)=33.407535184955
       cp(6,7)=0.000000000000
       cp(6,10)=54.217615830116
       cp(6,13)=14.137096774194
       cp(6,16)=54.217615830116
       cp(6,19)=14.137096774194
       cp(6,22)=54.217615830116
       call csmcoe(6,3,1,0)
       icsash(6,1)=3
       h=1.130643099333
       call cscalc(250.,1,6,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',6,0,r
       h=1.176272465739
       call cscalc(250.,1,6,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',6,10,r
       h=1.221754344483
       call cscalc(250.,1,6,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',6,20,r
       h=1.266867832204
       call cscalc(250.,1,6,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',6,30,r
       h=1.311507939381
       call cscalc(250.,1,6,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',6,40,r
       h=1.355648079584
       call cscalc(250.,1,6,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',6,50,r
       h=1.399314712828
       call cscalc(250.,1,6,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',6,60,r
       h=1.442570003896
       call cscalc(250.,1,6,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',6,70,r
       h=1.485499812778
       call cscalc(250.,1,6,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',6,80,r
       h=1.528205218916
       call cscalc(250.,1,6,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',6,90,r
       h=1.570796326795
       call cscalc(250.,1,6,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',6,100,r
       cp=0.
       cp(7,1)=30.131674227373
       cp(7,4)=6.084500827358
       cp(7,7)=16.188888888889
       cp(7,10)=37.432346632347
       cp(7,13)=30.131674227373
       cp(7,16)=23.967037047953
       cp(7,19)=30.131674227373
       cp(7,22)=23.967037047953
       call csmcoe(7,3,1,0)
       icsash(7,1)=3
       h=0.199251016318
       call cscalc(300.,1,7,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',7,0,r
       h=0.306899863955
       call cscalc(300.,1,7,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',7,10,r
       h=0.411716512436
       call cscalc(300.,1,7,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',7,20,r
       h=0.513828288072
       call cscalc(300.,1,7,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',7,30,r
       h=0.613372105553
       call cscalc(300.,1,7,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',7,40,r
       h=0.710478246163
       call cscalc(300.,1,7,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',7,50,r
       h=0.805259953169
       call cscalc(300.,1,7,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',7,60,r
       h=0.897807929714
       call cscalc(300.,1,7,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',7,70,r
       h=0.988188721977
       call cscalc(300.,1,7,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',7,80,r
       h=1.076445998866
       call cscalc(300.,1,7,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',7,90,r
       h=1.162603827696
       call cscalc(300.,1,7,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',7,100,r
       cp=0.
       cp(8,1)=16.188888888889
       cp(8,4)=37.432346632347
       cp(8,7)=0.000000000000
       cp(8,10)=59.578890286535
       cp(8,13)=16.188888888889
       cp(8,16)=59.578890286535
       cp(8,19)=16.188888888889
       cp(8,22)=59.578890286535
       call csmcoe(8,3,1,0)
       icsash(8,1)=3
       h=1.162603827696
       call cscalc(300.,1,8,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',8,0,r
       h=1.198095546494
       call cscalc(300.,1,8,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',8,10,r
       h=1.236136080052
       call cscalc(300.,1,8,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',8,20,r
       h=1.275896354082
       call cscalc(300.,1,8,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',8,30,r
       h=1.316796868127
       call cscalc(300.,1,8,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',8,40,r
       h=1.358436499016
       call cscalc(300.,1,8,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',8,50,r
       h=1.400541702604
       call cscalc(300.,1,8,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',8,60,r
       h=1.442929710018
       call cscalc(300.,1,8,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',8,70,r
       h=1.485481313540
       call cscalc(300.,1,8,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',8,80,r
       h=1.528120160043
       call cscalc(300.,1,8,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',8,90,r
       h=1.570796326795
       call cscalc(300.,1,8,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',8,100,r
       cp=0.
       cp(9,1)=30.954139736749
       cp(9,4)=8.327192498621
       cp(9,7)=16.250000000000
       cp(9,10)=37.924131274131
       cp(9,13)=30.954139736749
       cp(9,16)=26.300085472605
       cp(9,19)=30.954139736749
       cp(9,22)=26.300085472605
       call csmcoe(9,3,1,0)
       icsash(9,1)=3
       h=0.262795480617
       call cscalc(340.,1,9,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',9,0,r
       h=0.362754358546
       call cscalc(340.,1,9,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',9,10,r
       h=0.459985695077
       call cscalc(340.,1,9,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',9,20,r
       h=0.554748665141
       call cscalc(340.,1,9,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',9,30,r
       h=0.647284580004
       call cscalc(340.,1,9,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',9,40,r
       h=0.737810596517
       call cscalc(340.,1,9,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',9,50,r
       h=0.826516580114
       call cscalc(340.,1,9,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',9,60,r
       h=0.913564253257
       call cscalc(340.,1,9,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',9,70,r
       h=0.999087955510
       call cscalc(340.,1,9,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',9,80,r
       h=1.083196508459
       call cscalc(340.,1,9,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',9,90,r
       h=1.165975808728
       call cscalc(340.,1,9,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',9,100,r
       cp=0.
       cp(10,1)=16.250000000000
       cp(10,4)=37.924131274131
       cp(10,7)=0.000000000000
       cp(10,10)=55.929309378216
       cp(10,13)=16.250000000000
       cp(10,16)=55.929309378216
       cp(10,19)=16.250000000000
       cp(10,22)=55.929309378216
       call csmcoe(10,3,1,0)
       icsash(10,1)=3
       h=1.165975808728
       call cscalc(340.,1,10,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',10,0,r
       h=1.195513932961
       call cscalc(340.,1,10,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',10,10,r
       h=1.229338949488
       call cscalc(340.,1,10,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',10,20,r
       h=1.266466782642
       call cscalc(340.,1,10,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',10,30,r
       h=1.306132598827
       call cscalc(340.,1,10,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',10,40,r
       h=1.347736065644
       call cscalc(340.,1,10,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',10,50,r
       h=1.390799723624
       call cscalc(340.,1,10,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',10,60,r
       h=1.434937030751
       call cscalc(340.,1,10,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',10,70,r
       h=1.479827350414
       call cscalc(340.,1,10,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',10,80,r
       h=1.525195794942
       call cscalc(340.,1,10,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',10,90,r
       h=1.570796326795
       call cscalc(340.,1,10,h,r,rx,rh,rxx,rxh,0)
       write(*,*) 'RADIUS',10,100,r
      end
