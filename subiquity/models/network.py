# Copyright 2015 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from subiquity.model import ModelPolicy


log = logging.getLogger('subiquity.models.network')


class SimpleInterface:
    """ A simple interface class to encapsulate network information for
    particular interface
    """
    def __init__(self, attrs):
        self.attrs = attrs
        for i in self.attrs.keys():
            if self.attrs[i] is None:
                setattr(self, i, "Unknown")
            else:
                setattr(self, i, self.attrs[i])


class NetworkModel(ModelPolicy):
    """ Model representing network interfaces
    """

    prev_signal = ('Back to install path',
                   'installpath:show',
                   'installpath')

    signals = [
        ('Network main view',
         'network:show',
         'network')
    ]

    additional_options = [
        ('Set default route',
         'network:set-default-route',
         'set_default_route'),
        ('Bond interfaces',
         'network:bond-interfaces',
         'bond_interfaces'),
        ('Install network driver',
         'network:install-network-driver',
         'install_network_driver')
    ]

    def __init__(self, prober):
        self.prober = prober
        self.network = {}

    def get_signal_by_name(self, selection):
        for x, y, z in self.get_signals():
            if x == selection:
                return y

    def get_signals(self):
        return self.signals + self.additional_options

    def get_menu(self):
        return self.additional_options

    def probe_network(self):
        log.debug('model calling prober.get_network()')
        self.network = self.prober.get_network()

    def get_interfaces(self):
        VALID_NIC_TYPES = ['eth', 'wlan']
        return [iface for iface in self.network.keys()
                if self.network[iface]['type'] in VALID_NIC_TYPES and
                not self.network[iface]['hardware']['DEVPATH'].startswith(
                    '/devices/virtual/net')]

    def get_vendor(self, iface):
        hwinfo = self.network[iface]['hardware']
        vendor_keys = [
            'ID_VENDOR_FROM_DATABASE',
            'ID_VENDOR',
            'ID_VENDOR_ID'
        ]
        for key in vendor_keys:
            try:
                return hwinfo[key]
            except KeyError:
                log.warn('Failed to get key '
                         '{} from interface {}'.format(key, iface))
                pass

        return 'Unknown Vendor'

    def get_model(self, iface):
        hwinfo = self.network[iface]['hardware']
        model_keys = [
            'ID_MODEL_FROM_DATABASE',
            'ID_MODEL',
            'ID_MODEL_ID'
        ]
        for key in model_keys:
            try:
                return hwinfo[key]
            except KeyError:
                log.warn('Failed to get key '
                         '{} from interface {}'.format(key, iface))
                pass

        return 'Unknown Model'

    def get_iface_info(self, iface):
        ipinfo = SimpleInterface(self.network[iface]['ip'])
        return (ipinfo, self.get_vendor(iface), self.get_model(iface))
