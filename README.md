Jinja configuration templates for Docker
========================================

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
