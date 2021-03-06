update connections set upstream_part='WRA000087' where upstream_part='WR-unknown';
update part_rosetta set hpn='WRA000087' where hpn='WR-unknown';
update part_info set comment='MAC - 08:00:30:b2:2e:08' where hpn='WRA000087';
update part_info set hpn='WRA000087' where hpn='WR-unknown';
delete from parts where hpn='WR-unknown';
insert into parts (hpn,hpn_rev,hptype,manufacturer_number,start_gpstime) values ('WRA000201','A','white-rabbit','S6.108','126709228');
insert into part_info (hpn,hpn_rev,comment,posting_gpstime) values ('WRA000201','A','MAC - 08:00:30:12:7c:a1','126709228');
insert into part_info (hpn,hpn_rev,comment,posting_gpstime) values ('WRA000201','A','IP - 10.80.2.136','126709238');
insert into part_rosetta (hpn,syspn,start_gpstime) values ('WRA000201','heraNode2wr','126709238');
insert into part_rosetta (hpn,syspn,start_gpstime) values ('RD13','heraNode2','126709248');
insert into connections (upstream_part,up_part_rev,downstream_part,down_part_rev,upstream_output_port,downstream_input_port,start_gpstime) values ('WRA000201','A','NCM14','A','mnt','mnt1','1267095618');
