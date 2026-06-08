import os
import json
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import pandas as pd
import plotly.express as px
import plotly.utils

main = Blueprint('main', __name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'dane_nieruchomosci.csv')

def pobierz_dane():
    return pd.read_csv(DATA_PATH)

@main.route('/')
def index():
    return render_template('base.html')

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    df = pobierz_dane()
    
    wojewodztwa = sorted(df['Wojewodztwo'].unique())
    kategorie = sorted(df['Kategoria'].unique())
    
    wybrane_wojewodztwo = request.form.get('wojewodztwo') or 'Opole'  
    wybrana_kategoria = request.form.get('kategoria') or kategorie[0]
    
    if wybrane_wojewodztwo.upper() in [w.upper() for w in wojewodztwa]:
        wybrane_wojewodztwo = [w for w in wojewodztwa if w.upper() == wybrane_wojewodztwo.upper()][0]

    # --- WYKRES 1 ---
    df_filtered = df[(df['Wojewodztwo'] == wybrane_wojewodztwo) & (df['Kategoria'] == wybrana_kategoria)]
    
    fig1 = px.bar(
        df_filtered,
        x='Rok',
        y='Liczba_Pensji',
        text='Liczba_Pensji',
        labels={'Liczba_Pensji': 'Wskaźnik (Liczba pensji)', 'Rok': 'Rok'},
        title=f'Ile pensji brutto kosztuje mieszkanie ({wybrana_kategoria}) w regionie: {wybrane_wojewodztwo}',
        color='Rok',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig1.update_traces(textposition='outside')
    fig1.update_layout(
        template='plotly_white', 
        showlegend=False,
        xaxis={'type': 'category'}  
    )
    graph_json1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    # --- WYKRES 2 ---
    df_ranking = df[(df['Rok'] == 2024) & (df['Kategoria'] == wybrana_kategoria)].sort_values(by='Liczba_Pensji')
    
    fig2 = px.bar(
        df_ranking,
        x='Liczba_Pensji',
        y='Wojewodztwo',
        orientation='h',
        text='Liczba_Pensji',
        labels={'Liczba_Pensji': 'Liczba wymaganych pensji', 'Wojewodztwo': 'Województwo'},
        title=f'Porównanie dostępności mieszkań ({wybrana_kategoria}) w Polsce w 2024 r.',
        color='Liczba_Pensji',
        color_continuous_scale=px.colors.sequential.Reds
    )
    fig2.update_traces(textposition='outside')
    fig2.update_layout(template='plotly_white', showlegend=False, height=550)
    graph_json2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    row_2024 = df_filtered[df_filtered['Rok'] == 2024]
    if not row_2024.empty:
        cena_val = row_2024['Cena_Mieszkania'].values[0]
        zarobki_val = row_2024['Zarobki'].values[0]
        pensje_val = row_2024['Liczba_Pensji'].values[0]
    else:
        cena_val = zarobki_val = pensje_val = 0

    return render_template(
        'dashboard.html', 
        name=current_user.username,
        wojewodztwa=wojewodztwa,
        kategorie=kategorie,
        wybrane_wojewodztwo=wybrane_wojewodztwo,
        wybrana_kategoria=wybrana_kategoria,
        graph_json1=graph_json1,
        graph_json2=graph_json2,
        cena_val=f"{cena_val:,.0f}".replace(",", " "),
        zarobki_val=f"{zarobki_val:,.2f}".replace(",", " ").replace(".", ","),
        pensje_val=pensje_val
    )