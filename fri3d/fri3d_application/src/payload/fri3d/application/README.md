# Fri3d Badge Application

This package contains the main Fri3d Badge Application. It is as much an application as it is a framework. By using this
you will automatically have to use:

* LVGL
* The Fri3d `indev` driver
* `asyncio` (although you can ignore most of this if you want to)

If you don't want to use for example LVGL you are in the wrong place and will need to write your own application and
launch that one instead from `main.py`.

## Structure

The application consists of the following major parts

### Application setup

Initializes base functionality

* Setup LVGL
* Setup indev
* Create the different managers
* Launch default app

### WindowManager

Takes care of showing screens and navigating between them.

### AppManager

Detects and manages both builtin and user apps.

### ThemeManager

Manages the look & feel of the badge.

### Apps

Everything else in the application is pluggable by writing an app. Each app has a main entrypoint and will register at
least one screen with the WindowManager which is shown when launched. After that the app is responsible for all user
interactions.

An app should properly release resources when exited / paused. For example if it is showing flashing LEDs, it should
stop doing so as soon as it loses focus. There is no resource manager that will take care of this for you. Remember,
with great power comes great responsibility.

### Launcher

This is the default app. It allows the user to interact with the AppManager to launch other components. Every entry you
can see in the launcher is written as a separate app so you can also launch it from elsewhere

## Miscellaneous

### Default app

You can modify which app gets launched at startup by passing the parameter `default_app` in `main.py` like so

```python
app_main = Application(default_app='user.example_app')
app_main.run()
```

This means that this app will also be jumped to whenever the Menu/Select button is pressed, so you could write your own
launcher!
