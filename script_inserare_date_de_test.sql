--- Clienti & Conturi
INSERT INTO clienti VALUES (null, 'Iasi, Soseaua Sararie, Bloc B5, Ap.10', '+40712345678', 'unEmail@gmail.com');
INSERT INTO conturi VALUES ('myUsername','76549b827ec46e705fd03831813fa52172338f0dfcbd711ed44b81a96dac51c6',SYSDATE,DEFAULT,NULL,clienti_id_client_seq.CURRVAL);
--- myUsername:myPassword

INSERT INTO clienti VALUES (null, 'Iasi, Strada Petru Poni, Bloc C12, Ap.7', '0715123412', 'altEmail@gmail.com');
INSERT INTO conturi VALUES ('iasiUsername','90007d74505ab48c9bf2a05dde9c538cc5224e13cd718f192434b049ed7a20c4',SYSDATE,DEFAULT,NULL,clienti_id_client_seq.CURRVAL);
--- iasiUsername:iasiPassword

INSERT INTO clienti VALUES (null, 'Bucuresti, Bulevardul Mircea Voda, Bloc A10, Ap.31', '+40712515278', 'emailBucuresti@yahoo.com');
INSERT INTO conturi VALUES ('myBucharestUsername','dd922d2d2da36f9c4e4871ed277fe18a0d5b26c3baf85b9104bbc8eacc7193bd',SYSDATE,DEFAULT,NULL,clienti_id_client_seq.CURRVAL);
-- myBucharestUsername:myBucharestPassword

INSERT INTO clienti VALUES (null, 'Brasov, Strada Zizinului, Bloc B2, Ap.15', '0756123456','superEmail@gmail.com');
INSERT INTO conturi VALUES ('brasovBrasov','320189d38a765866ecd6f99b33a32400c4af0d2ae15777e11c686768b1361d29',SYSDATE,DEFAULT,NULL,clienti_id_client_seq.CURRVAL);
-- brasovBrasov:Brasovbrasov

INSERT INTO clienti VALUES (null, 'Oradea, Strada Tudor Vladimirescu, Bloc C5, Ap.17', '+40713247678','emailTemporar@gmail.com');
INSERT INTO conturi VALUES ('OradeaMan','a09927702ccc43bac96d2ddbcb8db36fced14b6dfddd744958dd8fea0597fae9',SYSDATE,DEFAULT,NULL,clienti_id_client_seq.CURRVAL);
-- OradeaMan:naMaedarO

INSERT INTO clienti VALUES (null, 'Default Billing Address', '+4071234567890','admin@gmail.com');
INSERT INTO conturi VALUES ('admin','713bfda78870bf9d1b261f565286f85e97ee614efe5f0faf7c34e7ca4f65baca',SYSDATE,DEFAULT,NULL,clienti_id_client_seq.CURRVAL);
--admin:adminpass

--- Promotii
INSERT INTO promotii VALUES (null,0,SYSDATE,NULL,'Promotia implicita pentru un produs (0%)');
INSERT INTO promotii VALUES (null,20,SYSDATE,ADD_MONTHS(SYSDATE,1),'Promotie de 20% la camere foto');
INSERT INTO promotii VALUES (null,50,SYSDATE,ADD_MONTHS(SYSDATE,4),'Promotia de 50% la software Microsoft');
INSERT INTO promotii VALUES (null,25,SYSDATE,ADD_MONTHS(SYSDATE,2),'Promotie temporara');
INSERT INTO promotii VALUES (null,5,SYSDATE,ADD_MONTHS(SYSDATE,1),'Promotie temporara');

--- Produse
INSERT INTO produse VALUES (null,'IPhone 20 Pro Max',5000,'Apple',3,'Telefoane',DEFAULT,'Cel mai nou produs marca Apple cu un procesor de 1nm si 10Ghz',
    (SELECT id_promotie FROM promotii WHERE procent_reducere = 0 AND data_inceput = SYSDATE and data_sfarsit IS NULL));
INSERT INTO produse VALUES (null,'TV Samsung 50',8000,'Samsung',1,'TV',3,'TV 8K cu diagonala de 120 Inch',
    (SELECT id_promotie FROM promotii WHERE procent_reducere = 0 AND data_inceput = SYSDATE and data_sfarsit IS NULL));
INSERT INTO produse VALUES (null,'Mouse Gaming Wireless RGB x2000',300,'Logitech',12,'Periferice',DEFAULT,NULL,
    (SELECT id_promotie FROM promotii WHERE procent_reducere = 0 AND data_inceput = SYSDATE and data_sfarsit IS NULL));
INSERT INTO produse VALUES (null,'Tastatura Gaming Wireless RGB x1234',500,'Logitech',12,'Periferice',DEFAULT,NULL,
   (SELECT id_promotie FROM promotii WHERE procent_reducere = 0 AND data_inceput = SYSDATE and data_sfarsit IS NULL));
INSERT INTO produse VALUES (null,'Camera Bord A800',500,'Xiaomi',2,'Auto',2,'Rezolutie 2K',
    (SELECT id_promotie FROM promotii WHERE procent_reducere = 0 AND data_inceput = SYSDATE and data_sfarsit IS NULL));
INSERT INTO produse VALUES (null,'Camera Foto Canon 90D',2500,'Canon',5,'Foto',DEFAULT,'Rezolutie Foto 4K, include obiectiv de 80mm. Permite filmari 2K',
    (SELECT id_promotie FROM promotii WHERE procent_reducere = 20 AND data_inceput = SYSDATE and data_sfarsit = ADD_MONTHS(SYSDATE,1)));
INSERT INTO produse VALUES (null,'Windows 11 Pro',200,'Microsoft',10,'Software',24,'Include un cod de activare',
    (SELECT id_promotie FROM promotii WHERE procent_reducere = 50 AND data_inceput = SYSDATE and data_sfarsit = ADD_MONTHS(SYSDATE,4)));

--- Wishlists
INSERT INTO wishlists VALUES (null,'myWishlist',SYSDATE,DEFAULT,
    (SELECT id_client FROM clienti WHERE email = 'unEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'Camera Bord A800' AND producator = 'Xiaomi'));
INSERT INTO wishlists VALUES (null,'myWishlist',SYSDATE,DEFAULT,
    (SELECT id_client FROM clienti WHERE email = 'unEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'IPhone 20 Pro Max' AND producator = 'Apple'));
INSERT INTO wishlists VALUES (null,'myWishlist nr2',SYSDATE,'Nelistat',
    (SELECT id_client FROM clienti WHERE email = 'unEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'IPhone 20 Pro Max' AND producator = 'Apple'));
INSERT INTO wishlists VALUES (null,'myWishlist nr2',SYSDATE,'Nelistat',
    (SELECT id_client FROM clienti WHERE email = 'unEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'Mouse Gaming Wireless RGB x2000' AND producator = 'Logitech'));
INSERT INTO wishlists VALUES (null,'bucharest Wishlist',SYSDATE,'Nelistat',
    (SELECT id_client FROM clienti WHERE email = 'emailBucuresti@yahoo.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'TV Samsung 50' AND producator = 'Samsung'));
INSERT INTO wishlists VALUES (null,'someOtherWishlist',SYSDATE,'Public',
    (SELECT id_client FROM clienti WHERE email = 'superEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'Tastatura Gaming Wireless RGB x1234' AND producator = 'Logitech'));
INSERT INTO wishlists VALUES (null,'someOtherWishlist',SYSDATE,'Public',
    (SELECT id_client FROM clienti WHERE email = 'superEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'Camera Bord A800' AND producator = 'Xiaomi'));

--- Cosuri
INSERT INTO cosuri VALUES (null,3,
    (SELECT id_client FROM clienti WHERE email = 'unEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'Windows 11 Pro' AND producator = 'Microsoft'));
INSERT INTO cosuri VALUES (null,1,
    (SELECT id_client FROM clienti WHERE email = 'unEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'IPhone 20 Pro Max' AND producator = 'Apple'));
INSERT INTO cosuri VALUES (null,1,
    (SELECT id_client FROM clienti WHERE email = 'altEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'Mouse Gaming Wireless RGB x2000' AND producator = 'Logitech'));
INSERT INTO cosuri VALUES (null,1,
    (SELECT id_client FROM clienti WHERE email = 'emailBucuresti@yahoo.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'Camera Foto Canon 90D' AND producator = 'Canon'));

--- Comenzi
INSERT INTO comenzi VALUES (null,SYSDATE,null,DEFAULT,
    (SELECT id_client FROM clienti WHERE email = 'unEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'Windows 11 Pro' AND producator = 'Microsoft'),2);
INSERT INTO comenzi VALUES (null,SYSDATE,null,DEFAULT,
    (SELECT id_client FROM clienti WHERE email = 'unEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'IPhone 20 Pro Max' AND producator = 'Apple'),1);
INSERT INTO comenzi VALUES (null,SYSDATE,null,DEFAULT,
    (SELECT id_client FROM clienti WHERE email = 'altEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'Mouse Gaming Wireless RGB x2000' AND producator = 'Logitech'),4);
INSERT INTO comenzi VALUES (null,SYSDATE,null,DEFAULT,
    (SELECT id_client FROM clienti WHERE email = 'altEmail@gmail.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'Tastatura Gaming Wireless RGB x1234' AND producator = 'Logitech'),1);
INSERT INTO comenzi VALUES (null,SYSDATE,null,DEFAULT,
    (SELECT id_client FROM clienti WHERE email = 'emailBucuresti@yahoo.com'),
    (SELECT id_produs FROM produse WHERE denumire = 'Mouse Gaming Wireless RGB x2000' AND producator = 'Logitech'),2);

--- Coduri Promotionale
INSERT INTO coduri_promotionale VALUES (
    (SELECT id_client FROM clienti WHERE email = 'unEmail@gmail.com'),
    (SELECT id_comanda FROM comenzi WHERE id_client = (SELECT id_client FROM clienti WHERE email = 'unEmail@gmail.com')
    AND id_produs = (SELECT id_produs FROM produse WHERE denumire = 'Windows 11 Pro' AND producator = 'Microsoft')),
    123,20,SYSDATE,ADD_MONTHS(SYSDATE,1),null);
INSERT INTO coduri_promotionale VALUES (
    (SELECT id_client FROM clienti WHERE email = 'unEmail@gmail.com'),
    (SELECT id_comanda FROM comenzi WHERE id_client = (SELECT id_client FROM clienti WHERE email = 'unEmail@gmail.com')
    AND id_produs = (SELECT id_produs FROM produse WHERE denumire = 'IPhone 20 Pro Max' AND producator = 'Apple')),
    123,20,SYSDATE,ADD_MONTHS(SYSDATE,1),null);
INSERT INTO coduri_promotionale VALUES (
    (SELECT id_client FROM clienti WHERE email = 'altEmail@gmail.com'),
    (SELECT id_comanda FROM comenzi WHERE id_client = (SELECT id_client FROM clienti WHERE email = 'altEmail@gmail.com')
    AND id_produs = (SELECT id_produs FROM produse WHERE denumire = 'Mouse Gaming Wireless RGB x2000' AND producator = 'Logitech')),
    124,5,SYSDATE,ADD_MONTHS(SYSDATE,2),null);
