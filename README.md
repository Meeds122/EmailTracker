This README will be updated eventually.

Currently the software is in the ultra-beta stage and needs some major bug hunting and refinement before it gets used.

If you want to contribute, please do so. The main.py file currently has all of my notes. 

The end goal is the ease in tracking email openings. 

It uses .csv files in the excell format for ease of import and  export. 

It uses the time and a unique classwide identifier for the instance to generate a unique hash. Email clients then try to resolve that image and
the built in server class parses the GET request and increments the hit count for the hash in the .csv file. I would like to add the capabitiy to log
the last hit time as well and have left that option in the csv file format specification.

TODO:
-Create optional command line argument to change default request location 
parser should be able to handle it. It only looks at the second to last item in the url
-I'd like to change the csv spec to include headers for human readibility when imported into spreadsheet applications
-When inserting the html tag into thunderbird, it attempts to resolve the img as well. This could throw off the targeting of individuals. 
-Add last click time functionality


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
        -dump file.csv            | dump a file to stdout. ID displayed is only the first 7 digits
    Examples:
        mailtracker.py -server -port 56789 -csvfile register.csv
        mailtracker.py -newtag -name john -server customcrypto.com -port 56789 -csvfile register.csv
        mailtracker.py -dump register.csv
        
    [!] -server, -newtag, -dump must be the first argument called
    [!] All parameters for an instance must be set
    [!] Some email clients will attempt to resolve the image as well. It may be better if you're tracking individuals to start the server process after the email is sent
    
    I recommend you start the server as a daemon process (appending an & to the end in unix and disown)
    To exit, ctrl-pause on a windows machine in cmd (I know, its a windows python thing)