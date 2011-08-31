msd-examples
===========

Example code for processing the Million Song Database. This repostory contains
code that can be used to process the million song dataset.

 http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset

Density
------
Finds the most dense and the least dense songs

density.py


### Local Usage:

    python density.py tiny.dat


### EC2 Usage
This will run the job on EC2 Map reduce on 100 small instances. Note that you have to 
add the track.py code to t.tar.gz with:

    % tar cvfz t.tar.gz track.py

To run the job on 100 CPUs on all of the MSD use:     

    %  python density.py --num-ec2-instances 100 --python-archive t.tar.gz -r emr 's3://tbmmsd/*.tsv.*' > output.dat


(Of course you will need to setup your Amazon credentials. See http://packages.python.org/mrjob/writing-and-running.html#running-on-emr )


