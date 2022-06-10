import signal
import subprocess

import pexpect as pexpect
import psutil as psutil
from pexpect import popen_spawn


def run_cloud_sql_proxy(cloud_sql_proxy_path: str, connection_name: str, port: int, enable_iam: bool) -> int:
    instance_description = '-instances={}=tcp:{}'.format(
        connection_name, port)

    if cloud_sql_proxy_path is None:
        assert cloud_sql_proxy_path, 'Could not find cloud_sql_proxy path'

    if enable_iam:
        command = [cloud_sql_proxy_path, '-enable_iam_login', instance_description]
    else:
        command = [cloud_sql_proxy_path, instance_description]

    process = subprocess.Popen(command, start_new_session=True)

    return process.pid


def stop_cloud_sql_proxy(pid : int, name: str) -> bool:
    process = psutil.Process(pid)
    if process:
        if name in process.name():
            process.kill()
            return True
    else:
        return False


