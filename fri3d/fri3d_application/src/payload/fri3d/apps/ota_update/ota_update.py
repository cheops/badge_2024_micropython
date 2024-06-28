import asyncio
import lvgl as lv
import requests
import ota.status
import ota.update
import semver

from fri3d.application import App, AppInfo, Managers
from fri3d.version import version as current_version
from p0tat0.badge import badge_type, FRI3D_BADGE_2022, FRI3D_BADGE_2024
from fri3d.application.wifi_manager import WifiManager
from fri3d.utils.python_ext import cmp_to_key


class OtaUpdate(App):
    def __init__(
            self,
            info: AppInfo,
            managers: Managers,
    ):
        super().__init__(info, managers)

    async def current_version(self):
        screen = lv.screen_active()

        if self.ota_cabapble():
            self.btn_check = lv.button(screen)
            lbl_check = lv.label(self.btn_check)
            lbl_check.set_text("Check online")
            lbl_check.center()
            self.btn_check.align(lv.ALIGN.RIGHT_MID, -20, 40)
            self.btn_check.add_event_cb(self.btn_check_click, lv.EVENT.CLICKED, None)
        else:
            self.not_supported_lbl = lv.label(screen)
            self.not_supported_lbl.set_text("Ota not supported")
            self.not_supported_lbl.align(lv.ALIGN.RIGHT_MID, -20, 0)
        
        self.btn_cancel = lv.button(screen)
        lbl_cancel = lv.label(self.btn_cancel)
        lbl_cancel.set_text("Cancel")
        lbl_cancel.center()
        self.btn_cancel.align(lv.ALIGN.LEFT_MID, 20, 40)

        self.label = lv.label(screen)
        self.label.set_text("Current Version")
        self.label.align(lv.ALIGN.TOP_MID, 0, 5)

        self.label_version = lv.label(screen)
        self.label_version.set_text(current_version)
        self.label_version.align_to(self.label, lv.ALIGN.OUT_BOTTOM_MID, 0, 5)
        self.label_version.set_style_bg_color(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN)
        self.label_version.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)

        
        self.running = True
        while self.running:
            await asyncio.sleep(0.1)

    def btn_check_click(self, event):
        self.logger.debug("checking for newer version")
        with WifiManager() as wm:
            user = "cheops"
            repo = "fri3d-ota"
            board_name = self._get_board_name()
        
            self.available_versions_sorted, self.board_versions = self.fetch_available_ota_versions(user, repo, board_name)
        self.logger.debug("available versions: %s", self.available_versions_sorted)

        self.versions_info()

        screen = lv.screen_active()

        self.label_available = lv.label(screen)
        self.label_available.set_text("Available versions")
        self.label_available.align_to(self.label_version, lv.ALIGN.OUT_BOTTOM_MID, 0, 5)

        self.drop_down = lv.dropdown(screen)
        self.drop_down.set_options("\n".join(self.available_versions_sorted))
        self.drop_down.add_event_cb(self.drop_down_change, lv.EVENT.VALUE_CHANGED, None)
        self.drop_down.align_to(self.label_available, lv.ALIGN.OUT_BOTTOM_MID, 0, 5)

        self.selected_version = self.available_versions_sorted[0]
        self.logger.debug('selected_version: %s', self.selected_version)

        self.btn_check.delete()

        self.btn_update = lv.button(screen)
        lbl_update = lv.label(self.btn_update)
        lbl_update.set_text("Update")
        lbl_update.center()
        self.btn_update.align(lv.ALIGN.RIGHT_MID, -20, 40)
        self.btn_update.add_event_cb(self.btn_update_click, lv.EVENT.CLICKED, None)        

    def drop_down_change(self, event):
        index = self.drop_down.get_selected()
        self.selected_version = self.available_versions_sorted[index]
        # longest = len(max(self.available_versions_sorted, key=len))  # calculate len of longest version string
        # self.logger.debug
        # selected_version = " "*longest  # should be large enough to store the option
        # self.drop_down.get_selected_str(selected_version, len(selected_version))
        # self.selected_version = selected_version.strip()  # .strip() removes trailing spaces
        self.logger.debug('selected_version: %s', self.selected_version)

    def btn_update_click(self, event):
        self.logger.info("we will updgrade from current %s to %s", current_version, self.selected_version)
        u = self.board_versions[self.selected_version]["micropython.bin"]
        self.logger.debug(u)
        
        with WifiManager() as wm:
            headers = {"User-Agent": "micropython", "Accept": "application/vnd.github.raw+json"}
            ota.update.from_file(url=u['url'], length=u['size'], headers=headers)
    
    def versions_info(self):
        latest_version = self.available_versions_sorted[0]

        c = semver.compare(latest_version, current_version)
        if c > 0:
            self.logger.info("we can updgrade from current %s to %s", current_version, latest_version)
        elif c == 0:
            self.logger.debug("running latest version: %s", latest_version)
        else:
            self.logger.debug("current %s is newer than available %s", current_version, latest_version)

    async def start(self):
        self.logger.info("Launching %s", self.name)
        self.current_version_task = asyncio.create_task(self.current_version())

    async def stop(self):
        self.running = False
        await self.current_version_task

        self.label.delete()
        self.label_version.delete()
        self.btn_cancel.delete()
        if self.ota_cabapble():
            self.btn_check.delete()
        else:
            self.not_supported_lbl.delete()

    @staticmethod
    def ota_cabapble():
        return ota.status.ready()

    @staticmethod
    def _get_board_name():
        if badge_type == FRI3D_BADGE_2022:
            return 'fri3d_badge_2022'
        elif badge_type == FRI3D_BADGE_2024:
            return 'fri3d_badge_2024'
        else:
            raise(OSError("Unknown badge type"))

    def github_json_tree_to_dict(self, json:str) -> dict:
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
            # self.logger.debug(file["path"])
            sp = file["path"].split("/")
            # self.logger.debug(sp)
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

    def fetch_available_ota_versions(self, user:str, repo:str, board_name:str) -> tuple[str, dict]:
        """return a sorted list of available versions and dict of all files for all these versions

        expected repository layout:
            ota/board_name/version/<files>

        needs active internet connection when making this call

        param: user: github username of the ota repository
            repo: github repository of the ota repository
            board_name: board name to search for in the repository tree
        returns: available_versions_sorted, board_versions
        """
        url = f"https://api.github.com/repos/{user}/{repo}/git/trees/main?recursive=1"
        self.logger.debug(url)
        headers = {"User-Agent": "micropython", "Accept": "application/vnd.github+json"}
        r = requests.get(url, headers=headers)
        #logger.debug(r.text)
        res = r.json()
        
        repo_c = self.github_json_tree_to_dict(res)
        #logger.debug(repo_c)
        
        board_versions = repo_c["ota"][board_name]

        available_versions_sorted = sorted(list(board_versions.keys()), key=cmp_to_key(semver.compare), reverse=True)

        return available_versions_sorted, board_versions
