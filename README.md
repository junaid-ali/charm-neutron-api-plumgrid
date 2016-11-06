# About the PLUMgrid Platform

The [PLUMgrid Platform](http://www.plumgrid.com/technology/plumgrid-platform/) is a software-only solution that provides a rich set of distributed network functions such as routers, switches, NAT, IPAM, DHCP, and it also supports security policies, end-to-end encryption, and third party Layer 4-7 service insertion.

# Overview

This charm enables PLUMgrid Neutron plugin in an OpenStack environment.

Once deployed, the charm enables the necessary actions in the neutron-server container that allows the PLUMgrid plugin to take over networking for the OpenStack environment.

It is a subordinate charm to neutron-api charm.

# Usage

Instructions on using the charm:

    juju deploy neutron-api
    juju deploy neutron-api-plumgrid
    juju add-relation neutron-api:neutron-plugin-api-subordinate neutron-api-plumgrid:neutron-plugin-api-subordinate
    juju add-relation plumgrid-director:plumgrid-configs neutron-api-plumgrid:plumgrid-configs


# Configuration

Example Config

    neutron-api-plumgrid:
        install_sources: 'ppa:plumgrid-team/stable'
        install_keys: 'null'
        enable-metadata: False
        manage-neutron-plugin-legacy-mode: False
    neutron-api:
        neutron-plugin: "plumgrid"

Provide the source repo path for PLUMgrid Debs in 'install_sources' and the corresponding keys in 'install_keys'
The "neutron-plugin" config parameter is required to be "plumgrid" in the neutron-api charm to enable PLUMgrid.

# Contact Information

Bilal Baqar <bbaqar@plumgrid.com>
Javeria Khan <javeriak@plumgrid.com>
Junaid Ali <junaidali@plumgrid.com>
