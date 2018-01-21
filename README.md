This README will be updated eventually.

Currently the software is in the ultra-beta stage and needs some major bug hunting and refinement before it gets used.

If you want to contribute, please do so. The main.py file currently has all of my notes. 

The end goal is the ease in tracking email openings. 

It uses .csv files in the excell format for ease of import and  export. 

It uses the time and a unique classwide identifier for the instance to generate a unique hash. Email clients then try to resolve that image and
the built in server class parses the GET request and increments the hit count for the hash in the .csv file. I would like to add the capabitiy to log
the last hit time as well and have left that option in the csv file format specification.

Current known issues are 
-CLI problems and parsing issues.
-Server instability