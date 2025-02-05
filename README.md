# Ispitni Projekat - Pygame Animacija sa LSL i OpenVibe
Ispitni projekat iz fiziološkog računarstva – animacija u Pygame-u povezana sa signalima iz OpenVibe-a poslatim preko LSL-a. Kišne kapi se generišu u zavisnosti od disajnog ritma i na osnovu njihove količine, cveće "raste".


## Opis projekta
Ovaj projekat je deo ispita iz fiziološkog računarstva i predstavlja Pygame animaciju povezanju sa Live Stream Link (LSL) protokolom. Animacija prikazuje cveće koje reaguje na dolazne podatke o ritmu disanja, pri čemu brzina disanja kontroliše padanje kišnih kapljica koje utiču na veličinu cvetova.

## Tehnologije
- **Python** (verzija 3.x)
- **Pygame** (za vizuelizaciju)
- **pylsl** (za rad sa LSL protokolom)
- **OpenVibe** (kao izvor fizioloških podataka)

## Kako funkcioniše?
1. Program pretražuje dostupne LSL stream-ove i pokušava da se poveže sa `BreathingSignal` stream-om.
2. Kada pronađe stream, periodično čita vrednosti ritma disanja.
3. Na osnovu vrednosti ritma disanja generišu se kišne kapljice.
4. Kapljice padaju i pri kontaktu sa cvetovima povećavaju njihovu veličinu.
5. Efekat traje određeno vreme, nakon čega cvetovi postepeno vraćaju prvobitnu veličinu.

## Pokretanje projekta
1. Kloniraj repozitorijum:
   ```sh
   git clone https://github.com/pygame-fizioloska-aplikacija.git
   ```
2. Instaliraj potrebne zavisnosti:
   ```sh
   pip install pygame pylsl
   ```
3. Pokreni skriptu:
   ```sh
   python ispit.py
   ```

## Podešavanja
- **Maksimalan broj kapljica:** 1500
- **Maksimalan broj pogodaka cveta:** 15
- **Brzina opadanja efekta:** 30
- **Brzina generisanja kapljica:** proporcionalna ritmu disanja

## Zahtevi
- OpenVibe softver koji generiše `BreathingSignal` stream
- Python 3.x

## Autor
Marija Erić

## Licenca
Ovaj projekat je otvorenog koda pod [MIT licencom](LICENSE).

