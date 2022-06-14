from typing import Dict


class RunningInstances(object):
    def __init__(self, instances: Dict[str, int]):
        self.instances = instances

    def add_running(self, pid: int, connection_name: str):
        self.instances[connection_name] = pid

    def get_running(self, connection_name: str) -> int:
        return self.instances[connection_name]

    def get_all_running(self,) -> Dict[str, int]:
        return self.instances

    def remove_running(self, connection_name: str):
        self.instances.pop(connection_name)
