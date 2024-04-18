import fri3d.ui

try:
    import fri3d.hardware_test
    fri3d.hardware_test.test()
except:
    pass


fri3d.ui.center_text('REPL')