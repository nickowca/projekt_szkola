import json
import os
import msvcrt
from pathlib import Path

DATA_FILE = "dziennik.json"

class Szkola:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.klasy = []
        self.nauczyciele = []
        self.przedmioty = []

    def dodaj_klase(self, Klasa):
        self.klasy.append(Klasa)

    def dodaj_nauczyciela(self, Nauczyciel):
        self.nauczyciele.append(Nauczyciel)

    def dodaj_przedmiot(self, nazwa_przedmiotu):
        if nazwa_przedmiotu and nazwa_przedmiotu not in self.przedmioty:
            self.przedmioty.append(nazwa_przedmiotu)

    def __str__(self):
        return (
            f"Szkola: {self.nazwa}, "
            f"Klasy: {[str(klasa_obj) for klasa_obj in self.klasy]}, "
            f"Nauczyciele: {[str(nauczyciel_obj) for nauczyciel_obj in self.nauczyciele]}, "
            f"Przedmioty: {self.przedmioty}"
        )


class Osoba:
    def __init__(self, imie, nazwisko, data_urodzenia):
        self.imie = imie
        self.nazwisko = nazwisko
        self.data_urodzenia = data_urodzenia

    def __str__(self):
        return f"{self.imie} {self.nazwisko}, Data urodzenia: {self.data_urodzenia}"


class Nauczyciel(Osoba):
    def __init__(self, imie, nazwisko, data_urodzenia, przedmiot=None):
        super().__init__(imie, nazwisko, data_urodzenia)
        self.przedmiot = [przedmiot] if przedmiot else []

    def __str__(self):
        return f"Nauczyciel: {super().__str__()}, Przedmioty: {self.przedmiot}"


class Uczen(Osoba):
    def __init__(self, imie, nazwisko, data_urodzenia, numer_ucznia, Klasa):
        super().__init__(imie, nazwisko, data_urodzenia)
        self.numer_ucznia = numer_ucznia
        self.Klasa = Klasa
        self.oceny = []
        self.frekwencja = {}
        self.rodzice = []

    def dodaj_ocene(self, przedmiot, ocena):
        self.oceny.append({"przedmiot": przedmiot, "ocena": ocena})

    def dodaj_rodzica(self, rodzic):
        self.rodzice.append(rodzic)

    def dodaj_frekwencje(self, data, obecny):
        self.frekwencja[data] = obecny

    def __str__(self):
        return f"Uczen: {super().__str__()}, Numer ucznia: {self.numer_ucznia}, Klasa: {self.Klasa}, Oceny: {self.oceny}"


class Rodzic(Osoba):
    def __init__(self, imie, nazwisko, data_urodzenia):
        super().__init__(imie, nazwisko, data_urodzenia)
        self.uczniowie = []

    def dodaj_dziecko(self, Uczen):
        self.uczniowie.append(Uczen)
        Uczen.dodaj_rodzica(self)


class Klasa:
    def __init__(self, nazwa, wychowawca):
        self.nazwa = nazwa
        self.wychowawca = wychowawca
        self.uczniowie = []
        self.przedmioty = []

    def dodaj_ucznia(self, Uczen):
        self.uczniowie.append(Uczen)

    def dodaj_przedmiot(self, nazwa):
        if nazwa and nazwa not in self.przedmioty:
            self.przedmioty.append(nazwa)

    def __str__(self):
        return f"Klasa: {self.nazwa}, Wychowawca: {self.wychowawca}, Uczniowie: {[str(Uczen) for Uczen in self.uczniowie]}"


class Przedmiot:
    def __init__(self, nazwa, Nauczyciel):
        self.nazwa = nazwa
        self.Nauczyciel = Nauczyciel

    def __str__(self):
        return f"Przedmiot: {self.nazwa}, Nauczyciel: {self.Nauczyciel}"


class ZadanieDomowe:
    def __init__(self, przedmiot, opis, data_oddania):
        self.przedmiot = przedmiot
        self.opis = opis
        self.data_oddania = data_oddania
        self.uczniowie_ktore_oddali = []

    def dodaj_ucznia_ktory_oddal(self, Uczen):
        self.uczniowie_ktore_oddali.append(Uczen)

    def __str__(self):
        return f"Zadanie z {self.przedmiot}: {self.opis}, do: {self.data_oddania}"


class Sprawdzian:
    def __init__(self, przedmiot, data, maksmalna_punktacja):
        self.przedmiot = przedmiot
        self.data = data
        self.maksmalna_punktacja = maksmalna_punktacja
        self.wyniki = {}

    def dodaj_wynik(self, Uczen, punkty):
        self.wyniki[Uczen] = punkty

    def __str__(self):
        return f"Sprawdzian z {self.przedmiot}, {self.data}, max: {self.maksmalna_punktacja} pkt"


class Egzamin(Sprawdzian):
    def __init__(self, przedmiot, data, maksmalna_punktacja, typ):
        super().__init__(przedmiot, data, maksmalna_punktacja)
        self.typ = typ

    def __str__(self):
        return f"Egzamin ({self.typ}) z {self.przedmiot}, {self.data}"


class DziennikSzkolny:
    def __init__(self):
        self.szkoly = []
        self.sprawdziany = []
        self.egzaminy = []
        self.zadania_domowe = []

    def _wyswietl_liste_ocen(self, uczen_obj, naglowek):
        print("\n" + "=" * 60)
        print(f"{naglowek}: {uczen_obj.imie} {uczen_obj.nazwisko}".center(60))
        print("=" * 60)
        if not uczen_obj.oceny:
            print("Brak ocen")
        else:
            pogrupowane = {}
            for wpis in uczen_obj.oceny:
                przedmiot = wpis.get("przedmiot", "-")
                ocena = wpis.get("ocena", "-")
                if przedmiot not in pogrupowane:
                    pogrupowane[przedmiot] = []
                pogrupowane[przedmiot].append(str(ocena))

            for przedmiot, lista_ocen in pogrupowane.items():
                print(f"  {przedmiot:.<25} {{{', '.join(lista_ocen)}}}")
        print("=" * 60)

    def dodaj_szkole(self, Szkola):
        self.szkoly.append(Szkola)

    def dodaj_klase_do_szkoly(self, Szkola, Klasa):
        Szkola.dodaj_klase(Klasa)

    def dodaj_ucznia_do_klasy(self, Klasa, Uczen):
        Klasa.dodaj_ucznia(Uczen)

    def dodaj_ocene_uczniowi(self, Uczen, przedmiot, ocena):
        Uczen.dodaj_ocene(przedmiot, ocena)

    def dodaj_Nauczyciela_do_szkoly(self, Szkola, Nauczyciel):
        Szkola.dodaj_nauczyciela(Nauczyciel)

    def dodaj_przedmiot_do_szkoly(self, Szkola, przedmiot):
        Szkola.dodaj_przedmiot(przedmiot)

    def ustaw_przedmioty_klasy(self, Szkola, Klasa, przedmioty):
        dozwolone = set(getattr(Szkola, "przedmioty", []))
        Klasa.przedmioty = [p for p in przedmioty if p in dozwolone]

    def dodaj_przedmiot_do_Nauczyciela(self, Nauczyciel, przedmiot):
        if przedmiot and przedmiot not in Nauczyciel.przedmiot:
            Nauczyciel.przedmiot.append(przedmiot)

    def ustaw_przedmioty_Nauczyciela(self, Szkola, Nauczyciel, przedmioty):
        dozwolone = set(getattr(Szkola, "przedmioty", []))
        Nauczyciel.przedmiot = [p for p in przedmioty if p in dozwolone]

    def ustaw_wychowawce_do_klasy(self, Klasa, wychowawca):
        Klasa.wychowawca = wychowawca

    def dodaj_sprawdzian(self, sprawdzian):
        self.sprawdziany.append(sprawdzian)

    def dodaj_egzamin(self, egzamin):
        self.egzaminy.append(egzamin)

    def dodaj_zadanie_domowe(self, zadanie):
        self.zadania_domowe.append(zadanie)

    def wyswietl_dziennik(self):
        print("\n" + "=" * 80)
        print("DZIENNIK SZKOLNY".center(80))
        print("=" * 80)
        for i, szkola_obj in enumerate(self.szkoly, 1):
            print(f"\nSZKOŁA {i}: {szkola_obj.nazwa}")
            print("-" * 80)
            for klasa_obj in szkola_obj.klasy:
                if isinstance(klasa_obj, Klasa):
                    print(f"  Klasa: {klasa_obj.nazwa} | Wychowawca: {klasa_obj.wychowawca}")
                    if klasa_obj.przedmioty:
                        print(f"    Przedmioty klasy: {', '.join(klasa_obj.przedmioty)}")
                    print(f"    Liczba uczniów: {len(klasa_obj.uczniowie)}")
                    for uczen_obj in klasa_obj.uczniowie:
                        print(f"       {uczen_obj.imie} {uczen_obj.nazwisko} (nr {uczen_obj.numer_ucznia})")
            if szkola_obj.przedmioty:
                print(f"\n  Przedmioty szkoly: {', '.join(szkola_obj.przedmioty)}")

    def wyswietl_oceny_ucznia(self, Uczen):
        self._wyswietl_liste_ocen(Uczen, "OCENY")

    def wyswietl_historia_ocen_ucznia(self, Uczen):
        self._wyswietl_liste_ocen(Uczen, "HISTORIA OCEN")

    def wyswietl_frekwencje_ucznia(self, Uczen):
        print("\n" + "=" * 60)
        print(f"FREKWENCJA: {Uczen.imie} {Uczen.nazwisko}".center(60))
        print("=" * 60)
        if not Uczen.frekwencja:
            print("Brak danych frekwencji")
        else:
            for data, obecny in Uczen.frekwencja.items():
                status = "Obecny" if obecny else "Nieobecny"
                print(f"  {data:.<35} {status}")
        print("=" * 60)

    def wyswietl_rodzicow_ucznia(self, Uczen):
        print("\n" + "=" * 60)
        print(f"RODZICE: {Uczen.imie} {Uczen.nazwisko}".center(60))
        print("=" * 60)
        if not Uczen.rodzice:
            print("Brak danych rodziców")
        else:
            for idx, rodzic in enumerate(Uczen.rodzice, 1):
                print(f"  {idx}. {rodzic.imie} {rodzic.nazwisko}")
                print(f"     Data urodzenia: {rodzic.data_urodzenia}")
        print("=" * 60)

    def oblicz_srednia_ocen_ucznia(self, Uczen):
        if not Uczen.oceny:
            return 0

        wartosci = [
            wpis.get("ocena")
            for wpis in Uczen.oceny
            if isinstance(wpis, dict) and isinstance(wpis.get("ocena"), (int, float))
        ]
        if not wartosci:
            return 0

        srednia = sum(wartosci) / len(wartosci)
        return round(srednia, 2)

    def wyswietl_srednia_ocen_ucznia(self, Uczen):
        srednia = self.oblicz_srednia_ocen_ucznia(Uczen)
        print("\n" + "=" * 60)
        print(f"ŚREDNIA: {Uczen.imie} {Uczen.nazwisko}".center(60))
        print("=" * 60)
        if srednia == 0:
            print("  Brak ocen")
        else:
            print(f"  Średnia arytmetyczna: {srednia}".center(60))
        print("=" * 60)

    def wyswietl_srednie_oceny_klasy(self, Klasa):
        print("\n" + "=" * 80)
        print(f"ŚREDNIE OCENY KLASY: {Klasa.nazwa}".center(80))
        print("=" * 80)
        if not Klasa.uczniowie:
            print("  Brak uczniów w klasie")
        else:
            for Uczen in Klasa.uczniowie:
                srednia = self.oblicz_srednia_ocen_ucznia(Uczen)
                print(f"  {Uczen.imie} {Uczen.nazwisko:.<30} {srednia}")
        print("=" * 80)

    def wyswietl_Nauczycieli_szkoly(self, Szkola):
        print("\n" + "=" * 80)
        print(f"Nauczyciele: {Szkola.nazwa}".center(80))
        print("=" * 80)
        nauczyciele = getattr(Szkola, "nauczyciele", [])
        if not nauczyciele:
            print("  Brak Nauczycieli")
        else:
            for idx, nauczyciel_obj in enumerate(nauczyciele, 1):
                print(f"  {idx}. {nauczyciel_obj.imie} {nauczyciel_obj.nazwisko}")
                if nauczyciel_obj.przedmiot:
                    print(f"     Przedmioty: {', '.join(nauczyciel_obj.przedmiot)}")
                else:
                    print("     Przedmioty: brak")
                print(f"     Data urodzenia: {nauczyciel_obj.data_urodzenia}")
        print("=" * 80)

    def wyswietl_sprawdziany(self):

        print("\n" + "=" * 80)
        print("SPRAWDZIANY".center(80))
        print("=" * 80)

        if not self.sprawdziany:
            print("Brak sprawdzianów")
        else:
            for i, sprawdzian in enumerate(self.sprawdziany, 1):

                print(f"\n{i}. {sprawdzian.przedmiot}")
                print(f"   Data: {sprawdzian.data}")
                print(f"   Max punktów: {sprawdzian.maksmalna_punktacja}")
                print("   Wyniki:")
                for uczen, punkty in sprawdzian.wyniki.items():
                    print(f"      {uczen.imie} {uczen.nazwisko} - {punkty} pkt")

        print("=" * 80)

    def wyswietl_egzaminy(self):

        print("\n" + "=" * 80)
        print("EGZAMINY".center(80))
        print("=" * 80)
        if not self.egzaminy:
            print("Brak egzaminów")
        else:
            for i, egzamin in enumerate(self.egzaminy, 1):

                print(f"\n{i}. {egzamin.przedmiot}")
                print(f"   Typ: {egzamin.typ}")
                print(f"   Data: {egzamin.data}")
                print(f"   Max punktów: {egzamin.maksmalna_punktacja}")
                print("   Wyniki:")

                for uczen, punkty in egzamin.wyniki.items():
                    print(f"      {uczen.imie} {uczen.nazwisko} - {punkty} pkt")

        print("=" * 80)

    def wyswietl_zadania_domowe(self):

        print("\n" + "=" * 80)
        print("ZADANIA DOMOWE".center(80))
        print("=" * 80)

        if not self.zadania_domowe:
            print("Brak zadań")
        else:
            for i, zadanie in enumerate(self.zadania_domowe, 1):
                print(f"\n{i}. {zadanie.przedmiot}")
                print(f"   Treść: {zadanie.opis}")
                print(f"   Termin: {zadanie.data_oddania}")
                print("   Oddali:")

                if not zadanie.uczniowie_ktore_oddali:
                    print("      Nikt")
                else:
                    for uczen in zadanie.uczniowie_ktore_oddali:
                        print(f"      {uczen.imie} {uczen.nazwisko}")

        print("=" * 80)

    def __str__(self):
        return f"Dziennik Szkolny: {[str(Szkola) for Szkola in self.szkoly]}"


def sprawdzian_do_slownika(sprawdzian):
    return {
        "przedmiot": sprawdzian.przedmiot,
        "data": sprawdzian.data,
        "maksmalna_punktacja": sprawdzian.maksmalna_punktacja,
        "wyniki": {uczen.numer_ucznia: punkty for uczen, punkty in sprawdzian.wyniki.items()},
    }


def egzamin_do_slownika(egzamin):
    return {
        **sprawdzian_do_slownika(egzamin),
        "typ": egzamin.typ,
    }


def zadanie_domowe_do_slownika(zadanie):
    return {
        "przedmiot": zadanie.przedmiot,
        "opis": zadanie.opis,
        "data_oddania": zadanie.data_oddania,
        "uczniowie_ktore_oddali": [uczen.numer_ucznia for uczen in zadanie.uczniowie_ktore_oddali],
    }


def dziennik_do_slownika(dziennik):
    return {
        "szkoly": [szkola_do_slownika(szkoly) for szkoly in dziennik.szkoly],
        "sprawdziany": [sprawdzian_do_slownika(s) for s in dziennik.sprawdziany],
        "egzaminy": [egzamin_do_slownika(e) for e in dziennik.egzaminy],
        "zadania_domowe": [zadanie_domowe_do_slownika(z) for z in dziennik.zadania_domowe],
    }


def dziennik_ze_slownika(dane):
    dziennik = DziennikSzkolny()
    for szkola_dane in dane.get("szkoly", []):
        dziennik.dodaj_szkole(szkola_ze_slownika(szkola_dane))

    for sprawdzian_dane in dane.get("sprawdziany", []):
        sprawdzian = Sprawdzian(
            sprawdzian_dane["przedmiot"],
            sprawdzian_dane["data"],
            sprawdzian_dane["maksmalna_punktacja"]
        )
        for numer, punkty in sprawdzian_dane["wyniki"].items():
            uczen = znajdz_ucznia_po_numerze(dziennik, numer)
            if uczen:
                sprawdzian.dodaj_wynik(uczen, punkty)
        dziennik.dodaj_sprawdzian(sprawdzian)

    for egzamin_dane in dane.get("egzaminy", []):
        egzamin = Egzamin(
            egzamin_dane["przedmiot"],
            egzamin_dane["data"],
            egzamin_dane["maksmalna_punktacja"],
            egzamin_dane["typ"]
        )
        for numer, punkty in egzamin_dane["wyniki"].items():
            uczen = znajdz_ucznia_po_numerze(dziennik, numer)
            if uczen:
                egzamin.dodaj_wynik(uczen, punkty)
        dziennik.dodaj_egzamin(egzamin)

    for zadanie_dane in dane.get("zadania_domowe", []):
        zadanie = ZadanieDomowe(
            zadanie_dane["przedmiot"],
            zadanie_dane["opis"],
            zadanie_dane["data_oddania"]
        )
        for numer in zadanie_dane["uczniowie_ktore_oddali"]:
            uczen = znajdz_ucznia_po_numerze(dziennik, numer)
            if uczen:
                zadanie.dodaj_ucznia_ktory_oddal(uczen)
        dziennik.dodaj_zadanie_domowe(zadanie)

    return dziennik


def zapisz_dziennik(dziennik, sciezka=DATA_FILE):
    with open(sciezka, "w", encoding="utf-8") as plik:
        json.dump(dziennik_do_slownika(dziennik), plik, ensure_ascii=False, indent=2)


def wczytaj_dziennik(sciezka=DATA_FILE):
    if not Path(sciezka).exists():
        return DziennikSzkolny()

    try:
        with open(sciezka, "r", encoding="utf-8") as plik:
            dane = json.load(plik)
        return dziennik_ze_slownika(dane)
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return DziennikSzkolny()


def uczen_do_slownika(uczen_obj):
    return {
        "imie": uczen_obj.imie,
        "nazwisko": uczen_obj.nazwisko,
        "data_urodzenia": uczen_obj.data_urodzenia,
        "numer_ucznia": uczen_obj.numer_ucznia,
        "Klasa": uczen_obj.Klasa,
        "oceny": uczen_obj.oceny,
        "frekwencja": uczen_obj.frekwencja,
        "rodzice": [
            {
                "imie": rodzic.imie,
                "nazwisko": rodzic.nazwisko,
                "data_urodzenia": rodzic.data_urodzenia,
            }
            for rodzic in uczen_obj.rodzice
        ],
    }


def _normalizuj_oceny_z_json(dane):
    oceny_raw = dane.get("oceny", [])

    if isinstance(oceny_raw, list):
        wynik = []
        for wpis in oceny_raw:
            if isinstance(wpis, dict):
                wynik.append({
                    "przedmiot": wpis.get("przedmiot", ""),
                    "ocena": wpis.get("ocena"),
                })
            elif isinstance(wpis, (list, tuple)) and len(wpis) == 2:
                wynik.append({"przedmiot": wpis[0], "ocena": wpis[1]})
        if wynik:
            return wynik

    if isinstance(oceny_raw, dict):
        return [{"przedmiot": p, "ocena": o} for p, o in oceny_raw.items()]

    return []


def uczen_ze_slownika(dane):
    uczen_obj = Uczen(
        dane.get("imie", ""),
        dane.get("nazwisko", ""),
        dane.get("data_urodzenia", ""),
        dane.get("numer_ucznia", ""),
        dane.get("Klasa", ""),
    )

    historia_raw = dane.get("historia_ocen", [])
    if isinstance(historia_raw, list) and historia_raw:
        oceny_z_historii = []
        for wpis in historia_raw:
            if isinstance(wpis, (list, tuple)) and len(wpis) == 2:
                oceny_z_historii.append({"przedmiot": wpis[0], "ocena": wpis[1]})
            elif isinstance(wpis, dict):
                oceny_z_historii.append({
                    "przedmiot": wpis.get("przedmiot", ""),
                    "ocena": wpis.get("ocena"),
                })
        uczen_obj.oceny = oceny_z_historii
    else:
        uczen_obj.oceny = _normalizuj_oceny_z_json(dane)

    uczen_obj.frekwencja = dane.get("frekwencja", {})
    for rodzic_dane in dane.get("rodzice", []):
        rodzic_obj = Rodzic(
            rodzic_dane.get("imie", ""),
            rodzic_dane.get("nazwisko", ""),
            rodzic_dane.get("data_urodzenia", ""),
        )
        rodzic_obj.dodaj_dziecko(uczen_obj)

    return uczen_obj


def klasa_do_slownika(klasa_obj):
    return {
        "nazwa": klasa_obj.nazwa,
        "wychowawca": klasa_obj.wychowawca,
        "przedmioty": klasa_obj.przedmioty,
        "uczniowie": [uczen_do_slownika(uczen_obj) for uczen_obj in klasa_obj.uczniowie],
    }


def klasa_ze_slownika(dane):
    klasa_obj = Klasa(dane.get("nazwa", ""), dane.get("wychowawca", ""))
    przedmioty = dane.get("przedmioty", [])
    if isinstance(przedmioty, dict):
        klasa_obj.przedmioty = list(przedmioty.keys())
    elif isinstance(przedmioty, list):
        klasa_obj.przedmioty = przedmioty
    else:
        klasa_obj.przedmioty = []
    for uczen_dane in dane.get("uczniowie", []):
        klasa_obj.dodaj_ucznia(uczen_ze_slownika(uczen_dane))
    return klasa_obj


def nauczyciel_do_slownika(nauczyciel_obj):
    return {
        "imie": nauczyciel_obj.imie,
        "nazwisko": nauczyciel_obj.nazwisko,
        "data_urodzenia": nauczyciel_obj.data_urodzenia,
        "przedmioty": nauczyciel_obj.przedmiot,
    }


def nauczyciel_ze_slownika(dane):
    przedmioty = dane.get("przedmioty", dane.get("przedmiot", []))
    if isinstance(przedmioty, str):
        przedmioty = [przedmioty] if przedmioty else []
    elif not isinstance(przedmioty, list):
        przedmioty = []

    pierwszy_przedmiot = przedmioty[0] if przedmioty else None
    nauczyciel_obj = Nauczyciel(
        dane.get("imie", ""),
        dane.get("nazwisko", ""),
        dane.get("data_urodzenia", ""),
        pierwszy_przedmiot,
    )
    nauczyciel_obj.przedmiot = przedmioty
    return nauczyciel_obj


def szkola_do_slownika(szkola_obj):
    return {
        "nazwa": szkola_obj.nazwa,
        "klasy": [klasa_do_slownika(klasa_obj) for klasa_obj in szkola_obj.klasy],
        "przedmioty": szkola_obj.przedmioty,
        "nauczyciele": [
            nauczyciel_do_slownika(nauczyciel_obj) for nauczyciel_obj in szkola_obj.nauczyciele
        ],
    }


def szkola_ze_slownika(dane):
    szkola_obj = Szkola(dane.get("nazwa", ""))
    przedmioty = dane.get("przedmioty", [])
    if isinstance(przedmioty, list):
        szkola_obj.przedmioty = przedmioty
    for klasa_dane in dane.get("klasy", []):
        szkola_obj.dodaj_klase(klasa_ze_slownika(klasa_dane))
    for nauczyciel_dane in dane.get("nauczyciele", []):
        szkola_obj.dodaj_nauczyciela(nauczyciel_ze_slownika(nauczyciel_dane))
    return szkola_obj


def clear():
    os.system("cls")


def pause():
    input("\nNacisnij Enter, aby kontynuowac...")


def czytaj_klawisz():
    key = msvcrt.getch()
    if key in (b"\x00", b"\xe0"):
        return ("ARROW", msvcrt.getch())
    if key == b"\r":
        return ("ENTER", None)
    if key == b"\x1b":
        return ("ESC", None)
    return ("OTHER", key)


def menu_strzalki(tytul, opcje):
    if not opcje:
        return None

    index = 0
    while True:
        clear()
        print(f"=== {tytul} ===")
        print("Strzalki GORA/DOL, ENTER = wybierz, ESC = wroc\n")

        for i, nazwa in enumerate(opcje):
            znacznik = ">>" if i == index else "  "
            print(f"{znacznik} {nazwa}")

        typ, val = czytaj_klawisz()
        if typ == "ARROW":
            if val == b"H":
                index = (index - 1) % len(opcje)
            elif val == b"P":
                index = (index + 1) % len(opcje)
        elif typ == "ENTER":
            return index
        elif typ == "ESC":
            return None


def menu_wielokrotnego_wyboru(tytul, opcje, zaznaczone_poczatkowe=None):
    if not opcje:
        return []

    zaznaczone = set(zaznaczone_poczatkowe or [])
    index = 0

    while True:
        clear()
        print(f"=== {tytul} ===")
        print("Strzalki GORA/DOL, ENTER = zaznacz/odznacz, ESC = zatwierdz\n")

        for i, nazwa in enumerate(opcje):
            aktywna = ">>" if i == index else "  "
            check = "* " if nazwa in zaznaczone else ""
            print(f"{aktywna} {check}{nazwa}")

        typ, val = czytaj_klawisz()
        if typ == "ARROW":
            if val == b"H":
                index = (index - 1) % len(opcje)
            elif val == b"P":
                index = (index + 1) % len(opcje)
        elif typ == "ENTER":
            nazwa = opcje[index]
            if nazwa in zaznaczone:
                zaznaczone.remove(nazwa)
            else:
                zaznaczone.add(nazwa)
        elif typ == "ESC":
            return [n for n in opcje if n in zaznaczone]


def znajdz_szkole_po_nazwie(dziennik, nazwa):
    for szkola_obj in dziennik.szkoly:
        if szkola_obj.nazwa == nazwa:
            return szkola_obj
    return None


def znajdz_klase_w_szkole(szkola_obj, nazwa_klasy):
    for klasa_obj in szkola_obj.klasy:
        if isinstance(klasa_obj, Klasa) and klasa_obj.nazwa == nazwa_klasy:
            return klasa_obj
    return None


def znajdz_ucznia_po_numerze(dziennik, numer_ucznia):
    for szkola_obj in dziennik.szkoly:
        for klasa_obj in szkola_obj.klasy:
            if isinstance(klasa_obj, Klasa):
                for uczen_obj in klasa_obj.uczniowie:
                    if uczen_obj.numer_ucznia == numer_ucznia:
                        return uczen_obj
    return None


def znajdz_klase_ucznia(dziennik, uczen):
    for szkola_obj in dziennik.szkoly:
        for klasa_obj in szkola_obj.klasy:
            if isinstance(klasa_obj, Klasa) and uczen in klasa_obj.uczniowie:
                return szkola_obj, klasa_obj
    return None, None


def Nauczyciele_w_szkole(szkola_obj):
    if hasattr(szkola_obj, "nauczyciele"):
        return szkola_obj.nauczyciele
    return [n for n in szkola_obj.klasy if isinstance(n, Nauczyciel)]


def wybierz_szkole(dziennik):
    if not dziennik.szkoly:
        return None
    nazwy = [s.nazwa for s in dziennik.szkoly]
    idx = menu_strzalki("WYBOR SZKOLY", nazwy)
    if idx is None:
        return None
    return dziennik.szkoly[idx]


def wybierz_klase(szkola_obj):
    klasy_lista = [k for k in szkola_obj.klasy if isinstance(k, Klasa)]
    if not klasy_lista:
        return None
    nazwy = [k.nazwa for k in klasy_lista]
    idx = menu_strzalki(f"WYBOR KLASY ({szkola_obj.nazwa})", nazwy)
    if idx is None:
        return None
    return klasy_lista[idx]


def wybierz_Nauczyciela(szkola_obj):
    nauczyciele_lista = Nauczyciele_w_szkole(szkola_obj)
    if not nauczyciele_lista:
        return None
    etykiety = [
        f"{n.imie} {n.nazwisko} ({', '.join(n.przedmiot) if n.przedmiot else 'brak przedmiotow'})"
        for n in nauczyciele_lista
    ]
    idx = menu_strzalki(f"WYBOR NAUCZYCIELA ({szkola_obj.nazwa})", etykiety)
    if idx is None:
        return None
    return nauczyciele_lista[idx]


def wybierz_szkole_lub_komunikat(dziennik, komunikat):
    if not dziennik.szkoly:
        clear()
        print(komunikat)
        pause()
        return None
    return wybierz_szkole(dziennik)


def menu(dziennik):
    while True:
        opcje = [
            "Dodaj szkole",
            "Dodaj klase do szkoly",
            "Dodaj ucznia do klasy",
            "Dodaj Nauczyciela do szkoly",
            "Dodaj przedmiot do szkoly",
            "Przypisz przedmioty do klasy",
            "Przypisz przedmioty Nauczycielowi",
            "Ustaw wychowawce klasy",
            "Dodaj ocene uczniowi",
            "Wyswietl dziennik",
            "Wyswietl oceny ucznia",
            "Wyswietl Nauczycieli szkoly",
            "Wyswietl sprawdziany",
            "Wyswietl egzaminy",
            "Wyswietl zadania domowe",
            "Wyjscie",
        ]

        wybor = menu_strzalki("Dziennik", opcje)
        if wybor is None:
            break

        if wybor == 0:
            clear()
            nazwa = input("Podaj nazwe szkoly: ").strip()
            if not nazwa:
                print("Nazwa nie moze byc pusta.")
            elif znajdz_szkole_po_nazwie(dziennik, nazwa):
                print("Szkola o tej nazwie juz istnieje.")
            else:
                dziennik.dodaj_szkole(Szkola(nazwa))
                print("Dodano szkole.")
            pause()

        elif wybor == 1:
            szk = wybierz_szkole_lub_komunikat(dziennik, "Brak szkol. Najpierw dodaj szkole.")
            if szk is None:
                continue

            clear()
            print(f"Szkola: {szk.nazwa}")
            nazwa_klasy = input("Podaj nazwe klasy (np. 1A): ").strip()
            wychowawca = input("Podaj wychowawce (tekst): ").strip()

            if not nazwa_klasy:
                print("Nazwa klasy nie moze byc pusta.")
            elif znajdz_klase_w_szkole(szk, nazwa_klasy):
                print("Ta Klasa juz istnieje w tej szkole.")
            else:
                dziennik.dodaj_klase_do_szkoly(szk, Klasa(nazwa_klasy, wychowawca))
                print("Dodano klase.")
            pause()

        elif wybor == 2:
            szk = wybierz_szkole_lub_komunikat(dziennik, "Brak szkol.")
            if szk is None:
                continue

            kls = wybierz_klase(szk)
            if kls is None:
                continue

            clear()
            print(f"Szkola: {szk.nazwa}, Klasa: {kls.nazwa}")
            imie = input("Imie: ").strip()
            nazwisko = input("Nazwisko: ").strip()
            data_ur = input("Data urodzenia (DD-MM-RRRR): ").strip()
            numer = input("Numer ucznia: ").strip()

            if not (imie and nazwisko and data_ur and numer):
                print("Wszystkie pola sa wymagane.")
            elif znajdz_ucznia_po_numerze(dziennik, numer):
                print("Uczen o tym numerze juz istnieje.")
            else:
                nowy = Uczen(imie, nazwisko, data_ur, numer, kls.nazwa)
                dziennik.dodaj_ucznia_do_klasy(kls, nowy)
                print("Dodano ucznia.")
            pause()

        elif wybor == 3:
            szk = wybierz_szkole_lub_komunikat(dziennik, "Brak szkol.")
            if szk is None:
                continue

            clear()
            print(f"Szkola: {szk.nazwa}")
            imie = input("Imie Nauczyciela: ").strip()
            nazwisko = input("Nazwisko Nauczyciela: ").strip()
            data_ur = input("Data urodzenia (DD-MM-RRRR): ").strip()

            if not (imie and nazwisko and data_ur):
                print("Imie, nazwisko i data urodzenia sa wymagane.")
            else:
                n = Nauczyciel(imie, nazwisko, data_ur)
                dziennik.dodaj_Nauczyciela_do_szkoly(szk, n)
                print("Dodano Nauczyciela.")
            pause()

        elif wybor == 4:
            szk = wybierz_szkole_lub_komunikat(dziennik, "Brak szkol.")
            if szk is None:
                continue

            clear()
            print(f"Szkola: {szk.nazwa}")
            nazwa_przedmiotu = input("Podaj nazwe przedmiotu: ").strip()
            if not nazwa_przedmiotu:
                print("Nazwa przedmiotu nie moze byc pusta.")
            elif nazwa_przedmiotu in szk.przedmioty:
                print("Ten przedmiot juz istnieje w tej szkole.")
            else:
                dziennik.dodaj_przedmiot_do_szkoly(szk, nazwa_przedmiotu)
                print("Dodano przedmiot do szkoly.")
            pause()

        elif wybor == 5:
            szk = wybierz_szkole_lub_komunikat(dziennik, "Brak szkol.")
            if szk is None:
                continue

            if not szk.przedmioty:
                clear()
                print("Brak przedmiotow w tej szkole. Najpierw dodaj przedmioty.")
                pause()
                continue

            kls = wybierz_klase(szk)
            if kls is None:
                continue

            wybrane_przedmioty = menu_wielokrotnego_wyboru(
                f"PRZYPISZ PRZEDMIOTY DO KLASY {kls.nazwa}",
                szk.przedmioty,
                kls.przedmioty,
            )
            dziennik.ustaw_przedmioty_klasy(szk, kls, wybrane_przedmioty)

            clear()
            print("Zapisano przedmioty klasy:")
            if kls.przedmioty:
                for p in kls.przedmioty:
                    print(f"  * {p}")
            else:
                print("  (brak)")
            pause()

        elif wybor == 6:
            szk = wybierz_szkole_lub_komunikat(dziennik, "Brak szkol.")
            if szk is None:
                continue

            if not Nauczyciele_w_szkole(szk):
                clear()
                print("Brak Nauczycieli w tej szkole.")
                pause()
                continue

            if not szk.przedmioty:
                clear()
                print("Brak przedmiotow w tej szkole. Najpierw dodaj przedmioty.")
                pause()
                continue

            n = wybierz_Nauczyciela(szk)
            if n is None:
                continue

            wybrane_przedmioty = menu_wielokrotnego_wyboru(
                f"PRZYPISZ PRZEDMIOTY DLA {n.imie} {n.nazwisko}",
                szk.przedmioty,
                n.przedmiot,
            )
            dziennik.ustaw_przedmioty_Nauczyciela(szk, n, wybrane_przedmioty)

            clear()
            print("Zapisano przedmioty Nauczyciela:")
            if n.przedmiot:
                for p in n.przedmiot:
                    print(f"  * {p}")
            else:
                print("  (brak)")
            pause()

        elif wybor == 7:
            szk = wybierz_szkole_lub_komunikat(dziennik, "Brak szkol.")
            if szk is None:
                continue

            kls = wybierz_klase(szk)
            if kls is None:
                continue

            clear()
            print(f"Klasa: {kls.nazwa}")
            print("1. Wpisz wychowawce recznie")
            print("2. Wybierz z Nauczycieli szkoly")
            decyzja = input("Wybor (1/2): ").strip()

            if decyzja == "1":
                wych = input("Podaj wychowawce (tekst): ").strip()
                if not wych:
                    print("Wychowawca nie moze byc pusty.")
                else:
                    dziennik.ustaw_wychowawce_do_klasy(kls, wych)
                    print("Ustawiono wychowawce.")
            elif decyzja == "2":
                if not Nauczyciele_w_szkole(szk):
                    print("Brak Nauczycieli do wyboru.")
                else:
                    n = wybierz_Nauczyciela(szk)
                    if n is not None:
                        dziennik.ustaw_wychowawce_do_klasy(kls, f"{n.imie} {n.nazwisko}")
                        print("Ustawiono wychowawce z listy Nauczycieli.")
            else:
                print("Niepoprawny wybor.")
            pause()

        elif wybor == 8:
            clear()
            numer = input("Podaj numer ucznia: ").strip()
            u = znajdz_ucznia_po_numerze(dziennik, numer)
            if u is None:
                print("Nie znaleziono ucznia.")
                pause()
                continue

            szkola_ucznia, klasa_ucznia = znajdz_klase_ucznia(dziennik, u)
            if klasa_ucznia is None:
                print("Nie znaleziono klasy ucznia.")
                pause()
                continue

            if not klasa_ucznia.przedmioty:
                print("Klasa ucznia nie ma przypisanych przedmiotow.")
                pause()
                continue

            idx_przedmiotu = menu_strzalki(
                f"WYBIERZ PRZEDMIOT DLA UCZNIA {u.imie} {u.nazwisko}",
                klasa_ucznia.przedmioty,
            )
            if idx_przedmiotu is None:
                continue

            przedmiot = klasa_ucznia.przedmioty[idx_przedmiotu]
            ocena_txt = input("Ocena (1-6): ").strip()

            try:
                ocena_int = int(ocena_txt)
            except ValueError:
                print("Ocena musi byc liczba calkowita.")
                pause()
                continue

            if ocena_int < 1 or ocena_int > 6:
                print("Ocena musi byc w zakresie 1-6.")
            elif szkola_ucznia and przedmiot not in szkola_ucznia.przedmioty:
                print("Wybrany przedmiot nie nalezy do listy przedmiotow szkoly.")
            else:
                dziennik.dodaj_ocene_uczniowi(u, przedmiot, ocena_int)
                print("Dodano ocene.")
            pause()

        elif wybor == 9:
            clear()
            dziennik.wyswietl_dziennik()
            pause()

        elif wybor == 10:
            clear()
            numer = input("Podaj numer ucznia: ").strip()
            u = znajdz_ucznia_po_numerze(dziennik, numer)
            if u is None:
                print("Nie znaleziono ucznia.")
            else:
                dziennik.wyswietl_oceny_ucznia(u)
            pause()

        elif wybor == 11:
            szk = wybierz_szkole_lub_komunikat(dziennik, "Brak szkol.")
            if szk is None:
                continue

            clear()
            dziennik.wyswietl_Nauczycieli_szkoly(szk)
            pause()

        elif wybor == 12:
            clear()
            dziennik.wyswietl_sprawdziany()
            pause()

        elif wybor == 13:
            clear()
            dziennik.wyswietl_egzaminy()
            pause()

        elif wybor == 14:
            clear()
            dziennik.wyswietl_zadania_domowe()
            pause()

        elif wybor == 15:
            clear()
            print("Koniec programu.")
            break


if __name__ == "__main__":
    dziennik = wczytaj_dziennik()

    if not dziennik.szkoly:
        szkola1 = Szkola("Szkola Podstawowa nr 1")

        dziennik.dodaj_szkole(szkola1)

        przedmioty = [
            "matematyka",
            "polski",
            "angielski",
            "historia",
            "informatyka",
            "biologia",
            "geografia",
            "wf"
        ]

        for przedmiot in przedmioty:
            dziennik.dodaj_przedmiot_do_szkoly(
                szkola1,
                przedmiot
            )

        nauczyciele = [
            Nauczyciel("Anna", "Kowalska", "15-05-1980"),
            Nauczyciel("Piotr", "Nowak", "10-02-1975"),
            Nauczyciel("Maria", "Wisniewska", "21-11-1988"),
            Nauczyciel("Jan", "Zielinski", "01-09-1970"),
        ]

        for nauczyciel in nauczyciele:
            dziennik.dodaj_Nauczyciela_do_szkoly(
                szkola1,
                nauczyciel
            )

        dziennik.ustaw_przedmioty_Nauczyciela(
            szkola1,
            nauczyciele[0],
            ["matematyka"]
        )

        dziennik.ustaw_przedmioty_Nauczyciela(
            szkola1,
            nauczyciele[1],
            ["polski", "historia"]
        )

        dziennik.ustaw_przedmioty_Nauczyciela(
            szkola1,
            nauczyciele[2],
            ["biologia", "geografia"]
        )

        dziennik.ustaw_przedmioty_Nauczyciela(
            szkola1,
            nauczyciele[3],
            ["informatyka", "angielski", "wf"]
        )

        klasa1 = Klasa("1A", "Anna Kowalska")
        klasa2 = Klasa("2B", "Piotr Nowak")

        dziennik.dodaj_klase_do_szkoly(
            szkola1,
            klasa1
        )

        dziennik.dodaj_klase_do_szkoly(
            szkola1,
            klasa2
        )

        dziennik.ustaw_przedmioty_klasy(
            szkola1,
            klasa1,
            przedmioty
        )

        dziennik.ustaw_przedmioty_klasy(
            szkola1,
            klasa2,
            przedmioty
        )

        uczniowie_1A = [
            Uczen("Jan", "Nowak", "01-01-2010", "001", "1A"),
            Uczen("Adam", "Kowalski", "02-02-2010", "002", "1A"),
            Uczen("Kasia", "Wisniewska", "03-03-2010", "003", "1A"),
            Uczen("Ola", "Maj", "04-04-2010", "004", "1A"),
        ]

        uczniowie_2B = [
            Uczen("Tomasz", "Lis", "05-05-2009", "005", "2B"),
            Uczen("Natalia", "Kurek", "06-06-2009", "006", "2B"),
            Uczen("Michal", "Wojcik", "07-07-2009", "007", "2B"),
        ]

        for uczen in uczniowie_1A:
            dziennik.dodaj_ucznia_do_klasy(
                klasa1,
                uczen
            )

        for uczen in uczniowie_2B:
            dziennik.dodaj_ucznia_do_klasy(
                klasa2,
                uczen
            )

        for uczen in uczniowie_1A + uczniowie_2B:
            dziennik.dodaj_ocene_uczniowi(
                uczen,
                "matematyka",
                5
            )

            dziennik.dodaj_ocene_uczniowi(
                uczen,
                "polski",
                4
            )

            dziennik.dodaj_ocene_uczniowi(
                uczen,
                "informatyka",
                6
            )

            dziennik.dodaj_ocene_uczniowi(
                uczen,
                "angielski",
                5
            )

            dziennik.dodaj_ocene_uczniowi(
                uczen,
                "historia",
                3
            )

        for uczen in uczniowie_1A + uczniowie_2B:
            uczen.dodaj_frekwencje(
                "01-09-2025",
                True
            )

            uczen.dodaj_frekwencje(
                "02-09-2025",
                True
            )

            uczen.dodaj_frekwencje(
                "03-09-2025",
                False
            )

        rodzic1 = Rodzic(
            "Marek",
            "Nowak",
            "01-01-1980"
        )

        rodzic2 = Rodzic(
            "Joanna",
            "Nowak",
            "02-02-1982"
        )

        rodzic1.dodaj_dziecko(
            uczniowie_1A[0]
        )

        rodzic2.dodaj_dziecko(
            uczniowie_1A[0]
        )

        zadanie1 = ZadanieDomowe(
            "matematyka",
            "Strona 25 zadanie 1-5",
            "10-09-2025"
        )

        zadanie1.dodaj_ucznia_ktory_oddal(
            uczniowie_1A[0]
        )

        zadanie1.dodaj_ucznia_ktory_oddal(
            uczniowie_1A[1]
        )

        dziennik.dodaj_zadanie_domowe(zadanie1)

        sprawdzian1 = Sprawdzian(
            "matematyka",
            "15-09-2025",
            50
        )

        sprawdzian1.dodaj_wynik(
            uczniowie_1A[0],
            45
        )

        sprawdzian1.dodaj_wynik(
            uczniowie_1A[1],
            39
        )

        sprawdzian1.dodaj_wynik(
            uczniowie_1A[2],
            50
        )

        dziennik.dodaj_sprawdzian(sprawdzian1)

        egzamin1 = Egzamin(
            "angielski",
            "20-10-2025",
            100,
            "Semestralny"
        )

        egzamin1.dodaj_wynik(
            uczniowie_2B[0],
            88
        )

        egzamin1.dodaj_wynik(
            uczniowie_2B[1],
            91
        )

        dziennik.dodaj_egzamin(egzamin1)

    menu(dziennik)
    zapisz_dziennik(dziennik)


# C:\ProgramData\anaconda3\python.exe "C:\Users\michalskif\PycharmProjects\projekt_szkola\main.py"
# C:\ProgramData\anaconda3\python.exe O:\Python\Project\main.py
