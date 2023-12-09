delete from connections where upstream_part='NBP22' and upstream_output_port='E9' and downstream_part='PAM010';
delete from connections where upstream_part='NBP22' and upstream_output_port='N9' and downstream_part='PAM010';
delete from connections where upstream_part='NBP22' and upstream_output_port='E12' and downstream_part='PAM019';
delete from connections where upstream_part='NBP22' and upstream_output_port='N12' and downstream_part='PAM019';
delete from connections where upstream_part='NBP19' and upstream_output_port='E1' and downstream_part='PAM013';
delete from connections where upstream_part='NBP19' and upstream_output_port='N1' and downstream_part='PAM013';
delete from connections where upstream_part='NBP20' and upstream_output_port='E8' and downstream_part='PAM016';
delete from connections where upstream_part='NBP20' and upstream_output_port='N8' and downstream_part='PAM016';

update connections set stop_gpstime = null where upstream_part='NBP22' and upstream_output_port='e9' and downstream_part='PAM010';
update connections set stop_gpstime = null where upstream_part='NBP22' and upstream_output_port='n9' and downstream_part='PAM010';
update connections set stop_gpstime = null where upstream_part='NBP22' and upstream_output_port='e12' and downstream_part='PAM019';
update connections set stop_gpstime = null where upstream_part='NBP22' and upstream_output_port='n12' and downstream_part='PAM019';
update connections set stop_gpstime = null where upstream_part='NBP19' and upstream_output_port='e1' and downstream_part='PAM013';
update connections set stop_gpstime = null where upstream_part='NBP19' and upstream_output_port='n1' and downstream_part='PAM013';
update connections set stop_gpstime = null where upstream_part='NBP20' and upstream_output_port='e8' and downstream_part='PAM016';
update connections set stop_gpstime = null where upstream_part='NBP20' and upstream_output_port='n8' and downstream_part='PAM016';