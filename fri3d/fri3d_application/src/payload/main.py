# Hello and welcome to the code of the Fri3d Badge!
# You have located the main entrypoint where the code of your badge is launched from.
# Feel free to modify this file or any of the files in the fri3d package.

# In case you mess up, just delete this file using the REPL, and it will be restored to the original state.
# Similarly, if you delete the fri3d or user package it will also get restored to its original state

# If you are looking to add an app of your own, you probably don't want to edit the fri3d package but add it as a
# subpackage in the user package. Read more information on how to do this here:
#
# https://...

import logging

from fri3d.application import Application


# If you want you can increase the log output level here
logging.basicConfig(level=logging.WARNING, force=True)

app_main = Application()
app_main.run()
