import os
import pandas as pd
import numpy as np

def transformuj_dane_gus():
    sciezka_ceny = os.path.join('data', 'srednie_cena_mieszkania.csv')
    sciezka_wynagrodzen = os.path.join('data', 'srednie_wynagrodzenie.csv')
    sciezka_wynikowa = os.path.join('data', 'dane_nieruchomosci.csv')

    os.makedirs('data', exist_ok=True)

    if not os.path.exists(sciezka_ceny) or not os.path.exists(sciezka_wynagrodzen):
        print("Błąd: Upewnij się, że umieściłeś pliki pobrane z GUS w folderze /data/!")
        return

    df_cena = pd.read_csv(sciezka_ceny, sep=';')
    df_wyn = pd.read_csv(sciezka_wynagrodzen, sep=';')

    wyn_rows = []
    for idx, row in df_wyn.iterrows():
        woj = row['Nazwa'].title()  
        for rok in [2023, 2024]:
            col_name = f'ogółem;{rok};[zł]'
            val_str = str(row[col_name]).replace(',', '.') 
            try:
                zarobki = float(val_str)
            except ValueError:
                zarobki = np.nan
            wyn_rows.append({'Wojewodztwo': woj, 'Rok': rok, 'Zarobki': zarobki})
    df_wyn_long = pd.DataFrame(wyn_rows)

    cena_rows = []
    for idx, row in df_cena.iterrows():
        woj = row['Nazwa'].title()
        for rok in [2023, 2024]:
            for kat, col_pfx in [('Do 40 m2', 'rynek wtórny;do 40 m2;'), ('40.1 - 60 m2', 'rynek wtórny;od 40,1 do 60 m2;')]:
                col_name = f'{col_pfx}{rok};[zł]'
                val_str = str(row[col_name]).replace(',', '.')
                try:
                    cena = float(val_str)
                except ValueError:
                    cena = np.nan
                cena_rows.append({'Wojewodztwo': woj, 'Rok': rok, 'Kategoria': kat, 'Cena_Mieszkania': cena})
    df_cena_long = pd.DataFrame(cena_rows)

    df_merged = pd.merge(df_cena_long, df_wyn_long, on=['Wojewodztwo', 'Rok'], how='left')

    df_merged['Liczba_Pensji'] = round(df_merged['Cena_Mieszkania'] / df_merged['Zarobki'], 1)

    os.makedirs('data', exist_ok=True)
    
    df_merged.to_csv('data/dane_nieruchomosci.csv', index=False, encoding='utf-8')
    print("Sukces! Dane zintegrowane i zapisane w: data/dane_nieruchomosci.csv")

if __name__ == '__main__':
    transformuj_dane_gus()