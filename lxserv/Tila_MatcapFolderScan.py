import lx
import lxifc
import lxu.command
import modo
import os
from os.path import isfile


import Tila_MatcapManagerModule

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
        reload(Tila_MatcapManagerModule)
        t = Tila_MatcapManagerModule

        t.generateForm()


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(CmdMyCustomCommand, "tila.matcapfolderscan")