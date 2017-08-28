import pytest
import cli
import infrastructure


@pytest.fixture(scope="module")
def yoba():
    pids = infrastructure.bootstrap()
    yield
    infrastructure.shutdown(pids)


def test_hub_ping(yoba):
    rs = cli.hub_ping()
    assert rs['status'] == 'OK'


def test_hub_status(yoba):
    rs = cli.hub_status()
    assert rs['uptime'] > 0
    assert rs['minerCount'] == 1
