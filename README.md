# Grafana Sync
This tool will help you to do easy backup to all your datasources and dashboards and will allow you to search and update all dashboards with few clicks


Features:

its a wrapper over grafana apis, it will allow you to do the following easily:
- backup all datasources
- backup all dashboards
- backup all alert-rules
- search specific values (like datasource or job name) in all datasources
- search specific values (like datasource or job name) in all dashboards
- search specific values (like datasource or job name) in all alert-rules
- update specific values (like datasource or job name) in all datasources
- update specific values (like datasource or job name) in all dashboards
- update specific values (like datasource or job name) in all alert-rules

Coming Soon:
- import all datasources to new grafana
- import all dashboards to new grafana
- import all alert-rules to new grafana

and all that with just few clicks, no need to search, write or memorize any apis 

NOTE: old alerts are not included only alert-rules (provisioned alerts) are included



To run the app use the following command
 
    `python start.py`

    
and make sure to install the following libraries 
- requests==2.28.1
