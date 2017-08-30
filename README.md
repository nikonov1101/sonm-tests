Tests
=====

Integration tests for sonm network components.

Requirements:
1. Build hub, miner and cli from [core repo](https://github.com/sonm-io/core) then put them to `GOPATH/src/github.com/sonm-io/core`
2. Set-up miner and hub using configs


Install stuff and run tests:
```
pip install -r requirements.txt
pytest .
```


Todo:
- make more verbose crash logs
- How to check hub and miner log output?
- Attach multiple miners
- Task with multiple exposed ports
- Checks for container network metrics
- Checks for container resource restrictions
- Work through bad network (random delay, packet loss)
