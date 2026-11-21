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
      cp(1,1)=12.388888888889
      cp(1,4)=16.710453444098
      cp(1,7)=0.000000000000
      cp(1,10)=20.562305295950
      cp(1,13)=6.157407407407
      cp(1,16)=20.562305295950
      cp(1,19)=6.157407407407
      cp(1,22)=20.562305295950
      call csmcoe(1,3,1,0)
      icsash(1,1)=3
      h=0.932831294404
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',0,r
      h=0.939210944728
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',1,r
      h=0.945590595052
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',2,r
      h=0.951970245376
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',3,r
      h=0.958349895700
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',4,r
      h=0.964729546024
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',5,r
      h=0.971109196348
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',6,r
      h=0.977488846672
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',7,r
      h=0.983868496996
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',8,r
      h=0.990248147320
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',9,r
      h=0.996627797644
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',10,r
      h=1.003007447967
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',11,r
      h=1.009387098291
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',12,r
      h=1.015766748615
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',13,r
      h=1.022146398939
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',14,r
      h=1.028526049263
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',15,r
      h=1.034905699587
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',16,r
      h=1.041285349911
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',17,r
      h=1.047665000235
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',18,r
      h=1.054044650559
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',19,r
      h=1.060424300883
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',20,r
      h=1.066803951206
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',21,r
      h=1.073183601530
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',22,r
      h=1.079563251854
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',23,r
      h=1.085942902178
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',24,r
      h=1.092322552502
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',25,r
      h=1.098702202826
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',26,r
      h=1.105081853150
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',27,r
      h=1.111461503474
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',28,r
      h=1.117841153798
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',29,r
      h=1.124220804122
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',30,r
      h=1.130600454446
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',31,r
      h=1.136980104769
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',32,r
      h=1.143359755093
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',33,r
      h=1.149739405417
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',34,r
      h=1.156119055741
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',35,r
      h=1.162498706065
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',36,r
      h=1.168878356389
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',37,r
      h=1.175258006713
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',38,r
      h=1.181637657037
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',39,r
      h=1.188017307361
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',40,r
      h=1.194396957685
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',41,r
      h=1.200776608008
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',42,r
      h=1.207156258332
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',43,r
      h=1.213535908656
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',44,r
      h=1.219915558980
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',45,r
      h=1.226295209304
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',46,r
      h=1.232674859628
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',47,r
      h=1.239054509952
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',48,r
      h=1.245434160276
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',49,r
      h=1.251813810600
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',50,r
      h=1.258193460924
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',51,r
      h=1.264573111247
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',52,r
      h=1.270952761571
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',53,r
      h=1.277332411895
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',54,r
      h=1.283712062219
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',55,r
      h=1.290091712543
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',56,r
      h=1.296471362867
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',57,r
      h=1.302851013191
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',58,r
      h=1.309230663515
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',59,r
      h=1.315610313839
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',60,r
      h=1.321989964163
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',61,r
      h=1.328369614487
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',62,r
      h=1.334749264810
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',63,r
      h=1.341128915134
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',64,r
      h=1.347508565458
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',65,r
      h=1.353888215782
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',66,r
      h=1.360267866106
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',67,r
      h=1.366647516430
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',68,r
      h=1.373027166754
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',69,r
      h=1.379406817078
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',70,r
      h=1.385786467402
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',71,r
      h=1.392166117726
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',72,r
      h=1.398545768049
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',73,r
      h=1.404925418373
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',74,r
      h=1.411305068697
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',75,r
      h=1.417684719021
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',76,r
      h=1.424064369345
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',77,r
      h=1.430444019669
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',78,r
      h=1.436823669993
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',79,r
      h=1.443203320317
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',80,r
      h=1.449582970641
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',81,r
      h=1.455962620965
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',82,r
      h=1.462342271289
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',83,r
      h=1.468721921612
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',84,r
      h=1.475101571936
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',85,r
      h=1.481481222260
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',86,r
      h=1.487860872584
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',87,r
      h=1.494240522908
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',88,r
      h=1.500620173232
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',89,r
      h=1.506999823556
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',90,r
      h=1.513379473880
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',91,r
      h=1.519759124204
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',92,r
      h=1.526138774528
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',93,r
      h=1.532518424851
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',94,r
      h=1.538898075175
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',95,r
      h=1.545277725499
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',96,r
      h=1.551657375823
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',97,r
      h=1.558037026147
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',98,r
      h=1.564416676471
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',99,r
      h=1.570796326795
      call cscalc(575.,1,1,h,r,rx,rh,rxx,rxh,0)
      write(*,*) 'CHECK',100,r
      end
