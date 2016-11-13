import lx
import modo
import lxu.command

import Tila_MatcapManagerModule as t
from Tila_MatcapManagerModule import user_value


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

        scn = modo.Scene()

        try:
            enable = scn.item(t.matcap_name).channel('enable').get()
            scn.item(t.matcap_name).channel('enable').set(not enable)
        except:
            pass

        try:
            enable = scn.item(t.matcap_grp_name).channel('enable').get()
            scn.item(t.matcap_grp_name).channel('enable').set(not enable)
        except:
            pass


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(CmdMyCustomCommand, t.TILA_MATCAP_TOGGLE_CMD)