import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import services.stats_service as ss

import controllers.prints as prints

# ============================================
# MENU PRINCIPAL (main.py)
# Caminho: [Início]
# ============================================
def exibir_menu():

    print("1. Tournaments stats")
    print("2. List all Data Base players")
    print("3. List all Data Base teams")
    print("4. List all Data Base maps")
    print("0. Exit")

# ============================================
# MENU DE SELEÇÃO DE TORNEIO
# Caminho: 1
# ============================================
def exibir_tournament_menu():

    prints.limpar_tela()

    tournaments = ss.get_tournament()

    print("Select a tournament:")

    num = 1

    for torneio in tournaments:

        print(f"{num}. {torneio[1]}")

        num += 1

    print("0. Back")

    print()

    return num - 1

# ============================================
# MENU DE ESTATÍSTICAS DO TORNEIO
# Caminho: 1 → [torneio]
# ============================================
def exibir_menu_stats():

    print("Avaible Stats:")
    print()

    print("1. Tournaments teams")
    print("2. List players from a team")
    print("3. Get player's stats")
    print("4. Get player's best map")
    print("5. Player average rating by map")
    print("6. Match Scoreboard")
    print("7. Team best maps")
    print("8. List players by rating")
    print("9. Maps T/CT rates")
    print("10. Team pistol perfomance")
    print("0. Back")

# ============================================
# MENU DE SELEÇÃO DE TIME (para ver jogadores)
# Caminho: 1 → [torneio] → 4
# ============================================                
def player_best_map_menu(torneio_id, torneio_name):  

    while True:

        prints.limpar_tela()

        print("Get player's best map:")

        print()

        # Opções do menu 1 → [torneio] → 4
        print("1. Type player ID")
        print("2. Select player")
        print("0. Back")

        print()

        option = input("Select an option: ")

        print()

        # Opção 1→ [torneio] → 4 → 0 (Voltar)
        if option == "0":

            break

        # Opção 1 → [torneio] → 4 → 1 (digitar ID do jogador)
        elif option == "1":

            while True:

                prints.limpar_tela()

                player_id = input('Type a player id or "EXIT" to return: ')

                players = ss.get_all_players(torneio_id)

                valid_player_id = False

                for player in players:

                    if player[0] == player_id:

                        valid_player_id = True
                
                if valid_player_id:

                    break

                elif player_id == "EXIT":

                    break

                else:
                    prints.limpar_tela()

                    print("Invalid player_id!")
                    print()
                
                    print("0. To return")
                    print("Press Enter to try again...")
                    print()
                    x = input("Select an option: ")
                    print()

                    if x == "0": break

            if valid_player_id:

                prints.print_player_best_map(player_id, torneio_id, torneio_name)

            elif player_id == "EXIT":

                prints.pausar()

            else:

                print("Invalid")

        # Opção 1 → [torneio] → 3 → 2 (selecionar jogador)

        elif option == "2":

            while True:

                prints.limpar_tela()

                players = ss.get_all_players(torneio_id)

                # Menu de seleção de time: 1 → [torneio] → 2 → 2
                print(f"Select a {torneio_name} player:")

                for i, player in enumerate(players, 1):

                    print(f"{i}. {player[1]}")

                print("0. Back")

                print()

                option = input("Select a Player: ")

                print()

                if option.isdigit() and int(option) >= 1 and int(option) <= i:

                    prints.print_player_best_map(players[int(option) - 1][0], torneio_id, torneio_name)
                        
                elif option == "0":

                    break

                else:

                    print("Invalid option!")

                    prints.pausar()

        else:

            prints.limpar_tela()

            print("Invalid option!")

            prints.pausar()

    
# ============================================
# MENU DE SELEÇÃO DE JOGADORES (para ver stats)
# Caminho: 1 → [torneio] → 3
# ============================================
def player_stats_menu(torneio_id, torneio_name):

    while True:

        prints.limpar_tela()

        # Opções do menu 1 → [torneio] → 3
        print("1. Type player ID")
        print("2. Select player")
        print("0. Back")

        print()

        option = input("Select an option: ")

        print()

        # Opção 1→ [torneio] → 3 → 0 (Voltar)
        if option == "0":

            break

        # Opção 1 → [torneio] → 3 → 1 (digitar ID do jogador)
        elif option == "1":

            while True:

                prints.limpar_tela()

                player_id = input('Type a player id or "EXIT" to return: ')

                players = ss.get_all_players(torneio_id)

                valid_player_id = False

                for player in players:

                    if player[0] == player_id:

                        valid_player_id = True
                
                if valid_player_id:

                    break

                elif player_id == "EXIT":

                    break

                else:
                    prints.limpar_tela()

                    print("Invalid player_id!")
                    print()
                
                    print("0. To return")
                    print("Press Enter to try again...")
                    print()
                    x = input("Select an option: ")
                    print()

                    if x == "0": break

            if valid_player_id:

                prints.print_player_stats(player_id, torneio_id, torneio_name)

            elif player_id == "EXIT":

                prints.pausar()

            else:

                print("Invalid")

        # Opção 1 → [torneio] → 3 → 2 (selecionar jogador)

        elif option == "2":

            while True:

                prints.limpar_tela()

                players = ss.get_all_players(torneio_id)

                # Menu de seleção de time: 1 → [torneio] → 2 → 2
                print(f"Select a {torneio_name} player:")

                for i, player in enumerate(players, 1):

                    print(f"{i}. {player[1]}")

                print("0. Back")

                print()

                option = input("Select a Player: ")

                print()

                if option.isdigit() and int(option) >= 1 and int(option) <= i:

                    prints.print_player_stats(players[int(option) - 1][0], torneio_id, torneio_name)
                        
                elif option == "0":

                    break

                else:

                    print("Invalid option!")

                    prints.pausar()

        else:

            prints.limpar_tela()


            print("Invalid option!")

            prints.pausar()

# ============================================
# MENU DE SELEÇÃO DE TIME (para ver jogadores)
# Caminho: 1 → [torneio] → 2
# ============================================
def list_players_from_team_menu(torneio_id, torneio_name):

    while True:

        prints.limpar_tela()

        # Opções do menu 1 → [torneio] → 2

        print("List players from a team: ")

        print("1. Type team ID")
        print("2. Select team")
        print("0. Back")

        print()

        option = input("Select an option: ")

        print()

        if option == "0":

            break

        # Opção 1 → [torneio] → 2 → 1 (digitar ID do time)
        elif option == "1":

            prints.limpar_tela()

            while True:

                team_id = input('Choose a team id or "EXIT" to return: ')

                teams = ss.get_tournament_teams(torneio_id)

                valid_team_id = False

                for team in teams:

                    if team[0] == team_id:

                        valid_team_id = True
                
                if valid_team_id:

                    break

                elif team_id == "EXIT":

                    break

                else:

                    prints.limpar_tela()
                    print("Invalid team_id!")
                    print()
                    
                    print("0. To return")
                    print("Press Enter to try again...")

                    print()
                    x = input("Select an option: ")
                    print()

                    if x == "0": break

            if valid_team_id:

                prints.list_players_from_team(team_id, torneio_id, torneio_name)

            elif team_id == "EXIT":

                prints.pausar()

            else:

                print("Invalid")
        
        # Opção 1 → [torneio] → 2 → 2 (selecionar time da lista)
        elif option == "2":

            while True:

                prints.limpar_tela()

                teams = ss.get_tournament_teams(torneio_id)

                # Menu de seleção de time: 1 → [torneio] → 2 → 2
                print(f"Select a {torneio_name} team:")

                for i, team in enumerate(teams, 1):

                    print(f"{i}. {team[1]}")

                print("0. Back")

                print()

                option = input("Select a team: ")

                print()

                if option.isdigit() and int(option) >= 1 and int(option) <= i:

                    prints.list_players_from_team(teams[int(option) - 1][0], torneio_id, torneio_name)

                elif option == "0":

                    break

                else:

                    print("Invalid option!")

                    prints.pausar()

        else:

            prints.limpar_tela()


            print("Invalid option!")

            prints.pausar()

# ============================================
# EXIBE TIMES DO TORNEIO
# Caminho: 1 → [torneio] → 1
# ============================================
def tournament_teams(torneio_id=None):

    prints.limpar_tela()

    teams = ss.get_tournament_teams(torneio_id)

    dados = []

    for i, team in enumerate(teams, 1):

        id, name, country = team

        dados.append((i, id, name, country))

    headers = ['#', 'ID', 'Name', 'Country']

    prints.rich_table(dados,headers, 'All Data Base Teams')

# ============================================
# CONTROLADOR DO MENU DE ESTATÍSTICAS
# Caminho: 1 → [torneio] → (opções)
# ============================================
def opcoes_stats(torneio_id, torneio_name):

    while True:

        prints.limpar_tela()

        exibir_menu_stats()

        option = input("Choose an option: ")

        print()

        if option == "0":

            break

        # Opção 1 → [torneio] → 1 (ver times)
        elif option == "1":

            print(f"Teams on {torneio_name}:")

            tournament_teams(torneio_id)

            prints.pausar()

        # Opção 1 → [torneio] → 2 (ver jogadores de um time)
        elif option == "2":

            list_players_from_team_menu(torneio_id, torneio_name)

        # Opção 1 → [torneio] → 2 (ver jogadores de um time)
        elif option == "3":

            player_stats_menu(torneio_id, torneio_name)

        elif option == "4":

            player_best_map_menu(torneio_id, torneio_name)

        else:
            
            prints.limpar_tela()

            print("Invalid option!")

            prints.pausar()


# ============================================
# CONTROLADOR DO MENU DE TORNEIOS
# Caminho: 1 → (seleção de torneio)
# ============================================
def tournament_menu():

    while True:

        tamanho = exibir_tournament_menu()

        tour_options = input("Select an option: ")

        print()

        if tour_options == "0": break

        elif tour_options.isdigit() and int(tour_options) >= 1 and int(tour_options) <= tamanho:

            torneios = ss.get_tournament()
            
            torneio_id = torneios[int(tour_options) - 1][0]

            torneio_name = torneios[int(tour_options) - 1][1]

            # Vai para o menu de estatísticas do torneio selecionado
            opcoes_stats(torneio_id, torneio_name)

        else:

            prints.limpar_tela()

            print("Invalid option!")

            prints.pausar()