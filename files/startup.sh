curl http://169.254.169.254/latest/meta-data/public-keys/0/openssh-key > /tmp/my-key
        cat /tmp/my-key > /home/admin/.ssh/authorized_keys
        chmod 600 /home/admin/.ssh/authorized_keys
        >/root/.ssh/authorized_keys
        rm /tmp/my-key

/opt/rbrain/bin/python /opt/rbrain/lib/python2.7/site-packages/rbrain/manage.py collectstatic --noinput
/opt/rbrain/bin/python /opt/rbrain/lib/python2.7/site-packages/rbrain/manage.py migrate --noinput
/opt/rbrain/bin/python /opt/rbrain/lib/python2.7/site-packages/rbrain/manage.py create_initial_admin_account admin `/opt/rbrain/bin/python /opt/rbrain/bin/get_aws_data.py InstanceID`
/opt/rbrain/bin/python /opt/rbrain/lib/python2.7/site-packages/rbrain/manage.py loaddata /opt/rbrain/bin/data.json

mkdir -p /mnt/ride/
rm -rf /mnt/ride/*
echo `/opt/rbrain/bin/python /opt/rbrain/bin/get_aws_data.py EFS`":// /mnt/ride/ nfs4 _netdev 0 0" >> /etc/fstab
mount -a
mkdir -p /mnt/ride/work
mkdir -p /mnt/ride/libraries
mkdir -p /mnt/ride/ride-share
chmod 775 /mnt/ride
echo "{" > /mnt/ride/ride-share/key.json
#echo "  \"instanceId\":" \"`curl http://169.254.169.254/latest/meta-data/instance-id`\", >> /mnt/ride/ride-share/key.json
#echo "  \"region\":" \"`/opt/rbrain/bin/python /opt/rbrain/bin/get_aws_data.py region`\" >> /mnt/ride/ride-share/key.json
echo "  \"customer\":" \"test\", >> /mnt/ride/ride-share/key.json
echo "  \"licenseKey\":" \"4s3vdzx9\(\)s\" >> /mnt/ride/ride-share/key.json
echo "}" >> /mnt/ride/ride-share/key.json
chown apprbrain:apprbrain -R /mnt/ride/

sed -i "s/APP_URL/`/opt/rbrain/bin/python /opt/rbrain/bin/get_aws_data.py AppELB`/g" /etc/nginx/sites-enabled/rbrain_api.conf
sed -i "s/APP_URL/`/opt/rbrain/bin/python /opt/rbrain/bin/get_aws_data.py AppELB`/g" /etc/nginx/sites-enabled/rbrain_api-redirect.conf
sed -i "s/PREVIEWS_URL/`/opt/rbrain/bin/python /opt/rbrain/bin/get_aws_data.py PreviewsELB`/g" /etc/nginx/sites-enabled/rbrain_api-previews.conf

rabbitmqctl add_user rbrain ovNadyojnopArm2
rabbitmqctl set_user_tags rbrain administrator
rabbitmqctl add_vhost rbrain
rabbitmqctl set_permissions -p rbrain rbrain ".*" ".*" ".*"

service rabbitmq-server restart
sleep 1
service docker restart
sleep 1
service docker-consul.service restart
service docker-manager.service restart
service redis-server restart
sleep 1
supervisorctl restart all
sleep 1
service nginx restart
