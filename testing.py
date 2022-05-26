import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Cloud SQL Instance Manager",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("command", choices=['start', 'stop', 'add', 'update', 'import', 'export'],help="Command")
    start_parser = argparse.ArgumentParser(parents =[parser],
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args()
    config = vars(args)
    print(config)