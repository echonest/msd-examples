msd-examples
===========
Example code for processing the Million Song Database. This repostory contains
code that can be used to process the million song dataset.

The Million Song Dataset is a freely-available collection of audio features and metadata for a million contemporary popular
music tracks available at:

 http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset

 Its purposes are:

 * To encourage research on algorithms that scale to commercial sizes
 * To provide a reference dataset for evaluating research
 * As a shortcut alternative to creating a large dataset with The Echo Nests API
 * To help new researchers get started in the MIR field

The core of the dataset is the feature analysis and metadata for one million songs, provided by The Echo Nest. The dataset
does not include any audio, only the derived features. Note, however, that sample audio can be fetched from services like
7digital, using code we provide.  Additional datasets have been attached to the Million Song Dataset, so far they contain lyrics and cover songs.  The Million Song Dataset started as a collaborative project between The Echo Nest and LabROSA. 
It was supported in part by the NSF.

These examples depend on mrjob, a python library for running MapReduce jobs on Hadoop or Amazon web services.  See
https://github.com/Yelp/mrjob and http://packages.python.org/mrjob/.


MSD Data on S3
==============
These examples use MSD data that has been loaded on to S3 at s3://tbmmsd.  There are around 330 files each with about 3000
sets track data each (one set per line) where each line is represented by 54 fields as described here:  
    
 http://labrosa.ee.columbia.edu/millionsong/pages/field-list

except that in the flat file format, the 'track id' field has been moved from field 52 to the first field.


Map-reduce jobs
===============

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


