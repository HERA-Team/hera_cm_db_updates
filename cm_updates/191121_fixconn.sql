delete from connections where upstream_part='FEM010' and downstream_part='NBP00';
delete from connections where upstream_part='FDV1' and downstream_part='FEM010';
delete from connections where upstream_part='PAM010' and downstream_part='PCH1';
delete from parts where hpn='FEM010';

delete from connections where upstream_part='FEM011' and downstream_part='NBP00';
delete from connections where upstream_part='FDV2' and downstream_part='FEM011';
delete from connections where upstream_part='PAM011' and downstream_part='PCH1';
delete from parts where hpn='FEM011';

delete from connections where upstream_part='FEM012' and downstream_part='NBP00';
delete from connections where upstream_part='FDV3' and downstream_part='FEM012';
delete from connections where upstream_part='PAM012' and downstream_part='PCH1';
delete from parts where hpn='FEM012';

delete from connections where upstream_part='FEM013' and downstream_part='NBP00';
delete from connections where upstream_part='FDV4' and downstream_part='FEM013';
delete from connections where upstream_part='PAM013' and downstream_part='PCH1';
delete from connections where upstream_part='PAM013' and downstream_part='SNPA000022';
update connections set stop_gpstime=1256644818 where upstream_part='FEM013' and stop_gpstime=1256817618;
update connections set start_gpstime=1256644818 where upstream_part='FEM013' and downstream_part='NBP07' and downstream_input_port='n5';

delete from connections where upstream_part='FEM014' and downstream_part='NBP00';
delete from connections where upstream_part='FDV6' and downstream_part='FEM014';
delete from connections where upstream_part='PAM014' and downstream_part='PCH1';
delete from connections where upstream_part='PAM014' and downstream_part='SNPA000022';

delete from connections where upstream_part='FEM015' and downstream_part='NBP00';
delete from connections where upstream_part='FDV7' and downstream_part='FEM015';
delete from connections where upstream_part='PAM015' and downstream_part='PCH1';

update connections set start_gpstime=1242039618 where upstream_part='FEM028' and downstream_part='FPS02';

update connections set start_gpstime=1242039618 where upstream_part='FEM032' and downstream_part='FPS02';

update connections set start_gpstime=1242039618 where upstream_part='FEM044' and downstream_part='FPS02';

update connections set start_gpstime=1242039618 where upstream_part='PAM042' and downstream_part='PCH02' and downstream_input_port='@slot08';

update connections set start_gpstime=1242039618 where upstream_part='PAM043' and downstream_part='PCH02';

update connections set start_gpstime=1242039618 where upstream_part='PAM045' and downstream_part='PCH02';

update connections set stop_gpstime=1256644817 where upstream_part='FEM047' and downstream_part='NBP07';

