Jinja configuration templates for Docker
========================================

*Warning: this script is still an early version and should only be used
for production with great care and much testing. For instance, exceptions
are not handled yet and the container will crash in many cases.*

**Security warning: this script is mostly intended for devops under the
asumption that templates are managed with the same security policy as the
script itself. The ``utils`` module that is passed to the Jinja renderer
makes executing arbitrary code from the template a piece of cake.**

Introduction
------------

This project is based on the awesome ``tiller`` principle and the amazing
``docker-gen`` by jwilder. It ships as a Docker containers that listens
on the Docker socket for specific events then walk through a directory
and renders each configuration file through the Jinja templating engine.

This behavior can easily be leveraged to dynamically reconfigure other
Docker containers or hosts to adapt to changing contexts. For instance :

 - run a dynamic DNS server replying to Docker container names ;
 - run a dynamic Web reverse proxy (just like ``jwilder/nginx-proxy`` does) ;
 - run a dynamic [whatever] reverse-proxy ;
 - dynamically monitor all containers, build Web pages, or pour coffee based
   on the list and configuration of running containers.

DNS Resolver for containers
---------------------------

Simply put the following hosts file template inside your source directory:

    127.0.0.1	localhost

    {% for container in containers %}
    {{ container["NetworkSettings"]["IPAddress"] }}	{{ container["Name"][1:] }}
    {% endfor %}

Run the configuration parser:

    $ docker run -d --name=config-parser -t \
    -v /path/to/src:/src \
    -v /path/to/dst:/dst \
    kaiyou/docker-jinja -n dnsmasq

Then run the appropriate dnsmasq container:

    $ docker run --name=dnsmasq \
    -v /path/to/dst/hosts:/hosts \
    -p 53:53/udp \
    yourfavourite/dnsmasq --no-resolv --no-hosts --addn-hosts=/hosts

You may now query your containers:

    $ dig A dnsmasq @127.0.0.1
    ;; QUESTION SECTION:
    ;dnsmasq.			IN	A

    ;; ANSWER SECTION:
    dnsmasq.		0	IN	A	10.0.0.2

Dynamic reverse proxy
---------------------

The following configuration mimics the dynamic behavior of ``jwilder/nginx-proxy``.

    {% for container in containers %}
    {% set env = utils.get_env(container) %}
    {% set hosts = env.get("VIRTUAL_HOST", "").split(",") %}

    {% if hosts[0] %}

    upstream {{ container["Id"] }} {
    	server {{ container["NetworkSettings"]["IPAddress"] }}:{{ port }}:80;
    }

    {% for host in hosts %}

    server {
    	server_name {{ host }};
    	listen [::]:80;

      location / {
    		proxy_pass http://{{ container["Id"] }};
    	}
    }
    {% endfor %}
    {% endif %}
    {% endfor %}
