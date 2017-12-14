Tests
=====

Integration tests for sonm network components.

Requirements:
1. Build components from [core repo](https://github.com/sonm-io/core), clone repo into `GOPATH/src/github.com/sonm-io/core`
2. Set-up config
3. start Hub, Worker and Node; 
    1. Locator and Marketplace is required
    2. Worker might be able to connect to the Hub


Install stuff and run tests:
```
pip install -r requirements.txt
pytest .
```
