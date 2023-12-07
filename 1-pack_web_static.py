#!/usr/bin/python3
"""Fabric script to compress contents of web_static folder"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """Create a compressed archive of web_static contents"""
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(current_time)

        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_name))

        return archive_name
    except Exception as e:
        return None
