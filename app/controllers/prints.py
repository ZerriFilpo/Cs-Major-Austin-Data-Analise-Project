import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import services.stats_service as ss

import os

from rich.console import Console

from rich.table import Table

from rich.panel import Panel

from rich.text import Text

from rich.align import Align

console = Console()

def cor_rating(valor):

    if valor < 0.96: return "bold red"
    elif valor <= 1.14: return "white"
    else: return "bold green"

def cor_kast(valor):

    if valor < 65: return "bold red"
    elif valor < 75: return "white"
    else: return "bold green"

def cor_dmr(valor):

    if valor < 68: return "bold red"
    elif valor <= 80: return "white"
    else: return "bold green"

def get_cor(nome, valor):

    if nome == 'Rating':

        return cor_rating(valor)

    elif nome == "kast":

        return cor_kast(valor)
    
    elif nome == "dmr":

        return cor_dmr(valor)

def cabecalho(titulo, nick, role, team, tournament_name):

    texto = Text()

    texto.append(f"{nick}\n", style="bold white")

    texto.append(f"Role: {role} | Team: {team}\n", style="white")

    texto.append(f"{tournament_name}", style="dim")

    panel = Panel(
        Align.center(texto),
        title=f"[bold]{titulo}[bold]",
        border_style="blue"
    )

    console.print(panel)


def rich_table(dados, headers, titulo=None, colorir_coluna=None):

    table = Table(title=titulo, expand=True)

    for header in headers:

        table.add_column(header)

    color_list = colorir_coluna or {}

    for linha in dados:

        linha_formatada = []

        for i, v in enumerate(linha):

            col_name = headers[i]

            if col_name in color_list:

                try:

                    color = color_list[col_name](float(v))

                    colored_text = Text(str(v), style=color)

                    linha_formatada.append(colored_text)

                except:

                    linha_formatada.append(str(v))

            else:

                linha_formatada.append(str(v))

        table.add_row(*linha_formatada)

    console.print(table)

def limpar_tela():
    os.system('clear')  # Linux/Mac
    # No Windows seria: os.system('cls')

def pausar():
    input("\nPress Enter to continue...")

def print_player_best_map(player_id, tournament_id, tournament_name):

    player_tournament_id = ss.get_player_tournament_id(player_id, tournament_id)

    player = ss.get_player_by_id(player_id)

    best_map = ss.get_player_best_map(player_tournament_id)

    headers = ["Map", "Average rating"]

    color = {"Average rating": cor_rating}

    rich_table([best_map], headers, f"{player[1]}'s best map and average rating on it", color)

    pausar()





def print_player_stats(player_id, torunament_id, torunament_name):

    player_tournament_id = ss.get_player_tournament_id(player_id, torunament_id)

    player_stats = ss.get_player_stats(player_tournament_id)

    if player_stats is None:

        print("No stats found for this player")

        pausar()

        return

    (stats, resumo, best_resumo) = player_stats

    headers = ['Round', 'BO', "Map", "Team", "Opponent", "Winner", "Rating",
                "Kills", 'Assists', 'Deaths', 'kast','adr']
    
    dados = []

    nick = stats[0][4]
    role = stats[0][5]
    team = stats[0][1]

    cabecalho("Player Stats", nick, role, team, torunament_name)

    for stat in stats:

        (map_, team, opponent, winner,
        nick, role, kills, assists, deaths,
        kast, dmr, rating, round_des, bo) = stat

        linha = (round_des, bo, map_, team, opponent, winner, rating,
                 kills, assists, deaths, kast, dmr)
        
        dados.append(linha)

    color_funcs = {
    "Rating": cor_rating,
    "kast": cor_kast,
    "adr": cor_dmr
    }
    
    rich_table(dados, headers, colorir_coluna=color_funcs)

    print()

    input("\nPress Enter to see Player Average...")

    limpar_tela()

    nick = stats[0][4]
    role = stats[0][5]
    team = stats[0][1]

    cabecalho("Averege Stats", nick, role, team, torunament_name)


    over_headers = ["Rating", "Kills", 'Assists', 'Deaths', 'kast', 'adr']

    dados_resumo = [(
        resumo['avg_rating'],
        resumo['avg_kill'],
        resumo['avg_assists'],
        resumo['avg_deaths'],
        resumo['avg_kast'],
        resumo['avg_dmr']
    )]

    rich_table(dados_resumo, over_headers, colorir_coluna=color_funcs)

    input("\nPress Enter to see Player Peak Stats...")

    limpar_tela()

    cabecalho("Peak Stats", nick, role, team, torunament_name)

    
    rich_table([best_resumo], over_headers, colorir_coluna=color_funcs)

    pausar()

def list_players_from_team(team_id, tournament_id, tournament_name):

    limpar_tela()

    players = ss.get_team_players(team_id, tournament_id)

    team = ss.get_team_by_id(team_id)

    (team_id, team_name, team_country) = team[0]

    print(f"{team_name} players on {tournament_name}:")

    # Calcular largura maxima da coluna
    max_nick = max(len(str(t[0])) for t in players)
    max_role = max(len(str(t[1])) for t in players)
    max_country = max(len(str(t[2])) for t in players)

    # Minimo
    max_nick = max(max_nick, len("Nickname"))
    max_role = max(max_role, len("Role"))
    max_country = max(max_country, len("Country"))

    # Printa header
    print(f"{"#":<4} {'Nickname':<{max_nick}} {"Role":<{max_role}} {"Country":<{max_country}}")
    print("-" * (4 + max_nick + max_country + max_role+ 3))

    # Printa dados

    for i, team in enumerate(players, 1):

        print(f"{i:<4} {team[0]:<{max_nick}} {team[1]:<{max_role}} {team[2]:<{max_country}}")
        
    pausar()

def print_all_players():

    limpar_tela()

    players = ss.get_all_players()

    dados = []

    for i, player in enumerate(players, 1):

        id, nick, country = player

        dados.append((i, id, nick, country))
    
    headers = ['#', 'ID', 'Nickname', 'Country']

    rich_table(dados, headers, 'All Data Base Players')