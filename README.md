# Program za pretvorbo koordinat digitaliziranih pluviogramov

pluviodata_converter.py je program za pretvorbo koordinat digitaliziranih pluviogramov.

Za optimalno delovanje priporočam pandas==1.3.5

Program pluviodata_converter.py je potrebno skopirati in zagnati v mapi, kjer so .csv datoteke digitaliziranih pluviografov. 
Imena datotek se morajo začeti s **trimestno** kodo postaje (npr. 035-krneki.csv) za katero lahko potem sledijo poljubni znaki, vsebovati pa mora le datume za določen mesec.
Program vrne datoteke s pretvorjenimi koordinatami ter v ime datoteke zapiše kodo postaje, leto in mesec in doda končnico z zaporedno številko (npr. o1922111.001, o1922111.002, etc.) Program datoteke shrani v direktorijih ločenih po mesecih (npr. Output_files2201).

Za .csv datoteke digitaliziranih pluviogramov velja:
- Suh dan: datuma ni v tabeli
- Manjkajoč dan: v tabeli je samo datum vendar brez priprdajočih podatkov
- Deževen dan: v tabeli je datum s podatki
- Dan s snegom: za datumom v tabeli je dodan -s (npr. 29-11-2021-s)
- Dan pri katerem so bile ročno dodane točke brez prekrivanja: za datumom v tabeli je dodan -r (npr. 29-11-2021-r)


Program samodejno odpravi prekrivanje točk (ob praznjenju posode) na časovnem intervalu 15 minut. Za datume z dodanim -r (npr. 29-11-2021-r) je prej omenjeni časovni interval 0.

