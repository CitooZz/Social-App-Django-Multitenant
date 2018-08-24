from django.db import connection
from django.conf import settings
from django.core.urlresolvers import reverse

from tenant_schemas.test.cases import TenantTestCase
from tenant_schemas.test.client import TenantClient
from tenant_schemas.utils import get_tenant_model


class TestMultiTenantSocialAuth(TenantTestCase):

    @classmethod
    def setUpClass(cls):
        settings.AUTHENTICATION_BACKENDS = ('social_core.backends.twitter.TwitterOAuth',
                                            'django.contrib.auth.backends.ModelBackend',)
        cls.sync_shared()
        tenant_domain = 'tenant.test.com'
        invalid_tenant_domain = 'invalid_tenant.test.com'

        cls.social_auth_settings = {
            'twitter': {
                'SOCIAL_AUTH_TWITTER_KEY': 'TtfLziJDLaNc0bRwCCYCxpMIc',
                'SOCIAL_AUTH_TWITTER_SECRET': 'AXgPEFhJNHtbhBycoKn9KfMtsINOAOHsQ4o2wSJmzG0XCMeVbr'
            }
        }
        cls.tenant = get_tenant_model()(domain_url=tenant_domain,
                                        schema_name='test', social_auth_settings=cls.social_auth_settings)

        cls.tenant.save(verbosity=0)

        cls.invalid_tenant = get_tenant_model()(domain_url=invalid_tenant_domain,
                                                schema_name='invalid_test', social_auth_settings={})
        cls.invalid_tenant.save(verbosity=0)

        connection.set_tenant(cls.tenant)

    def setUp(self):
        self.c = TenantClient(self.tenant)
        self.invalid_c = TenantClient(self.invalid_tenant)

    def test_tenant_social_auth_settings(self):
        self.assertEqual(self.tenant.social_auth_settings,
                         self.social_auth_settings)

    def test_user_login(self):
        response = self.c.get(
            reverse('social:begin', args=['twitter']))
        self.assertIn('auth_token=', response['Location'])

    def test_invalid_user_login(self):
        connection.set_tenant(self.invalid_tenant)
        response = self.invalid_c.get(
            reverse('social:begin', args=['twitter']))

        self.assertEqual(400, response.status_code)
