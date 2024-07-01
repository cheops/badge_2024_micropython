import asyncio
import aiohttp
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

        self.should_stop = False
        self.btn_check_clicked = asyncio.ThreadSafeFlag()
        self.bnt_cancel_clicked = asyncio.ThreadSafeFlag()
        self.btn_update_clicked = asyncio.ThreadSafeFlag()

        self.initial_screen_layout()
        
        while True:
            if self.bnt_cancel_clicked.state:
                self.bnt_cancel_clicked.clear()
                self.logger.debug("cancel this screen")
                break
            
            if self.btn_check_clicked.state:
                self.btn_check_clicked.clear()
                await self.check_versions()
            
            if self.btn_update_clicked.state:
                self.btn_update_clicked.clear()
                await self.update()
            
            if self.should_stop:
                break
            
            await asyncio.sleep(0)
            


    def initial_screen_layout(self):
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
        self.btn_cancel.add_event_cb(self.btn_cancel_click, lv.EVENT.CLICKED, None)

        self.label = lv.label(screen)
        self.label.set_text("Current Version")
        self.label.align(lv.ALIGN.TOP_MID, 0, 5)

        self.label_version = lv.label(screen)
        self.label_version.set_text(current_version)
        self.label_version.align_to(self.label, lv.ALIGN.OUT_BOTTOM_MID, 0, 5)
        self.label_version.set_style_bg_color(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN)
        self.label_version.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)


    def update_screen_layout_available_versions(self):
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


    async def check_versions(self):
        user = "cheops"
        repo = "fri3d-ota"
        board_name = self._get_board_name()
        
        try:
            self.available_versions_sorted, self.board_versions = await self.afetch_available_ota_versions(user, repo, board_name)
            self.logger.debug("available versions: %s", self.available_versions_sorted)

            self.versions_info()
            self.update_screen_layout_available_versions()
        except Exception as err:
            self.logger.error("Failed getting ota versions %s", repr(err))


    def btn_cancel_click(self, event):
        self.logger.debug("Cancel button clicked")
        self.bnt_cancel_clicked.set()

    def btn_check_click(self, event):
        self.logger.debug("checking for newer version")
        self.btn_check_clicked.set()

    def drop_down_change(self, event):
        index = self.drop_down.get_selected()
        self.selected_version = self.available_versions_sorted[index]
        self.logger.debug('selected_version: %s', self.selected_version)

    def btn_update_click(self, event):
        self.btn_update_clicked.set()
    
    async def update(self):
        self.logger.info("we will updgrade from current %s to %s", current_version, self.selected_version)
        u = self.board_versions[self.selected_version]["micropython.bin"]
        self.logger.debug(u)
        
        try:
            async with WifiManager():
                headers = {"User-Agent": "micropython", "Accept": "application/vnd.github.raw+json"}
                await ota.update.afrom_url(url=u['url'], length=u['size'], headers=headers)
        except Exception as err:
            self.logger.error("Failed updating to '%s': %s", self.selected_version, err)
    
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
        self.should_stop = True
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

    async def afetch_available_ota_versions(self, user:str, repo:str, board_name:str) -> tuple[str, dict]:
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

        async with WifiManager():
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as r:
                    json_body = await r.json()
        
        repo_c = self.github_json_tree_to_dict(json_body)
        #logger.debug(repo_c)
        
        board_versions = repo_c["ota"][board_name]

        available_versions_sorted = sorted(list(board_versions.keys()), key=cmp_to_key(semver.compare), reverse=True)

        return available_versions_sorted, board_versions