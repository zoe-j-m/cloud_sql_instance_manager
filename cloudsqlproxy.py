import signal
import subprocess

import pexpect as pexpect
from pexpect import popen_spawn


def run_cloud_sql_proxy(cloud_sql_proxy_path: str, connection_name: str, port: int, enable_iam: bool):
    instance_flag = '-instances={}=tcp:{}'.format(
        connection_name, port)

    if cloud_sql_proxy_path is None:
        assert cloud_sql_proxy_path, 'Could not find cloud_sql_proxy path'

    if enable_iam:
        command = [cloud_sql_proxy_path, '-enable_iam_login', instance_flag]
    else:
        command = [cloud_sql_proxy_path, instance_flag]

    process = subprocess.Popen(command, start_new_session=True)

    print(process.pid)

