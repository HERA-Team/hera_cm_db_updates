insert into parts (hpn, hpn_rev, hptype, manufacturer_number, start_gpstime) values ('WR-unknown', 'A', 'white-rabbit', 'unknown', 1256554810);
update connections set upstream_part='WR-unknown' where upstream_part='WRA000087';
