#!/usr/local/bin/python3

import docker
import jinja2
import json
import os
import sys


def loop(client, react_to, src, dst):
    """ Loop through Docker events and react to proper ones.
    """
    for event in client.events():
        obj = json.loads(event.decode("utf-8"))
        if obj["status"] not in react_to:
            print("Gathering container data...")
            containers = [client.inspect_container(container["Id"])
                          for container in client.containers()]
            print("Parsing templates...")
            walk_convert(containers, src, dst)


def walk_convert(containers, src, dst):
    """ Walk through all subdirectories and convert files.
    """
    for dirpath, dirnames, filenames in os.walk(src):
        relpath = os.path.relpath(src, dirpath)
        for dirname in dirnames:
            os.makedirs(os.path.join(dst, relpath, dirname), exit_ok=True)
        for filename in filenames:
            print("Rendering {0}".format(filename))
            with open(os.path.join(dirpath, filename), "r") as src_file:
                template = jinja2.Template(src_file.read())
            with open(os.path.join(dst, relpath, filename), "w") as dst_file:
                dst_file.write(template.render(containers = containers))


if __name__ == "__main__":
    url, src, dst = sys.argv[1:4]
    react_to = sys.argv[4:]
    client = docker.Client(version="1.18", base_url=url)
    loop(client, react_to, src, dst)
