import lx
from Tila_MatcapManagerModule import dialog
import lxu.command
import os

import Tila_MatcapManagerModule as t

class CmdMyCustomCommand(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('matcapFolderIndex', lx.symbol.sTYPE_INTEGER)


    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO


    def basic_Enable(self, msg):
        return True


    def cmd_Interact(self):
        pass


    def basic_Execute(self, msg, flags):
        reload(t)

        print t.renderer_path

        if self.dyna_Int(0) == 0:
            dialog.open_folder(t.matcap_path)
        elif self.dyna_Int(0) == 1:
            lx.eval('scene.open "%s" normal' % t.renderer_path)


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(CmdMyCustomCommand, "tila.matcap.open")