import asyncio
import lvgl as lv
import ota.status
import ota.update
import semver

from fri3d.application import App, AppInfo, Managers
from fri3d.version import version as current_version
from .ota_helper import afetch_available_ota_versions, aupdate_from_url, ota_cabapble


class OtaUpdate(App):
    def __init__(
            self,
            info: AppInfo,
            managers: Managers,
    ):
        super().__init__(info, managers)

    async def start(self):
        self.logger.info("Launching %s", self.name)
        self.ota_update_main_task = asyncio.create_task(self.ota_update_main())

    async def stop(self):
        self.should_stop = True
        await self.ota_update_main_task
        self.screen_cleanup()

    async def ota_update_main(self):
        self.should_stop = False
        self.btn_check_clicked = asyncio.ThreadSafeFlag()
        self.bnt_cancel_clicked = asyncio.ThreadSafeFlag()
        self.btn_update_clicked = asyncio.ThreadSafeFlag()
        self.drop_down_changed = asyncio.ThreadSafeFlag()
        
        self.screen_initial_layout()
        
        while True:
            if self.bnt_cancel_clicked.state:
                self.bnt_cancel_clicked.clear()
                self.action_cancel()
                break
            
            if self.btn_check_clicked.state:
                self.btn_check_clicked.clear()
                await self.action_check_versions()
            
            if self.drop_down_changed.state:
                self.drop_down_changed.clear()
                self.action_drop_down_change()

            if self.btn_update_clicked.state:
                self.btn_update_clicked.clear()
                await self.action_update()
            
            if self.should_stop:
                break
            
            await asyncio.sleep(0)
            

    # screen construction functions
    ###############################
    def screen_initial_layout(self):
        screen = lv.screen_active()

        # Create a container with ROW flex direction
        self.cont_row = lv.obj(screen)
        self.cont_row.set_width(screen.get_width())
        self.cont_row.set_height(lv.SIZE_CONTENT)
        self.cont_row.align(lv.ALIGN.BOTTOM_MID, 0, -15)
        self.cont_row.set_flex_flow(lv.FLEX_FLOW.ROW)
        self.cont_row.set_style_flex_main_place(lv.FLEX_ALIGN.SPACE_EVENLY, 0)
        self.cont_row.set_style_pad_hor(5, lv.PART.MAIN)
        self.cont_row.set_style_pad_ver(5, lv.PART.MAIN)
        self.cont_row.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.cont_row.set_style_border_width(0,lv.PART.MAIN)

        self.btn_cancel = lv.button(self.cont_row)
        self.btn_cancel.set_size(lv.SIZE_CONTENT, lv.SIZE_CONTENT)
        self.btn_cancel.set_style_pad_ver(5, lv.PART.MAIN)
        lbl_cancel = lv.label(self.btn_cancel)
        lbl_cancel.set_text("Cancel")
        lbl_cancel.center()
        self.btn_cancel.add_event_cb(self.callback_btn_cancel_click, lv.EVENT.CLICKED, None)

        if ota_cabapble():
            self.btn_check = lv.button(self.cont_row)
            self.btn_check.set_size(lv.SIZE_CONTENT, lv.SIZE_CONTENT)
            self.btn_check.set_style_pad_ver(5, lv.PART.MAIN)
            lbl_check = lv.label(self.btn_check)
            lbl_check.set_text("Check online")
            lbl_check.center()
            self.btn_check.add_event_cb(self.callback_btn_check_click, lv.EVENT.CLICKED, None)
        else:
            self.not_supported_lbl = lv.label(self.cont_row)
            self.not_supported_lbl.set_text("Ota not supported")
        
        # Create a container with COLUMN flex direction
        self.cont_col = lv.obj(screen)

        self.cont_col.set_width(screen.get_width())
        self.cont_col.set_height(lv.SIZE_CONTENT)
        self.cont_col.align(lv.ALIGN.TOP_MID, 0, 5)

        self.cont_col.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.cont_col.set_style_flex_cross_place(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN)
        self.cont_col.set_style_flex_track_place(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN)
        self.cont_col.set_style_pad_row(5, lv.PART.MAIN)

        self.cont_col.set_style_pad_hor(0, lv.PART.MAIN)
        self.cont_col.set_style_pad_ver(5, lv.PART.MAIN)
        self.cont_col.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.cont_col.set_style_border_width(0, lv.PART.MAIN)

        self.label = lv.label(self.cont_col)
        self.label.set_text("Current Version")
        self.label.set_size(lv.SIZE_CONTENT, lv.SIZE_CONTENT)

        self.label_version = lv.label(self.cont_col)
        self.label_version.set_text(current_version)
        self.label_version.set_size(lv.SIZE_CONTENT, lv.SIZE_CONTENT)
        self.label_version.set_style_bg_color(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN)
        self.label_version.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)

    def screen_spinner_start(self, label_text):
        screen = lv.screen_active()

        self.cont_spinner = lv.obj(screen)
        self.cont_spinner.set_size(screen.get_width(), screen.get_height())
        self.cont_spinner.center()
        self.cont_spinner.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)

        size = int(min(screen.get_height()/2, screen.get_width()/2))
        spinner = lv.spinner(self.cont_spinner)
        spinner.set_size(size, size)
        spinner.align(lv.ALIGN.CENTER, 0, -10)
        spinner.set_anim_params(1_000, 200)

        self.label5 = lv.label(self.cont_spinner)
        self.label5.set_text(label_text)
        self.label5.align(lv.ALIGN.BOTTOM_MID, 0, 0)
    
    def screen_spinner_stop(self):
        self.cont_spinner.delete()
    
    def screen_spinner_add_progress_bar_message(self, message):
        screen = lv.screen_active()
        self.bar = lv.bar(self.cont_spinner)
        self.bar.set_size(screen.get_width()-20, 20)
        self.bar.align_to(self.label5, lv.ALIGN.OUT_TOP_MID, 0, -5)
        self.bar.set_value(0, lv.ANIM.OFF)
        label = lv.label(self.cont_spinner)
        label.align_to(self.bar, lv.ALIGN.OUT_TOP_MID, 0, -5)
        label.set_text(message)
    
    def screen_spinner_set_progress_bar_value(self, value):
        if value != self.bar.get_value():
            self.logger.debug("progress bar value: %d", value)
            self.bar.set_value(value, lv.ANIM.OFF)
    
    def screen_update_available_versions(self):
        self.label_available = lv.label(self.cont_col)
        self.label_available.set_text("Available versions")
        self.label_available.set_size(lv.SIZE_CONTENT, lv.SIZE_CONTENT)

        self.drop_down = lv.dropdown(self.cont_col)
        self.drop_down.set_width(lv.pct(90))
        self.drop_down.set_options("\n".join(self.available_versions_sorted))
        self.drop_down.add_event_cb(self.callback_drop_down_change, lv.EVENT.VALUE_CHANGED, None)
        self.drop_down.set_selected(0)

        self.selected_version = self.available_versions_sorted[0]

        self.btn_check.delete()

        self.btn_update = lv.button(self.cont_row)
        self.btn_update.set_size(lv.SIZE_CONTENT, lv.SIZE_CONTENT)
        self.btn_update.set_style_pad_ver(5, lv.PART.MAIN)
        lbl_update = lv.label(self.btn_update)
        lbl_update.set_text("Update")
        lbl_update.center()
        self.btn_update.add_event_cb(self.callback_btn_update_click, lv.EVENT.CLICKED, None)

    def screen_error_label_show(self, err):
        if not hasattr(self, 'label_error'):
            self.label_error = lv.label(self.cont_col)
            self.label_error.set_height(lv.SIZE_CONTENT)
            self.label_error.set_width(lv.pct(100))
            self.label_error.set_long_mode(lv.label.LONG.WRAP)
            self.label_error.set_style_bg_color(lv.palette_main(lv.PALETTE.RED), lv.PART.MAIN)
            self.label_error.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.label_error.set_text(f"{type(err)}: {err.value}")
    
    def screen_error_label_remove(self):
        if hasattr(self, 'label_error'):
            self.label_error.delete()
            del self.label_error

    def screen_versions_info(self):
        if not hasattr(self, 'label_version_info'):
            self.label_version_info = lv.label(self.cont_col)
            self.label_version_info.set_height(lv.SIZE_CONTENT)
            self.label_version_info.set_width(lv.SIZE_CONTENT)
            self.label_version_info.set_style_bg_color(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN)
            self.label_version_info.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)

        c = semver.compare(self.selected_version, current_version)
        if c > 0:
            # newer
            self.label_version_info.set_text("newer-> upgrade")
            self.logger.info("we can updgrade from current %s to %s", current_version, self.selected_version)
        elif c == 0:
            # same
            self.label_version_info.set_text("same-> reinstall")
            self.logger.debug("running latest version: %s", self.selected_version)
        else:
            # older
            self.label_version_info.set_text("older-> downgrade")
            self.logger.debug("current %s is newer than available %s", current_version, self.selected_version)

    def screen_cleanup(self):
        # TODO: remove objects from screen
        self.label.delete()
        self.label_version.delete()
        self.btn_cancel.delete()
        if self.ota_cabapble():
            self.btn_check.delete()
        else:
            self.not_supported_lbl.delete()


    # callback functions
    ####################
    def callback_btn_cancel_click(self, event):
        self.bnt_cancel_clicked.set()

    def callback_btn_check_click(self, event):
        self.btn_check_clicked.set()

    def callback_drop_down_change(self, event):
        self.drop_down_changed.set()

    def callback_btn_update_click(self, event):
        self.btn_update_clicked.set()


    # actions
    #########
    def action_cancel(self):
        self.logger.debug("cancel this screen")
        self.screen_cleanup()
        self.app_manager.run_app('')

    async def action_check_versions(self):
        try:
            self.screen_spinner_start("Downloading versions ...")
            self.available_versions_sorted, self.board_versions = await afetch_available_ota_versions()
            self.screen_spinner_stop()
            self.logger.debug("available versions: %s", self.available_versions_sorted)
            self.screen_error_label_remove()
            self.screen_update_available_versions()
            self.screen_versions_info()

        except Exception as err:
            self.logger.error("Failed getting ota versions %s", repr(err))
            self.screen_spinner_stop()
            self.screen_error_label_show(err)

    def action_drop_down_change(self):
        index = self.drop_down.get_selected()
        self.selected_version = self.available_versions_sorted[index]
        self.logger.debug('selected_version: %s', self.selected_version)
        self.screen_versions_info()

    async def action_update(self):
        self.screen_error_label_remove()
        self.screen_spinner_start("Updating ...")
        self.screen_spinner_add_progress_bar_message("[screen will freeze]")

        self.logger.info("we will updgrade from current %s to %s", current_version, self.selected_version)
        u = self.board_versions[self.selected_version]["micropython.bin"]
        self.logger.debug(u)
        
        try:
            await aupdate_from_url(u['url'], u['size'], self.screen_spinner_set_progress_bar_value)
            await asyncio.sleep(0.1)
            self.screen_spinner_stop()
            await asyncio.sleep(0.1)
            self.screen_spinner_start("Rebooting ...")
            await asyncio.sleep(0.1)
            await ota.status.aota_reboot(delay=3)

        except Exception as err:
            self.logger.error("Failed updating to '%s': %s", self.selected_version, err)
            self.screen_spinner_stop()
            self.screen_error_label_show(err)
