import lx
from Tila_MatcapManagerModule import dialog
import lxu.command
import modo
import os
from os.path import isfile

import Tila_MatcapManagerModule as t

class CmdMyCustomCommand(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def basic_Execute(self, msg, flags):
        reload(t)

        curr_path = os.path.dirname(os.path.realpath(__file__))
        matcap_path = os.path.join(dialog.parentPath(curr_path), "Matcaps")

        dialog.open_folder(matcap_path)


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(CmdMyCustomCommand, "tila.matcap.folderopen")