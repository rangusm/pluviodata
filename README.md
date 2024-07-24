# Program za pretvorbo koordinat digitaliziranih pluviogramov

pluviodata_converter.py je program za pretvorbo koordinat digitaliziranih pluviogramov.

Ukaz za zagon (v mapi, kjer so .csv datoteke): <br>
```
python pluviodata_converter.py
```

Program pluviodata_converter.py je potrebno zagnati v mapi, kjer so .csv datoteke digitaliziranih pluviografov. 
Imena datotek se morajo začeti s **trimestno** kodo postaje (npr. **035**-krneki.csv) za katero lahko potem sledijo poljubni znaki, vsebovati pa mora le datume za določen mesec.
Program vrne datoteke s pretvorjenimi koordinatami ter v ime datoteke zapiše trimestno kodo postaje (o192), leto (21) in mesec(11) in doda končnico z zaporedno številko (.001). Najprej novi datoteki pripiše končnico .001, če pa ta že obstaja, potem ji pripiše končnico z naslednjo zaporedno številko (npr. o1922111.001, o1922111.002, etc.) 
Program datoteke shrani v direktorijih ločenih po mesecih in letih z imenom Output_files ter jim doda relevantna leto in mesec (npr. Output_files2111).<br>
Če je potrebno popraviti .csv datoteke, se najprej iz mape vse prejšnje .csv datoteke pobriše in potem v mapo skopira popravljene .csv datoteke. Po zagonu, program v mapi (npr. Output_files2101) ustvari nove datoteke s končnico .002 (če datoteke s končnico .001 že obstajajo).

Za .csv datoteke digitaliziranih pluviogramov velja:
- Suh dan: datuma ni v tabeli
- Manjkajoč dan: v tabeli je samo datum vendar brez priprdajočih podatkov
- Deževen dan: v tabeli je datum s podatki
- Dan s snegom: za datumom v tabeli je dodan -s (npr. 29-11-2021-s)
- Dan pri katerem so bile ročno dodane točke brez prekrivanja: za datumom v tabeli je dodan -r (npr. 29-11-2021-r)

<br>
Program samodejno odpravi šumenje ter prekrivanje točk (ob praznjenju posode) na časovnem intervalu 20 minut. Za datume z ročno digitaliziranimi prelivanji in torej dodanim -r (npr. 29-11-2021-r) je prej omenjeni časovni interval 0.

Program tudi zazna primere, je posamezna točka oddaljena vsaj 7000 enot  oz. 7 mm (v y-smeri) od sosednjih točk na krivulji in v terminal izpiše postajo, datum in točko izven krivulje (npr.: 086 23.05.2021 Tocka (2111, 9827) izven krivulje.) ter ustvari .pdf datoteko s slikami izrisanih grafov za te dni.
V terminalu se izpiše tudi ime in lokacija .pdf datoteke s slikami grafov in se jo lahko odpre ročno. Ime .pdf datoteke z grafi je avtomatsko generirano kot Slike_grafov_ z datumom in uro zagona programa (npr.: Slike_grafov_30-05-2022_10-53-52.pdf).
Za vse dni, kjer program javi 'točko izven krivulje' je potrebno pregledati in primerjati izrisani graf s scanom pluviograma:
-	Preveriti potencialno sumljive skoke.
-	Preveriti potencialno prekrivanje točk (premik časa nazaj).

<br>
Za optimalno delovanje priporočam pandas==1.3.5 <br>
Koda je bila napisana na Python 3.10.0
