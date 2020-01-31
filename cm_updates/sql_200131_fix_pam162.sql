insert into parts (hpn, hpn_rev, hptype, manufacturer_number, start_gpstime) values ('PAM162', 'A', 'post-amp', 162, 1264500018);
update connections set upstream_part='PAM162' where upstream_part='PAM163' and downstream_input_port='e6';
update connections set upstream_part='PAM162' where upstream_part='PAM163' and downstream_input_port='n4';
update connections set upstream_part='PAM162' where upstream_part='PAM163' and downstream_input_port='@slot2';
update connections set downstream_part='PAM162' where downstream_part='PAM163' and upstream_output_port='e2';
update connections set downstream_part='PAM162' where downstream_part='PAM163' and upstream_output_port='n2';

