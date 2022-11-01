import zmq
import io
import PIL.Image as Image

####this is how we will send a png package to the microservice.
####lets open are image before sending it
##photo = open("Image.png","rb")
####converts image into bytearray
##convert_to_bytes = bytearray(photo.read())
####converts bytearray into byte code
####bytecode = base64.b64encode(convert_to_bytes)
##bytecode = bytes(convert_to_bytes)

def convert_image_to_send(file_path):

    ##based on a local file_path in the system we
    ##will condense the image into a bytearray than byte data type.
    
    with open(file_path, "rb") as image:
        f = image.read()
        image_data = bytearray(f)
        image_data = bytes(image_data)

    return image_data
##    return f


context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


while True:

    '''Client side application, Partners project is going to make a request
    Through javascript using the same ZMQ framework. Python code can be altered
    where need be.'''



    user_input = input("Choices: \n1.) upload new image \n2.) return image \n3.) delete image\n")

    if int(user_input) == 1:
        
        ##now the user will enter in a file path for the image data
        image_path = input("Enter image path: \n")
        img = convert_image_to_send(image_path)

        
        print(f"Sending request …")
        socket.send_multipart([str.encode(user_input),str.encode(image_path),img])

        
        #  Get the reply.
        message = socket.recv()
        print(f"Received reply [ {message} ]")




    elif int(user_input) == 2:
        
        image_name = input("Enter image name: \n")
        
        socket.send_multipart([str.encode(user_input),str.encode(image_name),b""])

        print(f"Sending request …")

        #  Get the image, is stored in bytes.
        img = socket.recv()
        image = Image.open(io.BytesIO(img))
        image.show()
        

        
    elif int(user_input) == 3:

        image_name = input("Enter image name: \n")
        
        socket.send_multipart([str.encode(user_input),str.encode(image_name),b""])

        print(f"Sending request …")

        #  Get the image, is stored in bytes.
        img = socket.recv()
        print(img)

    else:
        print("Incorrect input")














