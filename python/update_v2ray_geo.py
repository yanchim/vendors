#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from urllib import request

"""
python update_v2ray_geo.py
"""


def callback(blocknum, blocksize, totalsize):
    """
    :param blocknum: already downloaded block number
    :param blocksize: block size
    :param totalsize: total size
    :return:
    """
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print("\r{:.2f}%".format(percent), end="", flush=True)


def update_geo_file(url, path):
    """
    Overwrite old geo files with new geo files.
    """
    try:
        name = url.split("/")[-1]
        print("\n----------")
        print("Downloading from: " + url)
        print("Downloading " + name + " to " + path + name)
        request.urlretrieve(url, path + name, callback)
    except Exception:
        print(Exception)


URL_DICT = {
    "cdn": [
        "https://cdn.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/geoip.dat",
        "https://cdn.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/geosite.dat",
    ],
    "github": [
        "https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geoip.dat",
        "https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geosite.dat",
    ],
    "ghproxy": [
        "https://ghproxy.com/https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geoip.dat",
        "https://ghproxy.com/https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geosite.dat",
    ],
}


def get_url(str):
    """
    :return: url that str matches
    """
    return URL_DICT[str]


parser = argparse.ArgumentParser(
    description="Get latest V2Ray geo files.", add_help=True
)
parser.add_argument(
    "-s",
    "--source",
    default="ghproxy",
    nargs="?",
    help="cdn, github or ghproxy, default 'ghproxy'",
)
parser.add_argument(
    "-p", "--path", required=True, nargs=1, help="The path to update geo files"
)

args = parser.parse_args()

urls = get_url(args.source)
for url in urls:
    geo_file = update_geo_file(url, args.path[0])
