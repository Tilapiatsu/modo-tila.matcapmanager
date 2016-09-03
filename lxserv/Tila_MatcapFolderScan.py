import lx
import lxu.command

import Tila_MatcapManagerModule as t

class CmdMyCustomCommand(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('silent',lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def basic_Execute(self, msg, flags):
        reload(t)

        t.generateFormTemplate(self.dyna_Bool(0))


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(CmdMyCustomCommand, "tila.matcap.folderscan")