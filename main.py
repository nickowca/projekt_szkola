# Szkola - nazwa, klasy
# osoba - imie, nazwisko, data urodzenia
# Nauczyciel - imie, nazwisko, przedmiot
# Uczen - Osoba + numer ucznia, Klasa, slownik ocen
# Klasa - nazwa, lista uzniow, wychowawca
# przedmiot - nazwa, Nauczyciel
# ocena - przedmiot, ocena
# DziennikSzkolny Klasa zarzadzajaca calym systemem

# Historia ocen ucznia
# Rodzice uczniów
# Przedmioty w klasie
# Frekwencja uczniów
# Zadania domowe
# Sprawdziany i egzaminy
# Automatyczne obliczanie średnich ocen

class Szkola:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.klasy = []
        self.nauczyciele = []  # <-- nowa, poprawna kolekcja nauczycieli

    def dodaj_klase(self, Klasa):
        self.klasy.append(Klasa)

    def dodaj_nauczyciela(self, Nauczyciel):
        self.nauczyciele.append(Nauczyciel)

    def __str__(self):
        return (
            f"Szkola: {self.nazwa}, "
            f"Klasy: {[str(klasa_obj) for klasa_obj in self.klasy]}, "
            f"Nauczyciele: {[str(nauczyciel_obj) for nauczyciel_obj in self.nauczyciele]}"
        )


class Osoba:
    def __init__(self, imie, nazwisko, data_urodzenia):
        self.imie = imie
        self.nazwisko = nazwisko
        self.data_urodzenia = data_urodzenia

    def __str__(self):
        return f"{self.imie} {self.nazwisko}, Data urodzenia: {self.data_urodzenia}"


class Nauczyciel(Osoba):
    def __init__(self, imie, nazwisko, data_urodzenia, przedmiot):
        super().__init__(imie, nazwisko, data_urodzenia)
        self.przedmiot = [przedmiot]

    def __str__(self):
        return f"Nauczyciel: {super().__str__()}, Przedmiot: {self.przedmiot}"


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
        self.przedmioty = {}

    def dodaj_ucznia(self, Uczen):
        self.uczniowie.append(Uczen)

    def dodaj_przedmiot(self, nazwa, Nauczyciel):
        self.przedmioty[nazwa] = Nauczyciel

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

    def dodaj_przedmiot_do_Nauczyciela(self, Nauczyciel, przedmiot):
        Nauczyciel.przedmiot.append(przedmiot)

    def ustaw_wychowawce_do_klasy(self, Klasa, wychowawca):
        Klasa.wychowawca = wychowawca

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
                    print(f"    Liczba uczniów: {len(klasa_obj.uczniowie)}")
                    for uczen_obj in klasa_obj.uczniowie:
                        print(f"       {uczen_obj.imie} {uczen_obj.nazwisko} (nr {uczen_obj.numer_ucznia})")

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
                print(f"     Przedmiot: {nauczyciel_obj.przedmiot}")
                print(f"     Data urodzenia: {nauczyciel_obj.data_urodzenia}")
        print("=" * 80)

    def __str__(self):
        return f"Dziennik Szkolny: {[str(Szkola) for Szkola in self.szkoly]}"

import json
import os
import msvcrt
from pathlib import Path


DATA_FILE = Path(__file__).with_name("dziennik.json")


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
    # Nowy format: lista wpisow {przedmiot, ocena}
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

    # Kompatybilnosc: stary slownik ocen {przedmiot: ocena}
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

    # Migracja starego formatu: jesli istnieje historia_ocen, traktuj ja jako glowna liste ocen.
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
    klasa_obj.przedmioty = dane.get("przedmioty", {})
    for uczen_dane in dane.get("uczniowie", []):
        klasa_obj.dodaj_ucznia(uczen_ze_slownika(uczen_dane))
    return klasa_obj


def nauczyciel_do_slownika(nauczyciel_obj):
    return {
        "imie": nauczyciel_obj.imie,
        "nazwisko": nauczyciel_obj.nazwisko,
        "data_urodzenia": nauczyciel_obj.data_urodzenia,
        "przedmiot": nauczyciel_obj.przedmiot,
    }


def nauczyciel_ze_slownika(dane):
    przedmioty = dane.get("przedmiot", [])
    pierwszy_przedmiot = przedmioty[0] if przedmioty else ""
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
        "nauczyciele": [
            nauczyciel_do_slownika(nauczyciel_obj) for nauczyciel_obj in szkola_obj.nauczyciele
        ],
    }


def szkola_ze_slownika(dane):
    szkola_obj = Szkola(dane.get("nazwa", ""))
    for klasa_dane in dane.get("klasy", []):
        szkola_obj.dodaj_klase(klasa_ze_slownika(klasa_dane))
    for nauczyciel_dane in dane.get("nauczyciele", []):
        szkola_obj.dodaj_nauczyciela(nauczyciel_ze_slownika(nauczyciel_dane))
    return szkola_obj


def dziennik_do_slownika(dziennik):
    return {
        "szkoly": [szkola_do_slownika(szkola_obj) for szkola_obj in dziennik.szkoly],
    }


def dziennik_ze_slownika(dane):
    dziennik = DziennikSzkolny()
    for szkola_dane in dane.get("szkoly", []):
        dziennik.dodaj_szkole(szkola_ze_slownika(szkola_dane))
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
        # Gdy plik jest uszkodzony, program startuje od pustych danych.
        return DziennikSzkolny()


def clear():
    os.system("cls")


def pause():
    input("\nNacisnij Enter, aby kontynuowac...")


def czytaj_klawisz():
    key = msvcrt.getch()
    if key in (b"\x00", b"\xe0"):
        return ("ARROW", msvcrt.getch())  # b'H' gora, b'P' dol
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


def Nauczyciele_w_szkole(szkola_obj):
    # preferowane źródło po poprawce:
    if hasattr(szkola_obj, "nauczyciele"):
        return szkola_obj.nauczyciele
    # kompatybilność wstecz (stare dane):
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
    etykiety = [f"{n.imie} {n.nazwisko} ({', '.join(n.przedmiot)})" for n in nauczyciele_lista]
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
            "Dodaj przedmiot Nauczycielowi",
            "Ustaw wychowawce klasy",
            "Dodaj ocene uczniowi",
            "Wyswietl dziennik",
            "Wyswietl oceny ucznia",
            "Wyswietl Nauczycieli szkoly",
            "Wyjscie",
        ]

        wybor = menu_strzalki("Dziennoik", opcje)
        if wybor is None:
            # ESC w menu glownym = wyjscie
            break

        # 1) dodaj_szkole
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

        # 2) dodaj_klase_do_szkoly
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

        # 3) dodaj_ucznia_do_klasy
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

        # 4) dodaj_Nauczyciela_do_szkoly
        elif wybor == 3:
            szk = wybierz_szkole_lub_komunikat(dziennik, "Brak szkol.")
            if szk is None:
                continue

            clear()
            print(f"Szkola: {szk.nazwa}")
            imie = input("Imie Nauczyciela: ").strip()
            nazwisko = input("Nazwisko Nauczyciela: ").strip()
            data_ur = input("Data urodzenia (DD-MM-RRRR): ").strip()
            przedmiot = input("Przedmiot: ").strip()

            if not (imie and nazwisko and data_ur and przedmiot):
                print("Wszystkie pola sa wymagane.")
            else:
                n = Nauczyciel(imie, nazwisko, data_ur, przedmiot)
                dziennik.dodaj_Nauczyciela_do_szkoly(szk, n)
                print("Dodano Nauczyciela.")
            pause()

        # 5) dodaj_przedmiot_do_Nauczyciela
        elif wybor == 4:
            szk = wybierz_szkole_lub_komunikat(dziennik, "Brak szkol.")
            if szk is None:
                continue

            if not Nauczyciele_w_szkole(szk):
                clear()
                print("Brak Nauczycieli w tej szkole.")
                pause()
                continue

            n = wybierz_Nauczyciela(szk)
            if n is None:
                continue

            clear()
            nowy_przedmiot = input("Podaj nowy przedmiot: ").strip()
            if not nowy_przedmiot:
                print("Przedmiot nie moze byc pusty.")
            else:
                dziennik.dodaj_przedmiot_do_Nauczyciela(n, nowy_przedmiot)
                print("Zmieniono przedmiot Nauczyciela.")
            pause()

        # 6) ustaw_wychowawce_do_klasy
        elif wybor == 5:
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

        # 7) dodaj_ocene_uczniowi
        elif wybor == 6:
            clear()
            numer = input("Podaj numer ucznia: ").strip()
            u = znajdz_ucznia_po_numerze(dziennik, numer)
            if u is None:
                print("Nie znaleziono ucznia.")
                pause()
                continue

            przedmiot = input("Przedmiot: ").strip()
            ocena_txt = input("Ocena (1-6): ").strip()

            try:
                ocena_int = int(ocena_txt)
            except ValueError:
                print("Ocena musi byc liczba calkowita.")
                pause()
                continue

            if ocena_int < 1 or ocena_int > 6:
                print("Ocena musi byc w zakresie 1-6.")
            elif not przedmiot:
                print("Przedmiot nie moze byc pusty.")
            else:
                dziennik.dodaj_ocene_uczniowi(u, przedmiot, ocena_int)
                print("Dodano ocene.")
            pause()

        # 8) wyswietl_dziennik
        elif wybor == 7:
            clear()
            dziennik.wyswietl_dziennik()
            pause()

        # 9) wyswietl_oceny_ucznia
        elif wybor == 8:
            clear()
            numer = input("Podaj numer ucznia: ").strip()
            u = znajdz_ucznia_po_numerze(dziennik, numer)
            if u is None:
                print("Nie znaleziono ucznia.")
            else:
                dziennik.wyswietl_oceny_ucznia(u)
            pause()

        # 10) wyswietl_Nauczycieli_szkoly
        elif wybor == 9:
            szk = wybierz_szkole_lub_komunikat(dziennik, "Brak szkol.")
            if szk is None:
                continue

            clear()
            dziennik.wyswietl_Nauczycieli_szkoly(szk)
            pause()

        # 11) wyjscie
        elif wybor == 10:
            clear()
            print("Koniec programu.")
            break




if __name__ == "__main__":
    dziennik = wczytaj_dziennik()

    # Dane startowe tylko przy pierwszym uruchomieniu (gdy brak zapisanych danych)
    if not dziennik.szkoly:
        Szkola1 = Szkola("Szkola podstawowa nr 1")
        Klasa1 = Klasa("1A", "pani Kowalska")
        Uczen1 = Uczen("Jan", "Nowak", "01-01-2010", "001", "1A")
        Nauczyciel1 = Nauczyciel("Anna", "Kowalska", "15-05-1980", "matematyka")

        dziennik.dodaj_szkole(Szkola1)
        dziennik.dodaj_klase_do_szkoly(Szkola1, Klasa1)
        dziennik.dodaj_ucznia_do_klasy(Klasa1, Uczen1)
        dziennik.dodaj_Nauczyciela_do_szkoly(Szkola1, Nauczyciel1)
        dziennik.dodaj_ocene_uczniowi(Uczen1, "matematyka", 5)

    menu(dziennik)
    zapisz_dziennik(dziennik)
