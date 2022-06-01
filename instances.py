import json
from typing import Dict

import jsonpickle


class Instance(object):
    def __init__(self, name: str, region: str, project: str, connection_name: str):
        self.port = None
        self.iam = False
        self.name = name
        self.shortname = name[:name.find("-instance-")]
        self.region = region
        self.project = project
        self.connection_name = connection_name

    def __repr__(self):
        return json.dumps(self.__dict__)

    def assign_port(self, port: int):
        self.port = port

    def print(self):
        print(f'Project: {self.project}, Nick: {self.shortname}, Port {self.port or "N/A"}, Name: {self.name}, Region: {self.region}, IAM Enabled: {self.iam}')

    def set_iam(self, iam : bool):
        self.iam = True



class Site(object):
    def __init__(self, instances: Dict[str, Instance]):
        self.instances = instances
        ports = [instance.port for instance in instances if instance.port is not None]
        ports.insert(0, 5433)
        self.nextPort = max(ports) + 1

    def __repr__(self):
        return jsonpickle.encode(self)

    def update(self, instance : Instance):
        if instance.connection_name not in self.instances.keys():
            if instance.port is None:
                instance.port = self.nextPort
                self.nextPort += 1
            self.instances[instance.connection_name] = instance

    def print_list(self):
        for instance in self.instances.values():
            instance.print()

    def get_instance_by_name(self, name, project):
        return self.instances[name]
