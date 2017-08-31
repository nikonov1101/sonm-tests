import pytest
import cli
import infrastructure
import yaml
import uuid
import re
import time

import docker
import requests


@pytest.fixture(scope="module")
def yoba():
    pids = infrastructure.bootstrap()
    yield
    infrastructure.shutdown(pids)


def _create_task_yaml(image):
    task = {
        'task': {
            'container': {
                'name': image,
            },
            'resources': {
                'CPU': 1,
                'RAM': '10Mb',
            }
        }
    }

    data = yaml.dump(task, default_flow_style=False)
    file_name = str(uuid.uuid4()) + '.yaml'

    with open(file_name, 'w') as f:
        f.write(data)

    return file_name


def test_task_list(yoba):
    ips = cli.miner_list_ips()
    assert len(ips) > 0

    miner = ips[0]
    tasks = cli.task_list(miner)
    # we don't started any task yet
    assert len(tasks) == 0


def test_task_start(yoba):
    ips = cli.miner_list_ips()
    miner = ips[0]

    task_file = _create_task_yaml('httpd:latest')
    task = cli.task_start(miner, task_file)

    assert len(task['id']) > 0
    assert len(task['endpoint']) > 0
    assert re.match(r'.{8}\-.{4}\-.{4}\-.{4}\-.{12}', task['id']) is not None
    assert len(task['endpoint']) == 1

    # move this shit into another test
    d = docker.from_env()
    ctr_list = d.containers.list()
    assert len(ctr_list) == 1

    ctr = ctr_list[0]
    port = list(ctr.attrs['Config']['ExposedPorts'].keys())[0]

    assert ctr.status == 'running'
    assert ctr.attrs['Config']['Image'] == 'httpd:latest'
    assert port == '80/tcp'

    # fixme(sshaman1101): hardcoded localhost may be shitty in some cases.
    localAddr = 'http://127.0.0.1:' + ctr.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']
    print('TRY TO CONNECT TO PAYLOAD AT {}'.format(localAddr))

    stepCount = 0
    maxSteps = 5
    rs = None

    # try to connect to container's payload every second
    while stepCount < maxSteps:
        print('   CONNECTING TO PAYLOAD STEP #{}'.format(stepCount))
        try:
            rs = requests.get(localAddr)
            break
        except Exception as e:
            print('   CANNOT CONNECT TO PAYLOAD: {}'.format(e))
            stepCount += 1
            time.sleep(1)

    assert '<html><body><h1>It works!</h1></body></html>\n' == rs.text


def test_task_list_noempty(yoba):
    ips = cli.miner_list_ips()
    assert len(ips) > 0

    miner = ips[0]
    tasks = cli.task_list(miner)
    assert len(tasks['statuses']) == 1

    task_id = list(tasks['statuses'].keys())[0]
    # status 2 is internal code for RUNNING state
    assert tasks['statuses'][task_id]['status'] == 2


def test_task_status():
    # get task list and extract task id
    ips = cli.miner_list_ips()
    miner = ips[0]
    tasks = cli.task_list(miner)
    task_id = list(tasks['statuses'].keys())[0]

    # wait for stats
    time.sleep(30)

    # get task status by id
    t_status = cli.task_status(miner, task_id)
    assert t_status['id'] == task_id
    assert t_status['miner'] == miner
    assert t_status['status'] == 'RUNNING'
    assert t_status['image'] == 'httpd:latest'
    assert int(t_status['uptime']) > 0
    assert int(t_status['cpu']) > 0
    assert int(t_status['mem']) > 0


def test_task_stop():
    ips = cli.miner_list_ips()
    miner = ips[0]
    tasks = cli.task_list(miner)
    task_id = list(tasks['statuses'].keys())[0]

    cli.task_stop(miner, task_id)

    d = docker.from_env()
    ctr_list = d.containers.list()
    assert len(ctr_list) == 0
