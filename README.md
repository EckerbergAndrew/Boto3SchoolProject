# Boto3SchoolProject
A project I did for 3rd year Automated Cloud services class at WIT
part 1 sets up a variable for the keypair, then makes an EC2 instance in the AWS cloud
There's a wait_until_running set up with a sleep command for 30 seconds to allow it to fully set up
before setting its ip address to a variable for later use

part 2 is uploading, chmod-ing, and running a monitoring script (included, written by instructor for use in project)  

part 3 is creating a bucket

part 4 gets an image from an external S3 bucket and uploads it into the one set up in part 3

part 5 creates the home page of an apache server via second external script (made by me)

The apache server homepage contains an image of the WIT crest, as well as local server metadata (ip address,hostname,
and instance type)
