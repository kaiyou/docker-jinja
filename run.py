#!/usr/local/bin/python3

import docker
import jinja2
import json
import argparse
import os
import sys
import signal


def loop(client, src, dst, react_to, notify):
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
            for container in notify:
                client.kill(container, signal.SIGHUP)


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
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Docker socket URL")
    parser.add_argument("src", help="Source directory for the templates")
    parser.add_argument("dst", help="Destination directory")
    parser.add_argument("-t", "--type", nargs="+", help="Event type")
    parser.add_argument("-n", "--notify", nargs="+", help="Notify containers")
    args = parser.parse_args()
    client = docker.Client(version="1.18", base_url=args.url)
    loop(client, args.src, args.dst, args.type, args.notify)
