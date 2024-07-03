import logging
import aiohttp
import ota.status
import semver

from p0tat0.badge import badge_type, FRI3D_BADGE_2022, FRI3D_BADGE_2024
from fri3d.utils.python_ext import cmp_to_key
from fri3d.application.wifi_manager import WifiManager


logger = logging.getLogger('fri3d.apps.ota_update.ota_helper')


def ota_cabapble():
    return ota.status.ready()

def get_board_name():
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
        # logger.debug(file["path"])
        sp = file["path"].split("/")
        # logger.debug(sp)
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

async def afetch_available_ota_versions() -> tuple[str, dict]:
    """return a sorted list of available versions and dict of all files for all these versions

    expected repository layout:
        ota/board_name/version/<files>

    needs active internet connection when making this call

    param: user: github username of the ota repository
        repo: github repository of the ota repository
        board_name: board name to search for in the repository tree
    returns: available_versions_sorted, board_versions
    """
    user = "cheops"
    repo = "fri3d-ota"
    board_name = get_board_name()
    
    url = f"https://api.github.com/repos/{user}/{repo}/git/trees/main?recursive=1"
    logger.debug(url)
    headers = {"User-Agent": "micropython", "Accept": "application/vnd.github+json"}

    async with WifiManager():
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as r:
                code: int = r.status
                if code != 200:
                    r_text = await r.text()
                    print(r_text)
                    await r.wait_closed()
                    raise ValueError(f"HTTP Error: {code}")
                json_body = await r.json()
    
    repo_c = github_json_tree_to_dict(json_body)
    #logger.debug(repo_c)
    
    board_versions = repo_c["ota"][board_name]

    available_versions_sorted = sorted(list(board_versions.keys()), key=cmp_to_key(semver.compare), reverse=True)

    return available_versions_sorted, board_versions

async def aupdate_from_url(url:str, length:int, progress_cb):
    async with WifiManager():
        headers = {"User-Agent": "micropython", "Accept": "application/vnd.github.raw+json"}
        ota.update.from_file(
            url=url, 
            length=length, 
            headers=headers, 
            reboot=False, 
            progress_cb=progress_cb
        )
