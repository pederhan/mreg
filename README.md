# mreg

### Grunnlag for prosjektet:

#### [Kravspec for MREG fra hostmaster](https://www.usit.uio.no/om/organisasjon/iti/gd/doc/hostmaster/mreg-krav.html)

#### [Spesifikasjon for Hostpolicy-modulen](http://www.usit.uio.no/om/tjenestegrupper/cerebrum/utvikling/dokumentasjon/dns/hostpolicy.html)

#### [Kort om dnsinfo ved USIT](https://www.usit.uio.no/om/organisasjon/iti/gd/doc/hostmaster/dnsinfo-dok.html)

### Dokumentasjon(kravspesifikasjon):

#### [API](API.md)

### Nyttige lenker:

##### Typer DNS-records
- [SOA](https://en.wikipedia.org/wiki/SOA_record),
[NS (1)](http://help.dnsmadeeasy.com/managed-dns/dns-record-types/ns-record/)
[(2)](https://www.digitalocean.com/community/questions/what-is-the-point-of-the-ns-records)
- [A](https://en.wikipedia.org/wiki/List_of_DNS_record_types#A) /
[AAAA](https://en.wikipedia.org/wiki/IPv6_address#Domain_Name_System),
 [CNAME](https://en.wikipedia.org/wiki/CNAME_record),
 [PTR](https://en.wikipedia.org/wiki/List_of_DNS_record_types#PTR),
 [HINFO](https://en.wikipedia.org/wiki/List_of_DNS_record_types#HINFO)
- [NAPTR](https://en.wikipedia.org/wiki/NAPTR_record),
[SRV](https://en.wikipedia.org/wiki/SRV_record),
[telefonnr-mapping/ENUM](https://en.wikipedia.org/wiki/Telephone_number_mapping)
- [TXT](https://en.wikipedia.org/wiki/TXT_record)
- [LOC](https://en.wikipedia.org/wiki/LOC_record)
- [andre typer](https://en.wikipedia.org/wiki/List_of_DNS_record_types)

### Logging av request og responses på API-siden

[django-logging](https://github.com/cipriantarta/django-logging)
Denne modulen ble valgt fordi den out-of-the-box gjør alt vi vil og er customizable.
Bonus: Den støtter elasticsearch også.


### Setup av sample-database i postgres (tar utgangspunkt i Fedora og python3)
- Trenger pakkene 'postgresql', 'postgresql-server', deretter initialiserer vi
databaseclusteret og bygger sampledatabasen fra samples/sample_data_dump
- Antar root
```
dnf update
dnf install postgresql postgresql-server
postgresql-setup --initdb
service postgresql start
```
- Nå som postgresql er oppe og går, trenger vi å klone (ev. forke) git-repoet
og sette opp databasen med psql
```
dnf install git
git clone git@github.com:usit-gd/mreg.git
cp mreg/samples/sample_data_dump /tmp
su - postgres
psql -f /tmp/sample_data_dump postgres
```
- Etter at dette har kjørt, er det på tide å få på plass ymse django dependencies.
I repoet ligger det en fil 'requirements.txt' som inneholder alle pakkene som trengs for å sette i gang.
Før den filen kommer til nytte, må vi ha på plass en package-manager for python som kan lese den. Her bruker vi pip.
I tillegg setter vi opp et virtual environment for python-pakkene, så de ikke interagerer med eventuelt andre pakker som
må være installert på systemet. Det kan python3 selv sette opp med 'venv'-kommandoen sammen med -m flagget.
Her legger vi virtual-environmentet i mappen 'venv' inni repoet.
```
dnf install python-pip
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
- For at django skal connecte til lokal database, og for å kunne gjøre testing lokalt uten å måtte gjøre endringer
i djangos settings-filer, kan man opprette en fil 'local_settings.py' i mappen 'mregsite'.
Djangos egen settings.py leter gjennom denne filen etter definisjoner som overskriver djangos egne.
For å connecte til lokal database kan man legge inn følgende:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mreg_sample',
        'USER': 'mreg_user',
        'PASSWORD': 'mregdbpass',
        'HOST': 'localhost',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'mreg_sample',
#     }
# }
```
- Den utkommenterte DATABASES definisjonen brukes gjerne for å kjøre tester når man endrer noe i datamodellene,
så slipper man å kjøre migreringer til ekstern database etc. før man vet at det funker.
- For at django skal få connecta til databasen må vi inn i en config-fil og gjøre et par små endringer.
I filen '/var/lib/pgsql/data/pg_hba.conf' må 'METHOD' for IPv4 og IPv6 local connections endres fra 'ident' til 'md5',
slik at den bruke passordautentisering. (Linjene er i bunn av filen)
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            ident
# IPv6 local connections:
host    all             all             ::1/128                 ident
```
- postgresql må restartes for at endringen skal tre i kraft
```
sudo service postgresql restart
```
- Start django-serveren ved å kjøre
```
python manage.py runserver
```
- psycopg2-pakken vil antagelig mase litt om en kommende rename. Det vil bli tatt høyde for senere.
- Du skal nå kunne gå til en browser og videre til http://localhost:8000/ressurs/
for å bl.a se på hva API'et har av info, der 'ressurs' er f.eks 'hosts' eller 'subnets'.

