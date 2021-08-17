#!/usr/bin/env python3
import boto3
import subprocess
import time

ec2=boto3.resource('ec2')

keyname= input("Enter a key name to be used for the instance: .pem (make sure the key is in the same place you're running this from)")


try:
	new_instance=ec2.create_instances(
		ImageId='ami-0fc970315c2d38f01',
		KeyName=keyname,
		MinCount=1,
		MaxCount=1,
		InstanceType='t2.nano',
		SecurityGroupIds=['sg-025153451860ce6ac'],
		UserData= """ 
		 +
		"""
		)
except Exception as e:
	print(e)
	
instance_list=[]
for inst in ec2.instances.all():
	instance_list.append(inst)


print(instance_list[0])	
instNo=instance_list[0].id
instance_list[0].wait_until_running()
time.sleep(30)
print('Instance is running:')
ipaddr=str(instance_list[0].public_ip_address)
	
	
#monitoring instance:
try: 
    importMonitor = 'scp -o StrictHostKeyChecking=no -i '+keyname+'.pem monitor.sh ec2-user@'+ipaddr + ":."
    print(importMonitor)
    responseImportMonitor = subprocess.run(importMonitor, shell=True)
    authoriseMonitor = 'ssh -i '+keyname+'.pem ec2-user@'+ipaddr+" 'chmod 700 monitor.sh' "
    print(authoriseMonitor)
    responseAuthoriseMonitor = subprocess.run(authoriseMonitor, shell=True)
    runMonitor = 'ssh -i '+keyname+'.pem ec2-user@'+ipaddr + " ' sudo ./monitor.sh' "
    print(runMonitor)
    responseRunMonitor = subprocess.run(runMonitor, shell=True)
    print('Monitor is monitoring')
except Exception as x:
    print(x)

#time to create a bucket
	
s3=boto3.client('s3')

try:
	created=s3.create_bucket(
		ACL='public-read',  #this makes bucket *completely* public, might have to go in and change that
		Bucket='mybucketforacs',
		CreateBucketConfiguration={
			'LocationConstraint': 'eu-west-1',
			},
	)
except Exception as c:
	print(c)

#following line gets image from external s3
subprocess.run(['curl','-s','https://witacsresources.s3-eu-west-1.amazonaws.com/image.jpg','-o','acsimg.jpg'])
 
 #following uploads image from last step to my s3 to be used on my webserver
try:
	response=s3.upload_file('acsimg.jpg','mybucketforacs','acsimg.jpg',ExtraArgs={'ACL':'public-read','ContentType':'jpeg'})
	print(response)
	print('success of image upload')
except Exception as p:
	print(p)
	
#time to create webserver homepage

try:
	importConfigScript='scp -o StrictHostKeyChecking=no -i '+keyname+'.pem webservconfig.sh ec2-user@'+ipaddr+':.'
	print(importConfigScript)
	responseImportConfigScript=subprocess.run(importConfigScript,shell=True)
	authoriseConfig='ssh -i '+keyname+'.pem ec2-user@' + ipaddr+" 'chmod 700 webservconfig.sh' "
	print(authoriseConfig)
	responseAuthoriseConfig=subprocess.run(authoriseConfig,shell=True)
	runConfigure='ssh -i '+keyname+'.pem ec2-user@'+ipaddr+" './webservconfig.sh' "
	print(runConfigure)
	responseRunConfigure=subprocess.run(runConfigure,shell=True)
	print('Website is ready')
except Exception as t:
	print(t)
	
	
	