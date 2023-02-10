import maya.cmds as cmd
from maya import mel


# ----------------------------------------------------------------------------

SHELF_NAME = "Facial_Controller_Data_Collector"
SHELF_TOOL = {
    "label": "Facial_Controller_Data_Collector",
    "command": "import data_collector_ui; data_collector_ui.delete(); reload(data_collector_ui); "
               "data_collector_ui.create(); reload(utils)",
    "annotation": "Data collector for Metahuman face rig controllers",
    "image1": "tool.png",
    "imageOverlayLabel": "",
    "sourceType": "python",
    "overlayLabelColor": [1, 1, 1],
    "overlayLabelBackColor": [0, 0, 0, 0],
}

# ----------------------------------------------------------------------------


def shelf():
    """
    Add a new shelf in Maya with the tools that is provided in the SHELF_TOOL
    variable. If the tab exists it will be checked to see if the button is
    already added. If this is the case the previous button will be deleted and
    a new one will be created in its place.
    """
    # get top shelf
    gShelfTopLevel = mel.eval("$tmpVar=$gShelfTopLevel")

    # get top shelf names
    shelves = cmd.tabLayout(gShelfTopLevel, query=1, ca=1)

    # create shelf
    if SHELF_NAME not in shelves:
        cmd.shelfLayout(SHELF_NAME, parent=gShelfTopLevel)

    # get existing members
    names = cmd.shelfLayout(SHELF_NAME, query=True, childArray=True) or []
    labels = [cmd.shelfButton(n, query=True, label=True) for n in names]

    # delete existing button
    if SHELF_TOOL.get("label") in labels:
        index = labels.index(SHELF_TOOL.get("label"))
        cmd.deleteUI(names[index])

    # add button
    cmd.shelfButton(style="iconOnly", parent=SHELF_NAME, **SHELF_TOOL)


if __name__ == "__main__":
    print 'this is main'
    shelf()
