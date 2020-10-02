update connections set upstream_part='RD41' where upstream_part='RD42' and downstream_part='NCM04';
update connections set upstream_part='RD42' where upstream_part='RD41' and downstream_part='NCM03';
update connections set upstream_part='NCM03' where upstream_part='NCM04' and downstream_part='N05';
update connections set upstream_part='NCM04' where upstream_part='NCM03' and downstream_part='N04';
