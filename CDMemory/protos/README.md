# protos
+ `protobuf support` in PyCharm
+ `pip install protobuf==3.6.0`


## How to regenerates the appropriate python files
```
Example for keyvaluestore.proto 
python -m grpc_tools.protoc \
    -I ./ \ 
    --python_out=. \
    --grpc_python_out=. \
    keyvaluestore.proto
```