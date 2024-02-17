import requests
import system

def main_menu():
    print("\nWhat you want to do today ?\n")
    options = ["Backup all datasources", 
               "Backup all dashboards",
               "Backup all alert-rules",
               "Cahnge a value in all datasources",
               "Change a value in all dashboards",
               "Change a value in all alert-rules", 
               "Import all datasources",
               "Import all dashboards",
               "Import all alert-rules",
               "Search a value in all datasources",
               "Search a value in all dashboards",
               "Search a value in all dalert-rules",]
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
            if choice in (1,2,3): # backup all
                if choice == 1:
                    type = "datasources"
                elif choice == 2:
                    type = "dashboards"
                elif choice == 3:
                    type = "alerts"
                system.create_backup(type, url)
            
            elif choice in (4,5,6): # update all
                if choice == 4:
                    type = "datasources"
                elif choice == 5:
                    type = "dashboards"
                elif choice == 6:
                    type = "alerts"
                old_value = input("\nWrite the value you want to change: ")
                new_value = input("Write the new value you want to add: ")
                system.update_all(type, old_value, new_value, url)
            
            elif choice in (7,8,9) : # import all 
                print("import all")
            
            elif choice in (10,11,12): # search all
                if choice == 10:
                    type = "datasources"
                elif choice == 11:
                    type = "dashboards"
                elif choice == 12:
                    type = "alerts"
                value = input("Write the value you want to find: ")
                system.search_all(type, value, url)

            return_main_menu(url)
        else:
            print("\nCheck your username and password and try again.")
            start_grafana_sync()
    except:
        print("\nCheck the url and try again.")
        start_grafana_sync()
    

print("\nWelcome to Grafana Sync")
print("-----------------------")

can_start = True
for folder in ("backup",'backup\dashboards','backup\datasources','backup\\alerts',
               "updated",'updated\dashboards','updated\datasources','updated\\alerts',
               "search_results",'search_results\dashboards','search_results\datasources','search_results\\alerts'):
    create_result = system.create_folder(folder)
    if create_result != "Created":
        print(folder,create_result)
        can_start = False
if can_start:
    start_grafana_sync()
