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
	* replace SITENAME with, sitename/ip
	
## Upstart job
	* see gunicorn-systemctl.template.service
	* replace Path names

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
