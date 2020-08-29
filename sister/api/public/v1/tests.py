import inspect
import json
from django.db import connection
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from django_tenants.test.client import TenantClient
from django_tenants.test.cases import TenantTestCase
from snapshottest.unittest import TestCase as uTestCase
from tenant_users.compat import (
    get_public_schema_name,
    get_tenant_model,
    get_tenant_domain_model
)


class GraphQLAPIClient(TenantClient):

    auth_token = None

    def __init__(
            self, api_path, tenant, server_port=8000,
            enforce_csrf_checks=False, **defaults):
        super().__init__(enforce_csrf_checks, **defaults)
        self.api_path = api_path
        self.tenant = tenant
        self.server_port = server_port

    def post(self, data={}, **extra):
        if self.auth_token:
            extra['HTTP_AUTHORIZATION'] = "jwt %s" % self.auth_token
        if 'HTTP_HOST' not in extra:
            extra['HTTP_HOST'] = self.tenant.get_primary_domain().domain
        if 'SERVER_PORT' not in extra:
            extra['SERVER_PORT'] = self.server_port
        return super().post(self.api_path, data, **extra)

    def login(self, email, password):
        auth_token = self._obtain_token(email, password)
        if auth_token:
            return True
        else:
            return False

    def _obtain_token(self, email, password):
        query = """
            mutation JWTLogin($email: String!, $password: String!) {
                tokenObtain(email: $email, password: $password) {
                    payload
                    refreshExpiresIn
                    token
                }
            }
        """
        variables = """
            {
                "email": "%s",
                "password": "%s"
            }
        """ % (email, password)
        response = self.post(
            data={
                'query': query,
                'variables': variables
            },
        )
        data = json.loads(
            response.content.decode('utf-8')
        )['data']['tokenObtain']
        self.auth_token = data.get('token', None)
        return self.auth_token


class GraphQLTestCase(uTestCase, TenantTestCase):

    user_email = 'test@gmail.com'
    user_password = 'test_password'

    @classmethod
    def setup_public_tenant(cls):
        tenant_name = get_public_schema_name()
        tenant_model = get_tenant_model()
        cls.public_tenant = tenant_model.objects.create(
            schema_name=tenant_name,
            name='Public Tenant',
            owner=cls.user)

        # Add one or more domains for the tenant
        cls.public_domain = get_tenant_domain_model().objects.create(
            domain=cls.get_test_domain(),
            tenant=cls.public_tenant,
            is_primary=True)

        cls.public_tenant.add_user(cls.user)

    @classmethod
    def get_test_domain(cls):
        return 'test.com'

    @classmethod
    def setUpClass(cls):
        cls.sync_shared()
        cls.add_allowed_test_domain()

        # setup user
        cls.setup_user()
        cls.setup_public_tenant()

        cls.tenant = get_tenant_model()(
            schema_name=cls.get_test_schema_name(),
            owner=cls.user
        )
        cls.tenant.save(verbosity=cls.get_verbosity())

        # Set up domain
        tenant_domain = cls.get_test_tenant_domain()
        cls.domain = get_tenant_domain_model()(
            tenant=cls.tenant, domain=tenant_domain)
        cls.setup_domain(cls.domain)
        cls.domain.save()

        connection.set_tenant(cls.tenant)

        # setup snapshoot
        cls._snapshot_tests = []
        cls._snapshot_file = inspect.getfile(cls)

        if cls is not uTestCase and cls.setUp is not uTestCase.setUp:
            orig_setUp = cls.setUp
            orig_tearDown = cls.tearDown

            def setUpOverride(self, *args, **kwargs):
                uTestCase.setUp(self)
                return orig_setUp(self, *args, **kwargs)

            def tearDownOverride(self, *args, **kwargs):
                uTestCase.tearDown(self)
                return orig_tearDown(self, *args, **kwargs)

            cls.setUp = setUpOverride
            cls.tearDown = tearDownOverride

    @classmethod
    def setup_user(cls):
        cls.user = get_user_model().objects.create(
            id="04f4efe1-8cd4-480b-9e1c-62986b8e897c",
            email=cls.user_email,
            is_active=True
        )
        cls.user.set_unusable_password()
        cls.user.save()
        return cls.user


class PublicTestSchema(GraphQLTestCase):

    def setUp(self):
        self.client = GraphQLAPIClient(
            reverse('api_url_v1'),
            self.public_tenant
        )

    def _signup_request(self, email, password):
        query = """
            mutation newSignUp($email: String!, $password: String!) {
                signUp(email: $email, password: $password) {
                    user {
                        email
                        isActive
                    }
                }
            }
        """
        variables = """
            {
                "email": "%s",
                "password": "%s"
            }
        """ % (email, password)
        response = self.client.post(
            data={
                'query': query,
                'variables': variables
            },
        )
        return response

    def _user_list_request(self):
        query = """
            query {
                userList {
                    edges {
                        node {
                            email
                            isActive
                        }
                    }
                }
            }
        """
        response = self.client.post(
            data={
                'query': query
            },
        )
        return response

    def _login_request(self, email, password):
        query = """
            mutation JWTLogin($email: String!, $password: String!) {
                tokenObtain(email: $email, password: $password) {
                    token
                }
            }
        """
        variables = """
            {
                "email": "%s",
                "password": "%s"
            }
        """ % (email, password)
        response = self.client.post(
            data={
                'query': query,
                'variables': variables
            },
        )
        return response

    def test_query_user_list(self):
        email = "new_email@gmail.com"
        password = "new_password"
        self._signup_request(email, password)
        self.client.login(email, password)
        response = self._user_list_request()
        results = json.loads(response.content.decode('utf-8'))
        self.assertMatchSnapshot(results)

    def test_mutation_signup(self):
        email = "new_email@gmail.com"
        password = "new_password"
        response = self._signup_request(email, password)
        results = json.loads(response.content.decode('utf-8'))
        self.assertMatchSnapshot(results)

    def test_mutation_obtain_token(self):
        email = "new_email@gmail.com"
        password = "new_password"
        self._signup_request(email, password)
        response = self._login_request(email, password)
        self.assertMatchSnapshot(response)

    def test_mutation_obtain_token_wrong_password(self):
        email = "test@gmail.com"
        password = "test_password"
        response = self._login_request(email, password)
        data = json.loads(response.content.decode('utf-8'))['data']
        self.assertIsNone(data.get('tokenObtain'))
