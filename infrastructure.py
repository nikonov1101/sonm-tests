import subprocess
import os
import re
import signal
import time

import docker


BIN_ROOT = os.getenv('GOPATH') + '/src/github.com/sonm-io/core'
HUB = BIN_ROOT + '/sonmhub'
MINER = BIN_ROOT + '/sonmminer'
CLI = BIN_ROOT + '/sonmcli'
BOOT_TIMEOUT = 10


def remove_old_containers():
    print('REMOVE ALL RUNNING DOCKER CONTAINERS')
    d = docker.from_env()

    for c in d.containers.list():
        c.remove(force=True)


def start_hub():
    hub_ps = subprocess.Popen(
        HUB,
        cwd=BIN_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True,
        preexec_fn=os.setsid,
    )
    print('HUB started')
    return hub_ps.pid


def start_miner():
    miner_ps = subprocess.Popen(
        MINER,
        cwd=BIN_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True,
        preexec_fn=os.setsid,
    )
    print('Miner started')
    return miner_ps.pid


def bootstrap():
    remove_old_containers()

    hub_pid = start_hub()
    miner_pid = start_miner()

    print('Wait for nodes...')
    time.sleep(BOOT_TIMEOUT)

    print('Test infrastructure started')
    return [hub_pid, miner_pid]


def _clean_test_task_files():
    cwd = os.path.dirname(os.path.abspath(__file__))
    for f in os.listdir(cwd):
        if re.search(r'(.*)\.yaml', f):
            os.remove(os.path.join(cwd, f))


def clean_tmp_data():
    _clean_test_task_files()


def shutdown(pids):
    print('Stopping test infrastructure...')
    for pid in pids:
        print('Killing process with PID = {}'.format(pid))
        os.killpg(pid, signal.SIGKILL)
    print('Test infrastructure was stopped...')

    clean_tmp_data()
    print('Environment was cleaned.')
