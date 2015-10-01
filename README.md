Jinja configuration templates for Docker
========================================

*Warning: this script is still an early version and should only be used
for production with great care and much testing. For instance, exceptions
are not handled yet and the container will crash in many cases.*

**Security warning: this script is mostly intended for devops under the
asumption that templates are managed with the same security policy as the
script itself. The ``utils`` module that is passed to the Jinja renderer
makes executing arbitrary code from the template a piece of cake.**

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
