import os


def file_exists(filename):
    return os.path.exists(filename)


def get_env(container):
    env = container["Config"]["Env"]
    return dict(map(lambda var: var.split("=", 1), env))
