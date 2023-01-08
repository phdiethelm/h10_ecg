#!/bin/bash
# from https://nob.ro/post/polar_h10_ubuntu/
gatttool -t random -b EC:EA:02:85:D9:7A --char-write-req --handle=0x0011 --value=0100 --listen | perl -ne 'if(/.*value: (\w+) (\w+) (\w+) (\w+)/) { ($x,$y,$z,$a) = ($1,$2,$3, $4);$rr = hex("$a$z"); printf ("%d, %f, %x, %x, %d\n", hex($y), $rr/1024, $a, $z, $rr);}'
