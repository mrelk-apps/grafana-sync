import requests
import json
import os
from datetime import datetime


app_path = os.path.dirname(os.path.abspath(__file__))

def create_backup(type, url, cookies=""):
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    headers = {'Cookie': cookies}
        
    print("Please wait while we are creating json files for all your "+type+"...")
    if type == "datasources":
        api_all =  "/api/datasources"
        api_uid =  "/api/datasources/uid/"
        backup_folder = "backup\datasources\\"+str(now)+"\\"
    elif type == "dashboards":
        api_all =  "/api/search?query=%"
        api_uid =  "/api/dashboards/uid/"
        backup_folder = "backup\dashboards\\"+str(now)+"\\"
        
    get_all = requests.get(url+api_all, headers=headers)
    if create_folder(backup_folder) == "Created":
        for get_each in get_all.json():
            if type == "datasources":
                get_each =  requests.get(url+api_uid+get_each["uid"], headers=headers).json()
            elif type == "dashboards":
                get_each =  requests.get(url+api_uid+get_each["uid"], headers=headers).json()["dashboard"]
            create_file(backup_folder, get_each["uid"]+"_v"+str(get_each["version"])+".json", json.dumps(get_each))
        print("Completed, Check folder ["+backup_folder+"].")
    else:
        print("Coudlnt create the folder, please try again")



def create_folder(folder_name):
    try:
        os.mkdir(app_path+'\\'+folder_name)
    except Exception as e:
        if "already exist" not in str(e):
            return str(e)
    return "Created"

def create_file(folder, file_name, content):
    f = open(app_path+"\\"+folder+"\\"+file_name, "a")
    f.write(content)
    f.close()


def update_all_dashboards(url, cookie=""):
    """
    TO DO: update all the dashboards then export them as valid json files
    """

def import_all_datasources(url, cookie=""):
    """
    TO DO: import all the datasoruces json files to the url mentioned
    """

def import_all_dashboards(url, cookie=""):
    """
    TO DO: import all the dashboards json files to the url mentioned
    """

def search_all_dashboards(url, cookie=""):
    """
    TO DO: search all the dashboards from the api directly
    """