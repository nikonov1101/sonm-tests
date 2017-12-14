import json
import os
import subprocess

import infrastructure

IS_VERBOSE = os.getenv('VERBOSE_TEST') is not None


def _call_cli(*args):
    cmd = [infrastructure.CLI, '--out', 'json']
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

################################
# utils on top of cli
###############################
def hub_get_eth_id():
    out = _call_cli('hub', 'status')
    data = json.loads(out)
    return data['ethAddr']

def hub_remove_asks():
    out = _call_cli('hub', 'ask-plan', 'list')
    data = json.loads(out)

    for slot in data['slots']:
        out = _call_cli('hub', 'ask-plan', 'remove', slot)
        data = json.loads(out)
        assert data['status'] == 'OK'


##############################
# commands wrappers
##############################
def hub_status():
    out = _call_cli('hub', 'status')
    return json.loads(out)


def hub_worker_list():
    out = _call_cli('hub', 'worker', 'list')
    return json.loads(out)


def hub_worker_status(id):
    out = _call_cli('hub', 'worker', 'status', id)
    return json.loads(out)


def hub_dev_list():
    out = _call_cli('hub', 'dev', 'list')
    return json.loads(out)


def hub_dev_set_props(id, file_path):
    out = _call_cli('hub', 'dev', 'set', id, file_path)
    return json.loads(out)


def hub_dev_get_props(id):
    out = _call_cli('hub', 'dev', 'get', id)
    return json.loads(out)


def hub_acl_list():
    out = _call_cli('hub', 'acl', 'list')
    return json.loads(out)


def hub_acl_register(addr):
    out = _call_cli('hub', 'acl', 'register', addr)
    return json.loads(out)


def hub_acl_deregister(addr):
    out = _call_cli('hub', 'acl', 'deregister', addr)
    return json.loads(out)


def hub_ask_list():
    out = _call_cli('hub', 'ask-plan', 'list')
    return json.loads(out)


def hub_ask_create(price, slot_file):
    out = _call_cli('hub', 'ask-plan', 'create', price, slot_file)
    return json.loads(out)


def hub_ask_remote(id):
    out = _call_cli('hub', 'ask-plan', 'remove', id)
    return json.loads(out)


def hub_task_list():
    out = _call_cli('hub', 'task', 'list')
    return json.loads(out)


def market_get_by_id(id):
    out = _call_cli('market', 'show', id)
    return json.loads(out)
