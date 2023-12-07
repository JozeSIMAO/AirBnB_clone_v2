#!/usr/bin/python3
"""Fabric script to deploy a compressed archive to web servers"""

from fabric.api import env, put, run
from os.path import exists, join

env.hosts = ['100.27.13.53', '100.25.37.138']


def do_deploy(archive_path):
    """Deploy archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        no_ext_name = archive_name.split(".")[0]
        remote_path = "/data/web_static/releases/{}/".format(no_ext_name)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(remote_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, remote_path))

        # Check if 'web_static' directory exists inside the archive
        if not exists(join(remote_path, 'web_static')):
            return False

        run("rm /tmp/{}".format(archive_name))
        run("mv {}web_static/* {}".format(remote_path, remote_path))
        run("rm -rf {}web_static".format(remote_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(remote_path))

        return True
    except Exception as e:
        return False
