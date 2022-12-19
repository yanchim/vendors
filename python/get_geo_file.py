#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from urllib import request

"""
python get_geo_file.py
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


DAT_URL_DICT = {
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

MMDB_URL_DICT = {
    "github": [
        "https://github.com/P3TERX/GeoLite.mmdb/releases/latest/download/GeoLite2-Country.mmdb"
    ],
    "ghproxy": [
        "https://ghproxy.com/https://github.com/P3TERX/GeoLite.mmdb/releases/latest/download/GeoLite2-Country.mmdb"
    ],
}


def get_url(where, ext):
    """
    :return: url that str matches
    """
    if ext == "dat":
        return DAT_URL_DICT[where]
    if ext == "mmdb":
        return MMDB_URL_DICT[where]


parser = argparse.ArgumentParser(description="Get latest geo files.", add_help=True)
parser.add_argument(
    "-s",
    "--source",
    default="ghproxy",
    nargs="?",
    help="cdn, github or ghproxy, default 'ghproxy'.",
)
parser.add_argument(
    "-f",
    "--format",
    default="dat",
    nargs="?",
    help="dat or mmdb, default 'dat'",
)
parser.add_argument(
    "-p", "--path", required=True, nargs=1, help="The path to update geo files"
)

args = parser.parse_args()

urls = get_url(args.source, args.format)
for url in urls:
    geo_file = update_geo_file(url, args.path[0])
