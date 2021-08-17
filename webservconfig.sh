echo '<html>' > index.html
echo 'Private IP address: ' >> index.html
curl http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html
echo '<br> Hostname: ' >> index.html
curl http://169.254.169.254/latest/meta-data/local-hostname >> index.html
echo '<br> Instance Type: ' >> index.html
curl http://169.254.169.254/latest/meta-data/instance-type >> index.html
echo '<br> Requested image: <br>' >> index.html
echo '<img src="https://mybucketforacs.s3-eu-west-1.amazonaws.com/acsimg.jpg">' >> index.html
sudo cp index.html /var/www/html