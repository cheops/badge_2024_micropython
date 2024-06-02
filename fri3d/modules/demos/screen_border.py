import lvgl as lv

scr = lv.obj()

buf = lv.draw_buf_create(scr.get_width(),scr.get_height(),lv.COLOR_FORMAT.RGB565, lv.STRIDE_AUTO)

canvas = lv.canvas(scr)
canvas.set_draw_buf(buf)
canvas.center()

layer = lv.layer_t()
canvas.init_layer(layer)

dsc = lv.draw_rect_dsc_t()

dsc.bg_color = lv.color_hex(0xffbf00)
dsc.bg_opa = lv.OPA.COVER

dsc.border_color = lv.color_hex(0xd2222d)
dsc.border_side = lv.BORDER_SIDE.TOP | lv.BORDER_SIDE.LEFT | lv.BORDER_SIDE.RIGHT | lv.BORDER_SIDE.BOTTOM
dsc.border_width = 2
dsc.border_opa = lv.OPA.COVER

dsc.radius = 61

coor = lv.area_t()
coor.x1 = 0
coor.y1 = 0
coor.x2 = 295
coor.y2 = 239

lv.draw_rect(layer, dsc, coor)

canvas.finish_layer(layer)

lv.screen_load(scr)

# draw the buffers to the screen
lv.timer_handler_run_in_period(5)