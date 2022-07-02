from _pytest.python_api import raises
from psutil import NoSuchProcess

from cloud_sql.cloud_sql_proxy import run_cloud_sql_proxy, check_if_proxy_is_running, stop_cloud_sql_proxy
from cloud_sql.gcp import obtain_instances
from cloud_sql.instances import Instance, Site, InstanceNotFoundError, DuplicateInstanceError
from tests import test_fixtures

from unittest import mock
from unittest.mock import patch, mock_open, MagicMock


class TestGcp:
    proxy_path = '/a/path'
    test_response = {
        'items': [
            {
                'name': test_fixtures.name1,
                'region': test_fixtures.region1,
                'project': test_fixtures.project1,
                'connectionName': test_fixtures.connection_name1,
                'instanceType': 'CLOUD_SQL_INSTANCE'
            },
            {
                'name': 'wrong',
                'region': 'wrong',
                'project': test_fixtures.project1,
                'connectionName': 'wrong',
                'instanceType': 'OTHER'
            },
        ]
    }

    @mock.patch('cloud_sql.gcp.discovery.build')
    @mock.patch('cloud_sql.gcp.google.auth.default')
    def test_obtain_instances(self, mock_auth,mock_discovery):
        service = MagicMock()
        instances = MagicMock()
        request = MagicMock()
        mock_auth.return_value = 'creds1', test_fixtures.project1
        mock_discovery.return_value = service
        service.instances.return_value = instances
        instances.list.return_value = request
        request.execute.return_value = self.test_response
        site = Site({})
        obtain_instances(site, None)
        assert len(site.instances) == 1
        assert 'database-postgres' in site.nicknames

        instances.list.reset_mock()
        obtain_instances(site, 'override')
        instances.list.assert_called_once_with(project='override')


