# service_quality_test_to_providers
A model to test the quality of service and experience on internet providers in local or remote clients. The characteristics of each internet provider can be analyzed in real time. The model is useful on SO Linux.

![](https://github.com/claudiorogerio/service_quality_test_to_providers/blob/main/img/overview_redes.png)

###  *Dependencies:*
- [x] sudo apt install python3
- [x] pip install colorama

### > Execute on port 5600
```shell
python3 client.py
```

### > Usage
> 1 - Server send all project compressed, and the service time to operating synchronously
> 2 - Client download, unzip project, and waiting the service time to iniciate operations
> 3 - Client start to collect data
> 4 - Periodically send data to server
> 5 - Server create all reports about quality os service
