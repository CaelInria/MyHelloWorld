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

Result examples
---------------
```
POST /welcome                                             ==>    Welcome! :-))))

POST /login(admin, root)                                  ==>    {"token":"TID_1513783243"}
POST /login(admin, admin)                                 ==>    {"fault":"too easy :o) ;-p"}
POST /login(tagada, pouet)                                ==>    {"fault":"invalid login and password"}
POST /login(foo, bar)                                     ==>    {"token":"TID_1513783245"}

POST /compute(TID_1513783243, "1 + 1")                    ==>    {"result":"2"}
POST /compute(TID_1513783245, "(1 + 2.2) * 3.14")         ==>    {"result":"10.048"}
POST /compute(TID_1513783243, "'foo' + 'foo' + 'foo'")    ==>    {"result":"foofoofoo"}
POST /compute(TID_1513783245, "1 + 1 == 2")               ==>    {"result":"True"}
POST /compute(TID_1513783243, "'foo' == 2")               ==>    {"result":"False"}

POST /setlifetime(TID_1513783243, 1000)                   ==>    {"fault":"lifetime too large = "1000"}
POST /setlifetime(TID_1513783243, 2)                      ==>    {"TID_1513783243.lifetime":"2"}

POST /compute(TID_1513783243, "1 + 1 == 2")               ==>    {"fault":"Zzz Zzz - lived for "4 seconds"}
POST /compute(TID_1513783245, "'foo = ' + str(3.14)")     ==>    {"result":"foo = 3.14"}
POST /compute(TID_1513783245, "sqrt(144)")                ==>    {"result":"12.0"}

POST /bye                                                 ==>    That's all Folks! :-))))
```
