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
- Miltiple miners
- Task with miltiple ports
- Check for network metrics
