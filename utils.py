import os


def file_exists(filename):
    return os.path.exists(filename)


def get_env(container):
    env = container["Config"]["Env"]
    return dict(map(lambda var: var.split("=", 1), env))


def get_ssl(path, domain):
    """ Find both SSL certificate and key inside the directory
    Files should be named after the host name with ".crt" and ".key"
    extensions.

    If a certificate is found for a parent domain, it will be used as a
    wildcard certificate with no further check.
    """
    parts = domain.split(".")
    while parts:
        domain = ".".join(parts)
        if os.path.exists(os.path.join(path, "%s.crt" % domain)):
            return "%s.crt" % domain, "%s.key" % domain
        parts.pop(0)
