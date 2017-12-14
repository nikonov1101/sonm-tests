import cli

def test_status():
    rs = cli.hub_status()
    assert rs['uptime'] > 0
    assert rs['minerCount'] > 0
    assert len(rs['ethAddr']) > 0
    # this two asserts may be completely wrong, but nevermind.
    assert 'v0.2.1' in rs['version']
    assert 'amd64' in rs['platform']


def test_worker_list():
    rs = cli.hub_worker_list()
    assert len(rs['info']) > 0


def test_worker_status():
    rs = cli.hub_worker_list()
    worker_id = list(rs['info'].keys())[0]

    rs = cli.hub_worker_status(worker_id)
    assert rs['name'] == worker_id
    assert rs['capabilities']['cpu'][0]['cores'] > 0
    assert rs['capabilities']['cpu'][0]['clockFrequency'] > 0
    assert rs['capabilities']['mem']['total'] > 0
    assert rs['capabilities']['mem']['used'] > 0


def test_dev_list():
    rs = cli.hub_dev_list()
    assert len(rs['CPUs']) >0
    dev_id = list(rs['CPUs'].keys())[0]
    assert len(dev_id) == 32


def test_dev_set_props():
    rs = cli.hub_dev_list()
    dev_id = list(rs['CPUs'].keys())[0]

    rs = cli.hub_dev_set_props(dev_id, 'dev_props.yaml')
    assert rs['status'] == 'OK'


def test_dev_get_props():
    rs = cli.hub_dev_list()
    dev_id = list(rs['CPUs'].keys())[0]

    rs = cli.hub_dev_get_props(dev_id)
    assert rs['foo'] == 1000
    assert rs['bar'] == 2.22


def test_acl_list():
    rs = cli.hub_acl_list()
    hub_id = cli.hub_get_eth_id()

    assert len(rs['ids']) > 0
    # hub must register itself
    assert rs['ids'][0]['id'] == hub_id


def test_acl_register():
    # todo: broken
    pass


def test_acl_unregister():
    # todo: broken
    pass

def test_ask_empty_list():
    rs = cli.hub_ask_list()
    assert len(rs) == 0

def _assert_slot(slot):
    assert slot['buyerRating'] == 22
    assert slot['supplierRating'] == 33

    res = slot['resources']
    assert res['cpuCores'] == 1
    assert res['ramBytes'] == 100
    assert res['gpuCount'] == 1
    assert res['storage'] == 200
    assert res['netTrafficIn'] == 10
    assert res['netTrafficOut'] == 20
    assert res['networkType'] == 2

def test_ask_create_and_delete():
    rs = cli.hub_ask_create('100', 'ask_slot.yaml')
    assert len(rs['id']) == 36

    ls = cli.hub_ask_list()
    slot = ls['slots'][rs['id']]

    _assert_slot(slot)

    # delete orders after test
    cli.hub_remove_asks()
    # ensure that slots are cleaned
    rs = cli.hub_ask_list()
    assert len(rs) == 0

def test_ask_create_and_get_from_market():
    rs = cli.hub_ask_create('100', 'ask_slot.yaml')
    ask = rs['id']
    assert len(ask) == 36

    rs = cli.market_get_by_id(ask)
    assert rs['price'] == '100'
    _assert_slot(rs['slot'])

    # delete orders after test
    cli.hub_remove_asks()
    # ensure that slots are cleaned
    rs = cli.hub_ask_list()
    assert len(rs) == 0

    # ensure that order is deleted from market
    rs = cli.market_get_by_id(ask)
    assert len(rs['error']) > 0
    assert rs['message'] == 'Cannot get order by ID'

def test_task_list():
    rs = cli.hub_task_list()
    # has one worker
    assert len(rs) == 1

    wrk = list(rs.keys())[0]
    # worker has no tasks
    assert len(rs[wrk]) == 0
