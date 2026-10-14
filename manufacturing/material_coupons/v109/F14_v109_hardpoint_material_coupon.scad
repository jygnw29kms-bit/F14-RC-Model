// F-14 v109 representative hardpoint material coupon
// Local front-socket geometry: 12x12 mm socket, 6.4 mm bore over 24 mm,
// 8 mm solid tail, bonded/monolithic into a 2 mm fork-style base tab.
$fn=96;
socket_w=12;
socket_h=12;
socket_len=24;
tail_len=8;
bore_d=6.4;
bore_z=8;           // v99 front socket bore center from bottom
fork_t=2;
fork_w=24;
fork_len=44;

module socket_body(){
    difference(){
        cube([socket_w,socket_len+tail_len,socket_h]);
        // Bore only through the original 24 mm socket zone; tail remains solid.
        translate([socket_w/2,-0.1,bore_z])
            rotate([-90,0,0]) cylinder(h=socket_len+0.2,d=bore_d);
    }
}

module fork_tab(){
    translate([-(fork_w-socket_w)/2,20,0]) cube([fork_w,fork_len,fork_t]);
}

union(){
    socket_body();
    fork_tab();
}