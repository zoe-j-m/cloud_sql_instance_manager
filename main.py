import sys
from typing import Dict

import gcp
from cloudsqlproxy import run_cloud_sql_proxy
from commandline import get_parameters
from config import Configuration
from instances import Instance, Site
from persistence import save_site, load_site, load_config, save_config


def execute_command(parameters: Dict[str,str], config : Configuration, site : Site):
    command = parameters['command']
    match command:
        case 'list':
            site.print_list()
        case 'start':
            instance = site.get_instance_by_name(parameters['name'], parameters['project'])
            if instance:
                run_cloud_sql_proxy(config.cloud_sql_path, instance.connection_name, instance.port, instance.iam)
                print(f"Started {instance.name} on port {instance.port}")
        case 'import':
            gcp.obtain_instances(site)
            print(f"Imported {len(site.instances)} instances.")
        case _:
            print("Specify a command or ask for help with --help")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config = load_config()
    print(sys.argv)
    parameters = get_parameters()
    print(parameters)
    site = load_site()
    execute_command(parameters, config, site)
    save_site(site)
    save_config(config)
    sys.exit()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
