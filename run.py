#!/usr/local/bin/python3
#
# "THE BEER-WARE LICENSE" (Revision 42):
# kaiyou wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
#

import docker
import jinja2
import json
import argparse
import os
import sys
import signal
import utils
import pprint


def loop(client, src, dst, react_to, notify, command):
    """ Loop through Docker events and react to proper ones.
    """
    walk_convert(client, src, dst)
    run_post(client, src, dst, notify, command)
    for event in client.events():
        obj = json.loads(event.decode("utf-8"))
        if "Type" not in obj or obj["Type"] == "container":
            if obj["status"] in react_to:
                walk_convert(client, src, dst)
                run_post(client, src, dst, notify, command)


def run_post(client, src, dst, notify, command):
    """ Run post generation operations
    """
    if notify:
        print("Notifying containers: {0}".format(notify))
        send_notify(client, notify)
    if command:
        print("Running system command: {0}".format(command))
        os.system(command)


def send_notify(client, containers):
    """ Send SIGHUP to the given containers.
    """
    if containers is not None:
        for container in containers:
            try:
                client.kill(container, signal.SIGHUP.value)
            except docker.errors.NotFound:
                print("Container {0} not found".format(container))


def walk_convert(client, src, dst):
    """ Walk through all subdirectories and convert files.
    """
    print("Gathering container data...")
    env = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True
    )
    containers = [client.inspect_container(container["Id"])
                  for container in client.containers()]
    networks = [client.inspect_network(network["Id"])
                for network in client.networks()]
    os.makedirs(dst, exist_ok=True)
    for dirpath, dirnames, filenames in os.walk(src):
        relpath = os.path.relpath(dirpath, src)
        for dirname in dirnames:
            os.makedirs(os.path.join(dst, relpath, dirname), exist_ok=True)
        for filename in filenames:
            print("Rendering {0}".format(os.path.join(relpath, filename)))
            with open(os.path.join(dirpath, filename), "r") as src_file:
                template = env.from_string(src_file.read())
            with open(os.path.join(dst, relpath, filename), "w") as dst_file:
                dst_file.write(template.render(
                    containers=containers, networks=networks, utils=utils))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Docker socket URL")
    parser.add_argument("src", help="Source directory for the templates")
    parser.add_argument("dst", help="Destination directory")
    parser.add_argument("-i", "--init", required=False, help="Init command")
    parser.add_argument("-t", "--type", nargs="+", help="Event type")
    parser.add_argument("-n", "--notify", nargs="+", help="Notify containers")
    parser.add_argument("-c", "--command", required=False, help="Notify command")
    args = parser.parse_args()
    if args.init:
        os.system(args.init)
    client = docker.Client(base_url=args.url)
    loop(client, args.src, args.dst, args.type, args.notify, args.command)
