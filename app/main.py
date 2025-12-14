import services.stats_service as ss
import controllers.menu as menu
import controllers.prints as prints

def main():

    while True:

        prints.limpar_tela()

        print("Welcome to Counter Strike Major's Stats")

        menu.exibir_menu()

        print()

        option = input("Type an option: ")

        print()

        if option == "1":

            menu.tournament_menu()
        
        elif option == "2":

            prints.print_all_players()
            
            print()

            prints.pausar()

            print()

        elif option == "3":

            menu.tournament_teams()

            prints.pausar()

            print()


        elif option == "4":

            prints.limpar_tela()

            maps = ss.get_all_maps()

            dados = []

            print("All maps in the Data Base: ")

            for i, map in enumerate(maps):

                dados.append((i, map[0]))

            headers = ["#", "Map Name"]

            prints.rich_table(dados, headers, 'All Data Base Maps')

            prints.pausar()

            

        elif option == "0":

            prints.limpar_tela()

            print("Bye bye!!!")

            break
        
        else:

            prints.limpar_tela()

            print("Invalid option!")

            prints.pausar()


if __name__ == "__main__":

    main()