import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df_nba = pd.read_csv('nba.csv')

year_list = df_nba['year_id'].unique().tolist()
equipos_list = df_nba['fran_id'].unique().tolist()

with st.sidebar:
    year = st.selectbox('Seleccionar año', year_list, 0)
    team = st.selectbox('Seleccionar equipo', equipos_list, 0)

    option_map = {
        1:'Temporada regular',
        2:'Playoffs',
        3:'Ambos'
    }

    selection = st.pills(
        "Seleccionar tipo de temporada",
        options=option_map.keys(),
        format_func=lambda x: option_map[x],
        selection_mode="single",
        default=1,
    )
    st.write(
        f"Seleccionaste: {option_map[selection]}"
    )

#filtros
team_filter = (df_nba['fran_id'] == team) & (df_nba['year_id'] == year)
season_filter = (df_nba['seasongame'] == option_map[selection])

col1, col2 = st.columns([2,3])
with col1:
    st.write("""#### Juegos Ganados/Perdidos por temporadas """)
    df = df_nba[team_filter]

    df['wins'] = df['game_result'].apply(lambda x: 1 if x == 'W' else 0)
    df['losses'] = df['game_result'].apply(lambda x: 1 if x == 'L' else 0)
    df['cum_wins'] = df['wins'].cumsum()
    df['cum_losses'] = df['losses'].cumsum()

    # Crear el gráfico de líneas
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(df['date_game'], df['cum_wins'], label='Juegos Ganados', color='blue', linestyle='-', marker='o')
    ax.plot(df['date_game'], df['cum_losses'], label='Juegos Perdidos', color='red', linestyle='-', marker='o')
    # Etiquetas y título
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Cantidad de Juegos')
    ax.set_title(f'Acumulado de Juegos Ganados y Perdidos - {team} ({year})')
    ax.legend()
    st.pyplot(fig)

with col2:
    df = df_nba[team_filter]
    st.dataframe(df, width = 400)