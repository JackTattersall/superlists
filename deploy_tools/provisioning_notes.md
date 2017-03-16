Provisioning a new site
=======================

## Required packages:
	* nginx
	* python 3
	* git
	* pip
	* virtualenv

eg, on ubuntu:
	sudo apt-get install nginx git python3 python3-pip
	sudo pip3 install virtualenv

## Nginx Virtual Host config
	* see nginx.template.conf
	* replace SITENAME with, sitename
eg
    sed "s/SITE/superlists.chillyroad.info/g" \
    deploy_tools/nginx.template.conf | sudo tee \
    /etc/nginx/sites-available/superlists.chillyroad.info

## Simlink sites-available to sites-enabled
eg
    sudo ln -s ../sites-available/superlists.chillyroad.info \
    /etc/nginx/sites-enabled/superlists.chillyroad.info
	
## Upstart job
	* see gunicorn-systemctl.template.service
	* replace Path names
eg
    sed "s/SITE/superlists.chillyroad.info/g" \
    deploy_tools/gunicorn-systemctl.template.service | sudo tee \
    /lib/systemd/system/SITE.service

## Folder structure
Assume we hav a user account at /home/username

/home/username
~ sites
  ~ SITENAME
    ~ SiteType eg prod/stage/uat
      ~ database
      ~ source
      ~ static
      ~ virtualenv

## Useful commands
    * run fab by
    fab -i /Users/administrator/Desktop/PemKeys/pythonServer.pem -u ubuntu deploy:host=ubuntu@superlists.chillyroad.info
