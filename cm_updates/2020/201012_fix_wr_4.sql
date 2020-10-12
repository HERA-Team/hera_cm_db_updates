insert into parts (hpn, hpn_rev, hptype, manufacturer_number, start_gpstime) values ('WR-len4p0', 'A', 'white-rabbit', 'S8.313', 1267092018);
update connections set upstream_part='WR-len4p0' where upstream_part='WRlen4p0';
delete from parts where hpn='WRlen4p0';
