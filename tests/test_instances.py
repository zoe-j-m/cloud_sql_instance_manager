from _pytest.python_api import raises

from cloud_sql.instances import Instance, Site, InstanceNotFoundError, DuplicateInstanceError


class TestInstance:
    name = 'database-postgres-instance-1234'
    project = 'project-1'
    region = 'region-1'
    connection_name = f'{project}:{region}:{name}'
    port = 5111

    def test_default_shortname(self):
        instance = Instance(self.name, self.region, self.project, self.connection_name)
        assert instance.shortname == 'database-postgres'

    def test_assign_port(self):
        instance = Instance(self.name, self.region, self.project, self.connection_name)
        instance.assign_port(self.port)
        assert instance.port == 5111

    def test_print(self):
        instance = Instance(self.name, self.region, self.project, self.connection_name)
        instance.assign_port(self.port)
        no_pid = instance.print(None)
        pid = instance.print(4512)
        assert no_pid == 'Project: project-1, Nick: database-postgres, Port 5111, Name: database-postgres-instance-1234, Region: region-1, IAM Enabled: False'
        assert pid == f'Pid: 4512, {no_pid}'

    def test_set_iam(self):
        instance = Instance(self.name, self.region, self.project, self.connection_name)
        assert instance.iam is False
        instance.set_iam(True)
        assert instance.iam is True

class TestSite:

    name1 = 'database-postgres-instance-1234'
    project1 = 'project-1'
    region1 = 'region-1'
    port1 = 5511
    instance1 = Instance(name1, region1, project1, f'{project1}:{region1}:{name1}')
    instance1.port = port1
    name2 = 'database-postgres-instance-1235'
    project2 = 'project-2'
    region2 = 'region-2'
    instance2 = Instance(name2, region2, project2, f'{project2}:{region2}:{name2}')
    instance2.port = 5512

    def test_setup_nicknames(self):
        site = Site({self.name1: self.instance1, self.name2: self.instance2})
        site.set_up_nicknames()
        assert site.nicknames['database-postgres'] == [self.instance1, self.instance2]

    def test_update(self):
        site = Site({self.name1: self.instance1, self.name2: self.instance2})
        name3 = 'db-pg-instance-3'
        instance = Instance(name3, self.region1, self.project1, f'{self.project1}:{self.region1}:{name3}')
        site.update(instance)
        assert instance.port == 5513

    def test_print_list(self):
        site = Site({self.name1: self.instance1, self.name2: self.instance2})
        values = site.print_list(self.project1)
        assert len(values) == 1
        assert values[0] == 'Project: project-1, Nick: database-postgres, Port 5511, Name: database-postgres-instance-1234, Region: region-1, IAM Enabled: False'

    def test_get_instance_by_nickname(self):
        site = Site({self.name1: self.instance1, self.name2: self.instance2})
        site.set_up_nicknames()
        with raises(InstanceNotFoundError):
            site.get_instance_by_nick_name('fish', None)

        with_nick = site.get_instance_by_nick_name('database-postgres', self.project1)
        assert with_nick == self.instance1

        name3 = 'db-pg-instance-3'
        instance = Instance(name3, self.region1, self.project1, f'{self.project1}:{self.region1}:{name3}')
        site.update(instance)
        site.set_up_nicknames()
        with raises(InstanceNotFoundError):
            site.get_instance_by_nick_name(instance.shortname, self.project2)

        with raises(DuplicateInstanceError):
            site.get_instance_by_nick_name('database-postgres', None)

