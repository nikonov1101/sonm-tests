import re

import pytest

import cli
import infrastructure


@pytest.fixture(scope="module")
def yoba():
    pids = infrastructure.bootstrap()
    yield
    infrastructure.shutdown(pids)


def test_miner_list(yoba):
    rs = cli.miner_list()

    # there is only one miner
    assert len(rs['info']) == 1

    # check miner ip
    miner_addr = list(rs['info'].keys())[0]
    ip, port = miner_addr.split(':')
    assert re.match(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', ip) is not None
    assert int(port) > 1024 and int(port) < 65535


def test_miner_status(yoba):
    ips = cli.miner_list_ips()
    assert len(ips) > 0

    miner = ips[0]
    status = cli.miner_status(miner)

    assert len(status['name']) > 0
    assert status['capabilities'] is not None
    assert len(status['capabilities']['cpu']) > 0
    assert status['capabilities']['cpu'][0]['name'] != ""
    assert status['capabilities']['cpu'][0]['vendor'] != ""
    assert status['capabilities']['cpu'][0]['cores'] > 0
    assert status['capabilities']['cpu'][0]['mhz'] > 0
    assert status['capabilities']['cpu'][0]['ext'] is not None

    assert status['capabilities']['mem'] is not None
    assert status['capabilities']['mem']['total'] > 0
    assert status['capabilities']['mem']['used'] > 0
