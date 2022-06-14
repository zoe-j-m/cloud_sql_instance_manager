import json
from typing import Dict, Optional

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

    def print(self, pid: Optional[int]):
        if not pid:
            print(
                f'Project: {self.project}, Nick: {self.shortname}, Port {self.port or "N/A"}, Name: {self.name}, Region: {self.region}, IAM Enabled: {self.iam}')
        else:
            print(
                f'Pid: {pid}, Project: {self.project}, Nick: {self.shortname}, Port {self.port or "N/A"}, Name: {self.name}, Region: {self.region}, IAM Enabled: {self.iam}')

    def set_iam(self, iam: bool):
        self.iam = iam


class Site(object):
    def __init__(self, instances: Dict[str, Instance]):
        self.nicknames = {}
        self.instances = instances
        self.nextPort = 0
        ports = [instance.port for instance in instances.values() if instance.port is not None]
        ports.insert(0, 5433)
        self.nextPort = max(ports) + 1

    def __repr__(self):
        return jsonpickle.encode(self)

    def set_up_nicknames(self):
        self.nicknames = {}
        for instance in self.instances.values():
            if instance.shortname in self.nicknames.keys():
                if instance not in self.nicknames[instance.shortname]:
                    self.nicknames[instance.shortname].append(instance)
            else:
                self.nicknames[instance.shortname] = [instance]

    def update(self, instance: Instance):
        if instance.connection_name not in self.instances.keys():
            if instance.port is None:
                instance.port = self.nextPort
                self.nextPort += 1
            self.instances[instance.connection_name] = instance

    def print_list(self):
        for instance in self.instances.values():
            instance.print(None)

    def get_instance_by_nick_name(self, name, project) -> Optional[Instance]:

        if name not in self.nicknames:
            print("No instance found with that nickname")
            return None

        possibles = self.nicknames[name]

        if project:
            possibles = [possible for possible in possibles if possible.project == project]

        if not possibles:
            print("No instance found with that nickname for that project")
            return None
        else:
            if len(possibles) == 1:
                return possibles[0]
            else:
                print("More than one instance with that nick - specify a project, or change the nickname")
                return None
