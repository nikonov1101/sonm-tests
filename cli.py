import json
import os
import subprocess

import infrastructure

IS_VERBOSE = os.getenv("VERBOSE_TEST") is not None
HUB_ADDR = os.getenv('HUB_ADDR', '[::]:10001')
CLI = os.path.join(infrastructure.GOPATH, 'src/github.com/sonm-io/core/sonmcli')


def _call_cli(*args):
    cmd = [CLI, '--addr', HUB_ADDR, '--out', 'json']
    [cmd.append(x) for x in args]
    if IS_VERBOSE:
        print('\r\n****************************************')
        print('RUN: {}'.format(' '.join(cmd)))

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out = result.stdout.decode('utf-8')
    if IS_VERBOSE:
        print('RES: {}'.format(out))
        print('****************************************\r\n')
    return out


def hub_ping():
    out = _call_cli('hub', 'ping')
    return json.loads(out)


def hub_status():
    out = _call_cli('hub', 'status')
    return json.loads(out)


def miner_list():
    out = _call_cli('miner', 'list')
    return json.loads(out)


def miner_list_ips():
    out = _call_cli('miner', 'list')
    data = json.loads(out)
    return list(data['info'].keys())


def miner_status(miner):
    out = _call_cli('miner', 'status', miner)
    return json.loads(out)


def task_list(miner):
    out = _call_cli('task', 'list', miner)
    return json.loads(out)


def task_start(miner, task_file):
    out = _call_cli('task', 'start', miner, task_file)
    return json.loads(out)


def task_status(miner, task_id):
    out = _call_cli('task', 'status', miner, task_id)
    return json.loads(out)


def task_stop(miner, task_id):
    out = _call_cli('task', 'stop', miner, task_id)
    return json.loads(out)
