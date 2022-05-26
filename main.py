import argparse
import json

from google.api.http_pb2 import Http
from googleapiclient import discovery
import google.auth

from instances import Instance, Site
from persistence import save_site, load_site


def get_credentials_and_project():
    return google.auth.default()


def get_google_service(credentials):
    return discovery.build('sqladmin', 'v1beta4')


def obtain_instances() -> Site:
    # Use a breakpoint in the code line below to debug your script.
    # creds, project = google.auth.default()
    #
    # # creds.valid is False, and creds.token is None
    # # Need to refresh credentials to populate those
    #
    # auth_req = google.auth.transport.requests.Request()
    # creds.refresh(auth_req)
    # Construct the service object for the interacting with the Cloud SQL Admin API.

    credentials, project = get_credentials_and_project()
    service = get_google_service(credentials)
    req = service.instances().list(project=project)
    resp = req.execute()
    instances = [Instance(item.get("name"), item.get("region"), item.get("project"), item.get("connectionName"))
                 for item in resp.get("items") if item.get("instanceType") == 'CLOUD_SQL_INSTANCE']
    site = Site({})
    for instance in instances:
        site.update(instance)

    save_site(site)
    return site


def parse_arguments():
    parser = argparse.ArgumentParser(description="Cloud SQL Instance Manager",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--archive", action="store_true", help="archive mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
    parser.add_argument("-B", "--block-size", help="checksum blocksize")
    parser.add_argument("--ignore-existing", action="store_true", help="skip files that exist")
    parser.add_argument("--exclude", help="files to exclude")
    parser.add_argument("src", help="Source location")
    parser.add_argument("dest", help="Destination location")
    args = parser.parse_args()
    config = vars(args)
    print(config)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
