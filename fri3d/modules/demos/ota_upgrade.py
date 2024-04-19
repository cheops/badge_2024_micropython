import requests

import ota.status
import ota.update
import semver
from wifi_manager import WifiManager

from fri3d.badge import version as fri3d_version
from fri3d.badge.hardware import board_name

from fri3d import logging

log = logging.Log(__name__, level=logging.DEBUG)

def github_json_tree_to_dict(json:str) -> dict:
    """convert the json tree to a dict with every directory level as key
    paths are further analyzed
    blobs get as attributes: url, size
    
    example path in the tree: /ota/fri3d_badge_2024/0.0.1/micropython.bin
    becomes d = {'ota': {'fri3d_badge_2024': {'0.0.1': {'micropython.bin': {'url': 'https://', 'size': 1234}}}}}
    
    makes for easy selecting
    url = d['ota']['fri3d_badge_2024']['0.0.1']['micropython.bin']['url']
    version = d['ota']['fri3d_badge_2024']
    """
    repo_c = {}
    for file in json["tree"]:
        #log.debug(file["path"])
        sp = file["path"].split("/")
        #log.debug(sp)
        e = repo_c
        for i, p in enumerate(sp):
            if p in e:
                e = e[p]
            elif i < len(sp) - 1:
                e[p] = {}
                e = e[p]
            elif i == len(sp) - 1 and file["type"] == "blob":
                e[p] = {
                    "url": file["url"],
                    "size": file["size"],
                }
    return repo_c


def fetch_latest_ota_version(user:str, repo:str, board_name:str) -> tuple[str, dict]:
    """return latest version and dict of all files availabe in that version

    expected repository layout:
        ota/board_name/version/<files>

    needs active internet connection when making this call

    param: user: github username of the ota repository
           repo: github repository of the ota repository
           board_name: board name to search for in the repository tree
    returns: latests_version, latest_version_files
    """
    url = f"https://api.github.com/repos/{user}/{repo}/git/trees/main?recursive=1"
    log.debug(url)
    headers = {"User-Agent": "micropython", "Accept": "application/vnd.github+json"}
    r = requests.get(url, headers=headers)
    #log.debug(r.text)
    res = r.json()

    repo_c = github_json_tree_to_dict(res)
    #log.debug(repo_c)

    board_versions = repo_c["ota"][board_name]

    log.debug(f"available versions: {list(board_versions.keys())}")

    latest_v = next(iter(board_versions))
    for v in board_versions:
        if semver.compare(v, latest_v) > 0:
            latest_v = v
    
    return latest_v, board_versions[latest_v]




ota_cap = ota.status.ready()
log.debug(f"ota update capable: {ota_cap} ")
log.debug(f"fri3d badge current version: {fri3d_version}")
log.debug(f"{board_name=}")

if not ota_cap:
    log.warning("badge does not support ota update")

else:
    # this enables wifi in the ContextManager
    with WifiManager() as wm:

        user = "cheops"
        repo = "fri3d-ota"
        
        latest_version, latest_files = fetch_latest_ota_version(user, repo, board_name)

        log.debug(f"{latest_version=}")
    
        if semver.compare(latest_version, fri3d_version) > 0:
            log.debug(f"we can updgrade from current {fri3d_version} to {latest_version}")
            u = latest_files["micropython.bin"]
            log.debug(u)
            headers = {"User-Agent": "micropython", "Accept": "application/vnd.github.raw+json"}
            ota.update.from_file(url=u['url'], length=u['size'], headers=headers)

        else:
            log.debug(f"current {fri3d_version} is equal or newer than available {latest_version}")
