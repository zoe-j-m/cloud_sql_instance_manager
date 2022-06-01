import argparse
from typing import Dict


def get_parameters() -> Dict[str, str]:
    parser = argparse.ArgumentParser(description="Cloud SQL Instance Manager",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    parser_list = subparsers.add_parser('list', help='list current instances')

    parser_start = subparsers.add_parser('start', help='start instance')
    parser_start.add_argument("name", help="instance name or nickname")
    parser_start.add_argument("-p", '--project', help='project name')

    parser_stop = subparsers.add_parser('stop', help='stop a running instance')
    parser_stop.add_argument("name", help="instance name or nickname")
    parser_stop.add_argument("-p", '--project', help='project name')

    parser_add = subparsers.add_parser('add', help='add a new instance')
    parser_add.add_argument("connection name", help="long connection name from gcp")
    parser_add.add_argument("-n", '--nick', help='set nickname')
#    parser_add.add_argument("-i", '--iam', const=True, default=False,help='run with enable iam login')

    args = vars(parser.parse_args())
    print(args)
    return args
