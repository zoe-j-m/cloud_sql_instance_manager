from unittest import mock

from _pytest.python_api import raises

from cloud_sql.config import default_configuration, Configuration, PathNotFoundError


class TestConfig:
    proxy_path = "/new/path"

    @mock.patch("cloud_sql.config.shutil.which")
    def test_default_config(self, which_mock):
        which_mock.return_value = self.proxy_path
        assert default_configuration().cloud_sql_path == self.proxy_path

    @mock.patch("cloud_sql.config.os.path.exists")
    def test_new_path(self, exists_mock):
        config = Configuration("/original/path")
        exists_mock.return_value = True
        config.new_path(self.proxy_path)
        assert config.cloud_sql_path == self.proxy_path

        exists_mock.return_value = False
        with raises(PathNotFoundError):
            config.new_path("/bad/path")
