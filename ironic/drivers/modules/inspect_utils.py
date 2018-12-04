# Copyright 2018 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_log import log as logging

from ironic.common import exception
from ironic import objects

LOG = logging.getLogger(__name__)


def create_ports_if_not_exist(task, macs):
    """Create ironic ports for the mac addresses.

    Creates ironic ports for the mac addresses returned with inspection
    or as requested by operator.

    :param task: A TaskManager instance.
    :param macs: A dictionary of port numbers to mac addresses
                 returned by node inspection.

    """
    node = task.node
    for port_num, mac in macs.items():
        # TODO(etingof): detect --pxe-enabled flag
        port_dict = {'address': mac, 'node_id': node.id}
        port = objects.Port(task.context, **port_dict)

        try:
            port.create()
            LOG.info("Port %(port_num)s created for MAC address %(address)s "
                     "for node %(node)s", {'address': mac, 'node': node.uuid,
                                           'port_num': port_num})
        except exception.MACAlreadyExists:
            LOG.warning("Port %(port_num)s already exists for "
                        "MAC address %(address)s for node "
                        "%(node)s", {'address': mac,
                                     'node': node.uuid,
                                     'port_num': port_num})
