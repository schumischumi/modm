

  302  baloosearch Pfarrkirchen type:Document~
  303  baloosearch Pfarrkirchen type:Document
  304  baloosearch Pfarrkirchen type:Document *.pdf
  305  baloosearch Pfarrkirchen*.pdf type:Document 
  306  baloosearch Pfarrkirchen type:Document and .pdf
  307  baloosearch Pfarrkirchen type:Document and pdf
  308  baloosearch Pfarrkirchen type:Document and PDF
  309  baloosearch Pfarrkirchen and PDF
  310  baloosearch Pfarrkirchen pdf type:Document 
  311  baloosearch Pfarrkirchen .pdf type:Document 

user:~ $ baloosearch --help
Aufruf: baloosearch [Optionen] query

Optionen:
  -l, --limit <Begrenzung>     Die maximale Anzahl der Ergebnisse
  -o, --offset <Versatz>       Versatz für die Startposition der Suche
  -t, --type <typeStr>         Datentyp, nach dem gesucht werden soll
  -d, --directory <directory>  Suche auf den angegebenen Ordner beschränken
  -i, --id                     Dokumentkennung anzeigen
  -h, --help                   Zeigt Hilfe zu den Kommandozeilenoptionen an.
  --help-all                   Zeigt Hilfe einschließlich Qt-spezifischer
                               Optionen an.
  -v, --version                Zeigt Versionsinformation an.


user:~ $ baloosearch Pfarrkirchen .pdf type:Document 
/home/user/Documents/LebenslaufV2.pdf
/home/user/Nextcloud/Backup/gdrive/Lebenslauf.pdf
/home/user/Nextcloud/Backup/gdrive/Lebenslauf 2018.pdf
/home/user/Nextcloud/Backup/gdrive/bewerbung/up/Lebenslauf.pdf
/home/user/Nextcloud/Backup/gdrive/bewerbung/up/bewerbung.pdf
/home/user/Nextcloud/Backup/gdrive/bewerbung/Lebenslauf1.pdf
Verstrichen: 5,71245 msec
user:~ $ baloosearch youngstars Pfarrkirchen .pdf type:Document 
Verstrichen: 3,08755 msec
user:~ $ baloosearch young Pfarrkirchen .pdf type:Document 
/home/user/Documents/LebenslaufV2.pdf
/home/user/Nextcloud/Backup/gdrive/Lebenslauf.pdf
/home/user/Nextcloud/Backup/gdrive/Lebenslauf 2018.pdf
Verstrichen: 3,54281 msec
user:~ $ baloosearch young-stars Pfarrkirchen .pdf type:Document 
/home/user/Documents/LebenslaufV2.pdf
/home/user/Nextcloud/Backup/gdrive/Lebenslauf.pdf
/home/user/Nextcloud/Backup/gdrive/Lebenslauf 2018.pdf
Verstrichen: 6,07827 msec
user:~ $ baloosearch young*stars Pfarrkirchen .pdf type:Document 
/home/user/Documents/LebenslaufV2.pdf
/home/user/Nextcloud/Backup/gdrive/Lebenslauf.pdf
/home/user/Nextcloud/Backup/gdrive/Lebenslauf 2018.pdf
