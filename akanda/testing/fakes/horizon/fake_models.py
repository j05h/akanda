import uuid

from akanda.horizon.akanda.common import PROTOCOL_CHOICES as protocol_choices
from akanda.horizon.akanda.firewall.forms import (
    POLICY_CHOICES as policy_choices)
from akanda.testing.fakes.horizon.fake_data import instances_fake_data


PROTOCOL_CHOICES = dict(protocol_choices)
POLICY_CHOICES = dict(policy_choices)


class Port(object):
    def __init__(self, alias_name, protocol, ports, id=None):
        self.alias_name = alias_name
        self.protocol = protocol
        self.ports = ports
        self.id = id or uuid.uuid4().hex

    @property
    def protocol(self):
        return PROTOCOL_CHOICES[self._protocol]

    @protocol.setter
    def protocol(self, value):
        if isinstance(value, basestring):
            self._protocol = int(value)
        else:
            self._protocol = value

    @property
    def ports(self):
        return '-'.join(map(str, self._ports))

    @ports.setter
    def ports(self, value):
        if isinstance(value, basestring):
            self._ports = map(int, value.split('-'))
            self._ports.sort()
        else:
            self._ports = value

    def raw(self):
        data = self.__dict__.copy()
        for k, v in data.items():
            if k.startswith('_'):
                tmp = data.pop(k)
                data[k[1:]] = tmp
        return data


class Host(object):
    def __init__(self, alias_name, instances, id=None):
        self.alias_name = alias_name
        self._instances = instances
        self.id = id or uuid.uuid4().hex

    @property
    def instances(self):
        instances = [instances_fake_data[instance]['name'] for instance in
                     self._instances]
        instances.sort()
        return ', '.join(instances)

    def raw(self):
        data = self.__dict__.copy()
        for k, v in data.items():
            if k.startswith('_'):
                tmp = data.pop(k)
                data[k[1:]] = tmp
        return data

    def get_instances_list(self):
        return self._instances


class Network(object):
    def __init__(self, alias_name, cidr, id=None):
        self.alias_name = alias_name
        self.cidr = cidr
        self.id = id or uuid.uuid4().hex

    def raw(self):
        return self.__dict__


class FirewallRule(object):
    """
    """

    def __init__(self, policy, source_network_alias, source_protocol,
                 source_public_ports, destination_network_alias,
                 destination_protocol, destination_public_ports, id=None):
        self._policy = policy
        self.source_network_alias = source_network_alias
        self.source_protocol = source_protocol
        self.source_public_ports = source_public_ports
        self.destination_network_alias = destination_network_alias
        self.destination_protocol = destination_protocol
        self.destination_public_ports = destination_public_ports
        self.id = id or uuid.uuid4().hex

        # avoid circular import
        from akanda.testing.fakes.horizon import NetworkAliasManager
        self.network_manager = NetworkAliasManager

    @property
    def policy(self, ):
        return POLICY_CHOICES[self._policy]

    @property
    def source_ip(self):
        network = self.network_manager.get(
            None, self.source_network_alias)
        return network.cidr

    @property
    def destination_ip(self):
        network = self.network_manager.get(
            None, self.destination_network_alias)
        return network.cidr

    @property
    def source_ports(self):
        return "%s %s" % (self.source_protocol,
                          '-'.join(map(str, self.source_public_ports)))

    @property
    def destination_ports(self, ):
        return "%s %s" % (self.destination_protocol,
                          '-'.join(map(str, self.destination_public_ports)))
