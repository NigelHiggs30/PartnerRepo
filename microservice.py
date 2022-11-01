from github import Github
import os
import io
import PIL.Image as Image
import time
import zmq
import dis

class Github_Obj:
    
    #contruct for all variables need to interact with github repository
    def __init__(self, repo, commit_messag, branch_name):
        self.repo = repo
        self.commit_message = commit_message
        self.branch_name = branch_name


    def upload_new_image(self,image_name,image_data):
        ##to upload a new photo to Photo folder, we need to obtain its contents
        contents = self.repo.get_contents("Photos",ref=self.branch_name)        
        
        ##next we want update the repository and to store the image
        self.repo.update_file("Photos/"+image_name.decode(),self.commit_message, image_data, contents[0].sha, branch=self.branch_name)

    def return_image(self,image_name):
        ##lets send are get_contents request
        contents = self.repo.get_contents("Photos/"+image_name.decode(),ref=self.branch_name)

        image = contents.decoded_content

        return image

    def delete_image(self,image_name):
        ###lets delete it
        contents = self.repo.get_contents("Photos/"+image_name.decode(), ref=self.branch_name)
        self.repo.delete_file(contents.path, "remove test", contents.sha, branch=self.branch_name)

def convert_image_to_send(file_path):

    ##based on a local file_path in the system we
    ##will condense the image into a bytearray than byte data type.
    
    with open(file_path, "rb") as image:
        f = image.read()
        image_data = bytearray(f)
        image_data = bytes(image_data)

    return image_data



if __name__ == "__main__":

    '''Boiler plate code to interact with are Github repository code.'''
    
    ##repo contains the api access point to the github account
    g=Github("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")
    repo=g.get_repo("NigelHiggs30/PartnerRepo")

    ##each new commit requires a message
    commit_message = "Commit Message"
    ##name of branch user is interacting with.
    branch_name = "main"

    ##This creates the interactive model for using the repository.
    test = Github_Obj(repo, commit_message, branch_name)

    
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")


    while True:
        
        message = socket.recv_multipart()

        ##when the message is recieved it will contain a list with three
        ##parts (1-3,image_path,image_data)

        if int(message[0].decode())==1:
            test.upload_new_image(message[1],message[2])
        
            #  Send reply back to client
            socket.send(b"Uploaded Photo")

        elif int(message[0].decode()) == 2:

            img = test.return_image(message[1])
            socket.send(img)
            #socket.send(b"Return Image")

        elif int(message[0].decode()) == 3:

            test.delete_image(message[1])
            socket.send(b"Deleted Photo")

        else:
            print("incorrect input")





















