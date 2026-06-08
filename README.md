#  Interaktywna Analiza Rynku Nieruchomości w Polsce (dane GUS)

Aplikacja internetowa typu *end-to-end* integrująca etap czyszczenia i transformacji surowych danych statystycznych Głównego Urzędu Statystycznego (GUS) z bezpiecznym, autoryzowanym panelem raportowym. Projekt umożliwia badanie relacji cen mieszkań na rynku wtórnym do przeciętnych miesięcznych wynagrodzeń w 16 województwach na przełomie lat 2023–2024.

---

##  Stos technologiczny

* **Język programowania:** Python 3.12+
* **Backend:** Flask (Routing, System fabryki aplikacji, Blueprints)
* **Baza danych:** SQLite + Flask-SQLAlchemy (Zarządzanie kontami użytkowników)
* **Analiza danych:** Pandas (Automatyczny potok danych ETL)
* **Wizualizacja:** Plotly (Interaktywne wykresy dynamiczne)
* **Uwierzytelnianie:** Flask-Login (Zarządzanie sesjami) + Werkzeug (Hashowanie haseł)
* **Frontend:** Bootstrap 5 (Responsywny interfejs użytkownika - RWD)

---

##  Struktura katalogów projektu

```text
GusProjekt/
│
├── app/
│   ├── __init__.py          # Inicjalizacja aplikacji i rozszerzeń
│   ├── models.py            # Model bazy danych (Użytkownicy)
│   ├── auth.py              # Logika logowania i rejestracji (Blueprint)
│   ├── main.py              # Logika panelu analitycznego i wykresów (Blueprint)
│   │
│   └── templates/           # Szablony HTML (Jinja2)
│       ├── base.html        # Główny układ strony
│       ├── login.html       # Ekran logowania
│       ├── register.html    # Ekran rejestracji
│       └── dashboard.html   # Panel raportowy (dostępny po zalogowaniu)
│
├── data/
│   ├── srednie_cena_mieszkania.csv  # Surowe dane GUS
│   ├── srednie_wynagrodzenie.csv    # Surowe dane GUS
│   └── dane_nieruchomosci.csv       # Oczyszczony plik wynikowy po procesie ETL
│
├── config.py                # Konfiguracja zmiennych aplikacji
├── convert_data.py          # Skrypt przetwarzający surowe pliki GUS
├── requirements.txt         # Lista wymaganych zależności i bibliotek
└── run.py                   # Plik uruchomieniowy serwera
```
* **1. Klonowanie repozytorium lub pobranie plików
Upewnij się, że znajdujesz się w docelowym katalogu roboczym, a następnie pobierz projekt:
git clone <url_twojego_repozytorium_na_githubie>
cd GusProjekt
* **2. Utworzenie i aktywacja środowiska wirtualnego
Bash
python -m venv venv
venv\Scripts\activate
* **3. Instalacja wymaganych bibliotek
Zainstaluj wszystkie zależności zdefiniowane w pliku requirements.txt:
pip install -r requirements.txt
* **4. Przygotowanie danych (Proces ETL)
Przed pierwszym uruchomieniem aplikacji należy uruchomić skrypt, który pobierze surowe pliki GUS z folderu /data/, oczyści je i wygeneruje docelową bazę analityczną w formacie CSV:
python convert_data.py
* **5. Uruchomienie aplikacji Flask
Uruchom serwer deweloperski za pomocą pliku startowego:
python run.py
