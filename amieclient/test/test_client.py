from ..client import Client


class TestClient:
    def test_creation(self):
        c = Client(site_name='test', api_key='test')
        assert c
        assert c._session.headers['XA-SITE'] == 'test'
        assert c._session.headers['XA-API-KEY'] == 'test'
