// F-14 RC v75 joint clearance coupon - P2S / 0.4 mm nozzle
// Measures real sliding/adhesive fit at 0.10, 0.15, 0.20, 0.25 mm per-side clearance.
$fn=48;
clearances=[0.10,0.15,0.20,0.25];
peg_w=8; peg_h=5; peg_len=18; wall=3; base=2.4; pitch=18;

module label_bar(x,c){
    translate([x-6,-9,0]) cube([12,3,base]);
    // physical notch code: 1..4 notches identifies clearance without relying on embossed text
    for(n=[0:round(c*20)-2]) translate([x-5+n*1.6,-9,base]) cube([0.8,2,0.8]);
}
module socket(x,c){
    difference(){
        translate([x-(peg_w+2*wall)/2,0,0]) cube([peg_w+2*wall,peg_len+wall,peg_h+base+wall]);
        translate([x-peg_w/2-c,wall,base]) cube([peg_w+2*c,peg_len+0.2,peg_h+2*c]);
    }
    label_bar(x,c);
}
module peg(x,c){
    translate([x-peg_w/2,27,base]) cube([peg_w,peg_len,peg_h]);
    translate([x-peg_w/2-1,25,0]) cube([peg_w+2,2,base+peg_h]);
    label_bar(x+0.01,c);
}
for(i=[0:3]){
    x=i*pitch;
    socket(x,clearances[i]);
    peg(x,clearances[i]);
}
// 6 mm carbon-like rod gauge with radial holes for 0.10..0.25 mm clearance
for(i=[0:3]){
    x=i*pitch;
    translate([x,-20,0]) difference(){
        cylinder(h=8,r=5);
        translate([0,0,-0.1]) cylinder(h=8.2,r=3+clearances[i]);
    }
}