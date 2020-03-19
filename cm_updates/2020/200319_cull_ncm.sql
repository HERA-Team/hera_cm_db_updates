update connections set upstream_part = 'NCM02' where upstream_part = 'NCMPro2';
update connections set upstream_part = 'NCMP2' where upstream_part = 'NCMPre2';
update connections set upstream_part = 'NCM03' where upstream_part = 'NCMPro3';
update connections set upstream_part = 'NCMP1' where upstream_part = 'NCMPre1'; 
update connections set upstream_part = 'NCM04' where upstream_part = 'NCMPro4'; 
update connections set upstream_part = 'NCM06' where upstream_part = 'NCMPro6'; 
update connections set upstream_part = 'NCM05' where upstream_part = 'NCMPro5'; 
update connections set upstream_part = 'NCM07' where upstream_part = 'NCMProd7'; 
update connections set upstream_part = 'NCM08' where upstream_part = 'NCMProd8'; 
update connections set upstream_part = 'NCM01' where upstream_part = 'NCMPro1'; 
update connections set upstream_part = 'NCM10' where upstream_part = 'NCMProd10'; 
update connections set upstream_part = 'NCM09' where upstream_part = 'NCMProd9'; 
update parts set manufacturer_number = 'NCM-Pro13' where manufacturer_number = 'NCM13';
update parts set manufacturer_number = 'NCM-Pro14' where manufacturer_number = 'NCM14';
delete from parts where hpn like 'NCMPr%';
  
