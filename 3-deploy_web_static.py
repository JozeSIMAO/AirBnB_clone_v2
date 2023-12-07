#!/usr/bin/python3
"""Fabric script for full deployment"""
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['100.27.13.53', '100.25.37.138']
env.user = 'ubuntu'
env.key_filename = 'my_ssh_private_key'


def do_pack():
    """Create a compressed archive of web_static contents"""
    try:
        local("mkdir -p versions")
        t_format = "%Y%m%d%H%M%S"
        t_now = datetime.utcnow().strftime(t_format)
        archive_path = "versions/web_static_{}.tgz".format(t_now)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Deploy archive to web servers"""
    if not archive_path or not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        no_ext_name = archive_name.split(".")[0]
        remote_path = "/data/web_static/releases/{}/".format(no_ext_name)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(remote_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, remote_path))

        run("rm /tmp/{}".format(archive_name))
        run("mv {}web_static/* {}".format(remote_path, remote_path))
        run("rm -rf {}web_static".format(remote_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(remote_path))

        return True
    except Exception as e:
        return False


def deploy():
    """Full deployment process"""
    archive_path = do_pack()
    if not archive_path:
        print("Failed to create archive.")
        return False

    return do_deploy(archive_path)
