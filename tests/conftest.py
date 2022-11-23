from string import printable

import pytest

import interactions

client = interactions.Client(
    "ODIzMTQxMTE3ODUxMjA1Njgy.G8pIon.3WZzfl6W-C5HO-E_rAHfCojJKeG6aq3keFvjGw"
)  # this token is invalidated
client._http = interactions.HTTPClient(client._http, client._cache)


def pytest_sessionstart(session):
    class _Request:
        async def request(self, route, **kwargs):
            if route.method == "POST" and route.path == "/channels/123456789/messages":
                kwargs["json"]["author"] = {}

            if json := kwargs.get("json"):
                return json

            return kwargs.get("data")  # I think we have to manually assert here

    interactions.api.http.request._Request.request = _Request.request


def pytest_sessionfinish(session):
    del client._http._req._session


@pytest.fixture(scope="session")
def fake_client():
    return client


@pytest.fixture(autouse=True)
def clear_commands(fake_client):
    fake_client._commands = []


@pytest.fixture(autouse=True)
def ensure_no_stdout(capfd):
    yield
    out, _ = capfd.readouterr()
    assert all(letter not in out for letter in printable)


@pytest.fixture(scope="session")
def channel(fake_client):
    ch = interactions.Channel(id=123456789, guild_id=987654321, _client=fake_client._http)
    ch.available_tags = []
    fake_client._http.cache[interactions.Channel].add(ch)
    return ch


@pytest.fixture(scope="session")
def guild(fake_client):
    g = interactions.Guild(id=987654321, _client=fake_client._http)
    fake_client._http.cache[interactions.Guild].add(g)
    return g


# todo test get func
# todo test every model
# todo "test" every http func?
# todo test gateway (events (-> AND CACHE)) as good as possible with fake data
# todo run every get request func in a sep file to ensure 0 printouts