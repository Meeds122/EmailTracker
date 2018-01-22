# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 21:28:54 2018

@author: Tristan Henning (meeds122)

The basic idea now is that an email client will attempt to resolve an image from an email and download the remote content. We can feed the client a 
unique random identifier. When the client attempts access it will attempt to connect to the server started by this software. From there we serve a 1x1 pixel
clear image to satisfy and mark the email as opened.

Basic architecture is 
    new = ID() --> new.generateID() --> new.generateTag(server, port) --> new.setName(name) --> print(new.getTag()) --> list.append(new) --> updateCSV(new)
    Server goes and recieves HTTP requests fro the info and returns 1x1 img or it 404s
    the clients will be requesting emails from <SERVER>:<PORT>/trkr/<ID>.jpg
    
CSV formatting
    ID, name, numberOfClicks, lastClickTime '

The 2 classes will be ID() and Server()
    ID() --> class with the ID, tag, and name associated
    Server --> class that takes requests, responds, updates CSV 

TODO:
    Have server respond with 404 and see if that resolves the reconnection issue
    Fix command line input
    Create optional command line argument to change default request location 
        parser should be able to handle it. It only looks at the second to last item in the url

"""

import datetime
import hashlib
import csv
import socket
import sys



class ID(object):
    internalCounter = 0 #ensures the uniqueness of hashes in same session jic internal clock is too slow    
    def __init__(self):
        self.ID = None
        self.tag = None
        self.name = None
    def generateID(self):
        if self.ID:
            return #see if id is already set for this class obj
        now = datetime.datetime.now()
        hashobj = hashlib.new('ripemd160')
        hashobj.update(str(str(now) + str(ID.internalCounter)).encode())
        ID.internalCounter += 1
        self.ID = hashobj.hexdigest()
    def generateTag(self, server, port):
        if not self.ID:
            self.generateID()
        if self.tag:
            return # see if tag is alrerady generated
        prototag = "<img src='http://<SERVER>:<PORT>/trkr/<ID>.jpg' alt='' width='' height='' border='0' style='border:0; outline:none; text-decoration:none; display:block;'></img>"
        prototag = prototag.replace("<SERVER>", str(server))
        prototag = prototag.replace("<PORT>", str(port))
        prototag = prototag.replace("<ID>", str(self.ID))
        self.tag = prototag
        return self.tag
    def setName(self, name):
        self.name = str(name)
        return
    def getTag(self):
        return self.tag
    def getName(self):
        return self.name
    def getID(self):
        return self.ID

"""
def updateCSV(fileName, ID, name, numOfClicks, lastClickTime)
Usage:
    update CSV file
current function is to read file into memory, try to find ID, if ID exists, replace line, rewrite into file, else append new ID and rewrite into file
there is probably a much better way of doing this but this is what I've been able to come up with at 3:22AM on a Thurday
"""
def updateCSV(fileName, ID, name, numOfClicks, lastClickTime, addIfNotFound=True):
    #todo
    inCSV = list()
    with open(str(fileName), 'r', newline='') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            inCSV.append(row)
    for i in range(len(inCSV)):
        if str(inCSV[i][0]) == str(ID):
            del inCSV[i]
            inCSV.insert(i, [str(ID), str(name), str(numOfClicks), str(lastClickTime)])
            #update file with new
            with open(str(fileName), 'w', newline='') as csvFile:
                writer = csv.writer(csvFile)
                for line in inCSV:
                    writer.writerow([line[0], line[1], line[2], line[3]])
            return True #return if ID is found in CSV file after updating
    if addIfNotFound == False:
        return False
    #ID not found in CSV file and flag set true, adding
    inCSV.append([str(ID), str(name), str(numOfClicks), str(lastClickTime)])
    with open(str(fileName), 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for line in inCSV:
            writer.writerow([line[0], line[1], line[2], line[3]])
    return True # success

"""
def readCSV(fileName)
usage:
    exactly as it looks
    returns list of lines from csv file
"""
def readCSV(fileName):
    csvlist = list()
    with open(str(fileName), 'r', newline='') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            csvlist.append(row)
    return csvlist

def dumpCSV(fileName):
    csvlist = list()
    csvlist = readCSV(fileName)
    print("ID       , NAME      , NUMBER OF CLICKS , LAST CLICK TIME")
    print("=========================================================")
    for i in csvlist:
        print(i[0][:8], ",", i[1], ",", i[2], ",", i[3])



"""
class Server()
Usage:
    create a server object to listen for connections. No required interaction to mark csv values after init
Notes:
    I don't know if I want to implement the multithreading into the server class itself of if it would be better in the main function
    I'll leave that problem for a later date
    I think the server will be a simple TCP socket server that responds to every request with a 404 error
    I'm also not sure why the Server is a class? maybe a function would work as well.
    seems like just leaving the client hanging is working fine? huh

A GET request looks like
GET /somefolder/somefile.jpg HTTP/1.1
Host: server:port
User-Agent:
...

A 404 response request looks like
HTTP/1.1 404 Not Found
Date: Thu, 18 Jan 2018 12:06:10 GMT
Server: Apache/2.4.25 (Debian)
Content-Length

"""
class Server():
    def __init__(self, host='', port=56789, csvFileName='register.csv'):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host,int(port)))
            s.listen(1)
            while True:
                conn, addr = s.accept()
                with conn:
                    print("[*] Connected by", addr)
                    self.data = conn.recv(1024)
                    print("[DEBUGGING] raw data ", str(self.data.decode("utf-8")))
                    datalist = self.data.decode("utf-8").split(' ') # break down header
                    print("[DEBUGGING] data list [1]", datalist[1])
                    item = datalist[1].split('/')[len(datalist[1].split('/')) - 1] # get item from end of stack
                    print("[DEBUGGING] item ", item)
                    recvID = item.split('.')[0]
                    print("[DEBUGGING] ID", str(recvID))
                    csvlist = readCSV(csvFileName)
                    line = list()
                    for i in csvlist:
                        if str(i[0]) == str(recvID):
                            line = i
                        else:
                            continue
                if line:
                    if updateCSV(csvFileName, line[0], line[1], str(int(line[2]) + 1), line[3], addIfNotFound=False):
                        print("[DEBUGGING] Successfully edited CSV file")
                    else:
                        print("[DEBUGGING] Faiure Editing.")
                else:
                    print("[DEBUGGING] Bad ID")

def usage():
    print("""
    Usage: mailtracker.py [OPTIONS]
    Server Options:
        -server                   | start tracking server
        -port 56789               | server port
        -csvfile file.csv         | csvfile to use as register
    Tag Options:
        -newtag                   | make a tag to track
        -name John                | associate a name with ID
        -server customcrypto.com  | server address
        -port 56789               | server port
        -csvfile file.csv         | csvfile to use as register
    Dumping csv file to console:
        -dump file.csv            | dump a file to stdout. ID is only the first 7 digits
    Examples:
        mailtracker.py -server -port 56789 -csvfile register.csv
        mailtracker.py -newtag -name john -server customcrypto.com -port 56789 -csvfile register.csv
        mailtracker.py -dump register.csv
        
    [!] -server, -newtag, -dump must be the first argument called
    [!] All parameters for an instance must be set
    
    I recommend you start the server as a daemon process (appending an & to the end in unix and disown)
    
    """)

def main():
    if len(sys.argv[1:]) < 2:
        usage()
        exit(0)
    elif sys.argv[1] == "-server":
        if len(sys.argv[1:]) != 5:
            print("[!] Syntax error, missing options")
            exit(1)
        args = sys.argv[1:]
        aport = str(args[args.index('-port') + 1])
        fname = str(args[args.index('-csvfile') + 1])
        s = Server(port=aport, csvFileName=fname, host='')
    elif sys.argv[1] == "-newtag":
        if len(sys.argv[1:]) != 9:
            print("[!] Syntax error, missing options")
            exit(1)
        #deconstruct command line args
        args = sys.argv[1:]
        name = str(args[args.index('-name') + 1])
        server = str(args[args.index('-server') + 1])
        port = str(args[args.index('-port') + 1])
        fname = str(args[args.index('-csvfile') + 1])
        new = ID()
        new.setName(name)
        new.generateID()
        print(new.generateTag(server,port))
        if updateCSV(fname, new.getID(), name, '0', '0'):
            print('[*] CSV file sucessfully updated')
            exit(0)
        print('[!] Error updating CSV file')
        exit(1)
    elif sys.argv[1] == "-dump":
        fname = sys.argv[2]
        dumpCSV(fname)
        exit(0)
    else:
        usage()
        exit(0)

if __name__ == "__main__":
    main()

















