# PartnerRepo
## Craftics Database - Communication Contract
This repository is a storage location for photos that will be saved in relation to my partners Craftics Database.
The package we will be using to communicate will be through ZeroZMQ with my microservice using Pyzmq specifically. 

Application will only need a standard socket zmq socket connection.

### Client
```
import zmq

context = zmq.Context()
#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
```

Sending image data through the socket requires it be in bytes, a simple python function has been made if needed.
regardless of how, the user just needs to convert all data into bytes.

```
def convert_image_to_send(file_path):

    ##based on a local file_path in the system we
    ##will condense the image into a bytearray than byte data type.
    
    with open(file_path, "rb") as image:
        f = image.read()
        image_data = bytearray(f)
        image_data = bytes(image_data)

    return image_data
    
```

### Request data
Once connection is established between server and client, the client needs to send 3 pieces of data. (1-3, image_name, image_data)

First arg: $~~~~~$ '1' '2' or '3' string data type. 
- 1.) upload photo  
- 2.) return image  
- 3.) delete image

Second arg: $~~~$ Name of image including file type 
- exa.) "result.png"

Third arg: $~~~~$ Using the above function to convert "result.png" into bytes.
- exa.) img = convert_image_to_send(file_path)

### Request example
All variables need to be in byte format.
```
socket.send_multipart([user_input,image_path,img])

```
### Recieve example
A single result will be return based on expected result.
`socket.recv()`















