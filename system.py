import requests
import json
import os
from datetime import datetime

app_path = os.path.dirname(os.path.abspath(__file__))

def create_file(folder, file_name, content):
    with open(os.path.join(app_path, folder, file_name), "a") as f:
        f.write(content)

def create_folder(folder_name):
    try:
        os.makedirs(os.path.join(app_path, folder_name))
    except Exception as e:
        if "already exist" not in str(e):
            return str(e)
    return "Created"

def sanitize_filename(filename):
    return "".join(c if c.isalnum() else "_" for c in filename)

def create_backup(type, url, cookies=""):
    """
    Connects to your grafana, crawl the data and creates backup files

    Params: 
     - type: string that matches one of the following (datasources, dashboards, alerts)
     - url: string with grafana url (https://www.mygrafana.com)
     - cookies: optional string that matches your session cookies, can be used instead of username and password
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    headers = {'Cookie': cookies}
    print(f"Please wait while we are creating json files for all your {type}...")
    if type == "datasources":
        api_all = "/api/datasources"
    elif type == "dashboards":
        api_all = "/api/search?query=%"
    elif type == "alerts":
        api_all = api_uid = "/api/v1/provisioning/alert-rules/"
    else:
        print("Error: type must be [alerts, dashboards or datasources]")
        exit()
    api_uid = "/api/"+type+"/uid/"
    backup_folder = os.path.join("backup", type, now)
    get_all = requests.get(url+api_all, headers=headers)
    if create_folder(backup_folder) == "Created":
        for get_each in get_all.json():
            if type in ("datasources", "alerts"):
                get_each = requests.get(url+api_uid+get_each["uid"], headers=headers).json()
                file_name = sanitize_filename(get_each["name"]) + ".json"
            elif type == "dashboards":
                dashboard = requests.get(url+api_uid+get_each["uid"], headers=headers).json()["dashboard"]
                file_name = sanitize_filename(dashboard["title"]) + ".json"
                get_each = dashboard
            
            create_file(backup_folder, file_name, json.dumps(get_each))
        print(f"Completed, Check folder [{backup_folder}].")
    else:
        print("Couldn't create the folder, please try again")

def update_all(type, old_value, new_value, url, cookies=""):
    """
    Connects to your grafana, crawl the data and update the values mentioned and save the files

    Params: 
     - type: string that matches one of the following (datasources, dashboards, alerts)
     - old_value: the value you want to change
     - new_value: the new value you want to add
     - url: string with grafana url (https://www.mygrafana.com)
     - cookies: optional string that matches your session cookies, can be used instead of username and password
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    headers = {'Cookie': cookies}
    print(f"Please wait while we update the values mentioned and save updated json files for all your {type}...")
    api_uid = "/api/"+type+"/uid/"
    update_folder = os.path.join("updated", type, now)

    if type == "datasources":
        api_all = "/api/datasources"
    elif type == "dashboards":
        api_all = "/api/search?query=%"
    elif type == "alerts":
        api_all = api_uid = "/api/v1/provisioning/alert-rules/"
    else:
        print("Error: type must be [alerts, dashboards or datasources]")
        exit()
    get_all = requests.get(url+api_all, headers=headers)
    if create_folder(update_folder) == "Created":
        for get_each in get_all.json():
            if type in ("datasources", "alerts"):
                get_each = requests.get(url+api_uid+get_each["uid"], headers=headers).json()
            elif type == "dashboards":
                get_each = requests.get(url+api_uid+get_each["uid"], headers=headers).json()["dashboard"]
            if old_value in json.dumps(get_each):
                get_each = json.dumps(get_each).replace(old_value, new_value)
                create_file(update_folder, json.loads(get_each)["uid"]+".json", get_each)
        print(f"Completed, Check folder [{update_folder}].")
    else:
        print("Couldn't create the folder, please try again")

def search_all(type, value, url, cookies=""):
    """
    Connects to your grafana, crawl the data and search the values mentioned and save the files if exist

    Params: 
     - type: string that matches one of the following (datasources, dashboards, alerts)
     - value: the value you want to find
     - url: string with grafana url (https://www.mygrafana.com)
     - cookies: optional string that matches your session cookies, can be used instead of username and password
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    headers = {'Cookie': cookies}
    print(f"Please wait while we search the value mentioned and save result json files for all your {type}...")
    api_uid = "/api/"+type+"/uid/"
    search_folder = os.path.join("search_results", type, now)
    if type == "datasources":
        api_all = "/api/datasources"
    elif type == "dashboards":
        api_all = "/api/search?query=%"
    elif type == "alerts":
        api_all = api_uid = "/api/v1/provisioning/alert-rules/"
    else:
        print("Error: type must be [alerts, dashboards or datasources]")
        exit()
    get_all = requests.get(url+api_all, headers=headers)
    if create_folder(search_folder) == "Created":
        for get_each in get_all.json():
            if type in ("datasources", "alerts"):
                get_each = requests.get(url+api_uid+get_each["uid"], headers=headers).json()
            elif type == "dashboards":
                get_each = requests.get(url+api_uid+get_each["uid"], headers=headers).json()["dashboard"]
            if value in json.dumps(get_each):
                create_file(search_folder, get_each["uid"]+".json", json.dumps(get_each))
        print(f"Completed, Check folder [{search_folder}].")
    else:
        print("Couldn't create the folder, please try again")

def import_all_datasources(url, cookie=""):
    """
    TO DO: import all the datasources json files to the url mentioned
    """

def import_all_dashboards(url, cookie=""):
    """
    TO DO: import all the dashboards json files to the url mentioned
    """

def import_all_alerts(url, cookie=""):
    """
    TO DO: import all the alerts json files to the url mentioned
    """
