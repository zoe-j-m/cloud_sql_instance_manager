import sys
from typing import Dict

import gcp
from cloudsqlproxy import run_cloud_sql_proxy, stop_cloud_sql_proxy
from commandline import get_parameters
from config import Configuration
from instances import Site
from persistence import save_site, load_site, load_config, save_config, load_running, save_running
from running_instances import RunningInstances


def execute_command(parameters: Dict[str, str], config: Configuration, site: Site, running_instances: RunningInstances):
    command = parameters['command']
    match command:
        case 'list':
            site.print_list()
        case 'list-running':
            running = running_instances.get_all_running()
            for connection_name in running.keys():
                instance = site.instances[connection_name]
                instance.print(running[connection_name])
            if len(running) == 0:
                print("No running instances")
        case 'start':
            instance = site.get_instance_by_nick_name(parameters['name'], parameters['project'])
            if instance:
                pid = run_cloud_sql_proxy(config.cloud_sql_path, instance.connection_name, instance.port, instance.iam)
                running_instances.add_running(pid, instance.connection_name)
                print(f"Started {instance.name} on port {instance.port}")
        case 'stop':
            instance = site.get_instance_by_nick_name(parameters['name'], parameters['project'])
            if instance:
                pid = running_instances.get_running(instance.connection_name)
                if pid:
                    if stop_cloud_sql_proxy(pid, instance.connection_name):
                        print(f"Stopped {instance.name} on port {instance.port}")
                    else:
                        print("Could not locate process to stop, it has been removed from the running list")
                    running_instances.remove_running(instance.connection_name)
                print(f"Stopped {instance.name} on port {instance.port}")
        case 'import':
            gcp.obtain_instances(site)
            print(f"Imported {len(site.instances)} instances.")
        case _:
            print("Specify a command or ask for help with --help")


if __name__ == '__main__':
    app_config = load_config()
    app_parameters = get_parameters()
    site_info = load_site()
    running = load_running()
    execute_command(app_parameters, app_config, site_info, running)
    save_running(running)
    save_site(site_info)
    save_config(app_config)
    sys.exit()
