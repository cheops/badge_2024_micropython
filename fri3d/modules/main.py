import fri3d.ui
from fri3d.ota_upgrade import confirm_boot

confirm_boot()

try:
    import fri3d.hardware_test
    fri3d.hardware_test.test()
except:
    pass


fri3d.ui.center_text('REPL')