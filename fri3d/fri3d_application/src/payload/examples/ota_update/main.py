import logging
logging.basicConfig(level=logging.DEBUG, force=True)

import requests

import ota.status
import ota.update
import semver

print("running main.py")

from p0tat0.badge import badge_type, FRI3D_BADGE_2022, FRI3D_BADGE_2024

from fri3d.wifi_manager import WifiManager

from fri3d.version import version as fri3d_version

logger = logging.Logger('examples.ota_update')


def _get_board_name():
    if badge_type == FRI3D_BADGE_2022:
        return 'fri3d_badge_2022'
    elif badge_type == FRI3D_BADGE_2024:
        return 'fri3d_badge_2024'
    else:
        raise(OSError("Unknown badge type"))



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
        #logger.debug(file["path"])
        sp = file["path"].split("/")
        #logger.debug(sp)
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
    logger.debug(url)
    headers = {"User-Agent": "micropython", "Accept": "application/vnd.github+json"}
    r = requests.get(url, headers=headers)
    #logger.debug(r.text)
    res = r.json()
    
    repo_c = github_json_tree_to_dict(res)
    #logger.debug(repo_c)
    
    board_versions = repo_c["ota"][board_name]
    
    logger.debug(f"available versions: {list(board_versions.keys())}")
    
    latest_v = next(iter(board_versions))
    for v in board_versions:
        if semver.compare(v, latest_v) > 0:
            latest_v = v
    
    return latest_v, board_versions[latest_v]



board_name = _get_board_name()

ota_cap = ota.status.ready()
logger.debug(f"ota update capable: {ota_cap} ")
logger.debug(f"fri3d badge current version: {fri3d_version}")
logger.debug(f"{board_name=}")

if not ota_cap:
    logger.warning("badge does not support ota update")

else:
    # this enables wifi in the ContextManager
    with WifiManager() as wm:

        user = "cheops"
        repo = "fri3d-ota"
        
        latest_version, latest_files = fetch_latest_ota_version(user, repo, board_name)

        logger.debug(f"{latest_version=}")
    
        if semver.compare(latest_version, fri3d_version) > 0:
            logger.debug(f"we can updgrade from current {fri3d_version} to {latest_version}")
            u = latest_files["micropython.bin"]
            logger.debug(u)
            headers = {"User-Agent": "micropython", "Accept": "application/vnd.github.raw+json"}
            ota.update.from_file(url=u['url'], length=u['size'], headers=headers)

        else:
            logger.debug(f"current {fri3d_version} is equal or newer than available {latest_version}")