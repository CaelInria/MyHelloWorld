RestServerExample

Available requests
------------------
```
http POST localhost:8080/welcome
http POST localhost:8080/login login=admin pass=root
http POST localhost:8080/compute token=<TID> expression="1 + 1 == 2"
http POST localhost:8080/compute token=<TID> expression="1 + 1"
http POST localhost:8080/compute token=<TID> expression="'foo' + 'bar'"
http POST localhost:8080/compute token=<TID> expression="sqrt(12)"
http POST localhost:8080/setlifetime token=<TID> value=10
http POST localhost:8080/bye

```
