from test_utils import CharmTestCase
from mock import patch
import neutron_plumgrid_context as context
import charmhelpers

TO_PATCH = [
    'config',
    'relation_get'
]


def fake_context(settings):
    def outer():
        def inner():
            return settings
        return inner
    return outer


class NeutronPGContextTest(CharmTestCase):

    def setUp(self):
        super(NeutronPGContextTest, self).setUp(context, TO_PATCH)
        self.relation_get.side_effect = self.test_relation.get
        self.config.side_effect = self.test_config.get
        self.test_config.set('enable-metadata', False)
        self.test_config.set('plumgrid-username', 'plumgrid')
        self.test_config.set('plumgrid-password', 'plumgrid')
        self.test_config.set('plumgrid-virtual-ip', '192.168.100.250')

    def tearDown(self):
        super(NeutronPGContextTest, self).tearDown()

    @patch.object(context, '_identity_context')
    @patch.object(charmhelpers.contrib.openstack.context, 'config',
                  lambda *args: None)
    @patch.object(charmhelpers.core.hookenv, 'relation_get')
    @patch.object(charmhelpers.contrib.openstack.context, 'relation_ids')
    @patch.object(charmhelpers.contrib.openstack.context, 'related_units')
    @patch.object(charmhelpers.contrib.openstack.context, 'config')
    @patch.object(charmhelpers.contrib.openstack.context, 'unit_get')
    @patch.object(charmhelpers.contrib.openstack.context, 'is_clustered')
    @patch.object(charmhelpers.contrib.openstack.context, 'https')
    @patch.object(context.NeutronPGPluginContext, '_save_flag_file')
    @patch.object(context.NeutronPGPluginContext, '_ensure_packages')
    @patch.object(charmhelpers.contrib.openstack.context,
                  'neutron_plugin_attribute')
    @patch.object(charmhelpers.contrib.openstack.context, 'unit_private_ip')
    def test_neutroncc_context_api_rel(self, _unit_priv_ip, _npa, _ens_pkgs,
                                       _save_ff, _https, _is_clus, _unit_get,
                                       _config, _runits, _rids, _rget,
                                       _iden_settings):
        def mock_npa(plugin, section, manager):
            if section == "driver":
                return "neutron.randomdriver"
            if section == "config":
                return "neutron.randomconfig"

        config = {
                  'enable-metadata': False,
                  'plumgrid-username': 'plumgrid',
                  'plumgrid-password': 'plumgrid',
                  'plumgrid-virtual-ip': '192.168.100.250'
                  }

        def mock_config(key=None):
            if key:
                return config.get(key)

            return config

        self.maxDiff = None
        self.config.side_effect = mock_config
        _npa.side_effect = mock_npa
        _iden_settings.return_value = {
            'auth_host': '10.0.0.1',
            'auth_port': '35357',
            'auth_protocol': 'http',
            'service_tenant': 'admin',
            'service_username': 'admin',
            'service_password': 'admin',
        }
        _unit_get.return_value = '192.168.100.201'
        _unit_priv_ip.return_value = '192.168.100.201'
        napi_ctxt = context.NeutronPGPluginContext()
        expect = {
            'enable_metadata': False,
            'pg_username': 'plumgrid',
            'pg_password': 'plumgrid',
            'virtual_ip': '192.168.100.250',
            'config': 'neutron.randomconfig',
            'core_plugin': 'neutron.randomdriver',
            'local_ip': '192.168.100.201',
            'network_manager': 'neutron',
            'neutron_plugin': 'plumgrid',
            'neutron_security_groups': None,
            'neutron_url': 'https://None:9696',
            #'admin_user': 'admin',
            #'admin_password': 'admin',
            #'admin_tenant_name': 'admin',
            #'service_protocol': 'http',
            #'auth_port': '35357',
            #'auth_host': '10.0.0.1',
            'metadata_mode': 'tunnel',
            'nova_metadata_proxy_secret': 'plumgrid',
            'pg_metadata_ip': '169.254.169.254',
            'pg_metadata_port': '8775',
        }
        self.assertEquals(expect, napi_ctxt())
