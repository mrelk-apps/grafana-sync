import requests
import system

def main_menu():
    print("\nWhat you want to do today ?\n")
    options = ["Backup all datasources", 
               "Backup all dashboards", 
               "Import all datasources",
               "Import all dashboards",
               "Change a value in all dashboards",
               "Search a value in all dashboards"]
    for idx, element in enumerate(options):
        print("{}- {}".format(idx + 1, element))

    i = input("\nEnter number: ")
    
    try: 
        if int(i) in range(1,len(options)+1):
            return int(i)
        else:
            print("wrong entry, please choose number from the menu!\n")
            main_menu()
    except:
        print("you should choose a number, stop writing gibberish\n")
        main_menu()


def return_main_menu(url):
    print("\nDo you want to do anything else?")
    i = input("Yes[Y] or No[N]: ").lower()
    if i in ("Yes".lower(), "Y".lower()):
        connect_new_grafana(url)
    elif i in ("No".lower(), "N".lower()):
        print("\nBye bye!\n")
    else:
        print(i)
        print("\nstop writing gibberish, choose yes or no!")
        return_main_menu(url)


def connect_new_grafana(url):
    print("\nUsing same grafana connection?")
    i = input("Yes[Y] or No[N]: ").lower()
    if i in ("Yes".lower(), "Y".lower()):
        start_grafana_sync(url)
    elif i in ("No".lower(), "N".lower()):
        start_grafana_sync()
    else:
        print(i)
        print("\nstop writing gibberish, choose yes or no!")
        connect_new_grafana(url)    


def build_url():
    print("\nConnect to the grafana you want to take action on...")
    print("URL Format: https://grafana-server:port\n")
    inp_url = input("Enter URL: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    scheme = inp_url.split('://')[0]
    url = inp_url.split('://')[1]
    connection_url = scheme+"://"+username+":"+password+"@"+url
    return connection_url


def start_grafana_sync(url=""):
    if url == "":
        url = build_url()
    try:
        response = requests.get(url+"/api/org")
        if response.status_code == 200:
            print("\nGood we are CONNECTED!")
            choice = main_menu()
            if choice == 1: # backup all datasources
                system.create_backup("datasources", url)
                return_main_menu(url)
            elif choice == 2: # backup all dashboards
                system.create_backup("dashboards", url)
                return_main_menu(url)
            elif choice == 3: # import all datasources
                print("choice 3")
            elif choice == 4: # import all dashboards
                print("choice 4")
            elif choice == 5: # change values of all dashboards
                print("choice 5")
            elif choice == 6: # search values of all dashboards
                print("choice 6")
        else:
            print("\nCheck your username and password and try again.")
            start_grafana_sync()
    except:
        print("\nCheck the url and try again.")
        start_grafana_sync()
    

print("\nWelcome to Grafana Sync")
print("-----------------------")

can_start = True
for folder in ("backup",'backup\dashboards','backup\datasources'):
    create_result = system.create_folder(folder)
    if create_result != "Created":
        print(folder,create_result)
        can_start = False
if can_start:
    start_grafana_sync()
