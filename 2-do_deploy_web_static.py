#!/usr/bin/python3
"""Fabric script to deploy a compressed archive to web servers"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['34.224.94.42', '52.204.18.168']


def do_deploy(archive_path):
    """Deploy archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        no_ext_name = archive_name.split(".")[0]
        path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext_name))
        run('tar -xzf /tmp/{} -C {}{}/'.
            format(archive_name, path, no_ext_name))
        run('rm /tmp/{}'.format(archive_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext_name))
        run('rm -rf {}{}/web_static'.format(path, no_ext_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.
            format(path, no_ext_name))
        return True
    except Exception as e:
        return False
