import maya.cmds as cmd

import data_collector_install


if not cmd.about(batch=True):
    cmd.evalDeferred(data_collector_install.shelf)

print "INITIALIZING"
