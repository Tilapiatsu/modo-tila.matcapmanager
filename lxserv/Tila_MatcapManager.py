import lx
import lxu.command
import modo
import os
from os.path import isfile
import Tila_MatcapManagerModule as t
from Tila_MatcapManagerModule import dialog
from Tila_MatcapManagerModule import manage_matcaps as mm

''' TODO
    - Add an On/Off Button/command to easily turn show or hide the matcap without having to delete it
'''
class CmdMyCustomCommand(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('matcapIndex', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('clearMatcap', lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

        self.scn = modo.Scene()

        self.matcaps = [f for f in os.listdir(t.matcap_path) if isfile(os.path.join(t.matcap_path, f))]

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def matcapIndex(self):
        return self.dyna_Int(0)

    def basic_Execute(self, msg, flags):
        reload(t)
        reload(mm)

        try:
            matcap_to_import = self.matcaps[self.dyna_Int(0)]
        except:
            dialog.init_message('error', 'Matcap is not found', "Matcap isn't in the folder anymore. Please restart Modo to refresh the UI.")
            lx.eval('tila.matcap.folderscan True')
            return None

        try:
            matcap_shader = modo.Item(t.matcap_name)
        except:
            matcap_shader = None

        matcap_image = None

        try:
            for i in self.scn.items(modo.c.VIDEOSTILL_TYPE):
                for j in self.matcaps:
                    name = os.path.basename(os.path.splitext(j)[0])
                    if i.name == name:
                        matcap_image = i.name
                        break
        except:
            matcap_image = None

        if mm.clearScene(self.dyna_Bool(1), matcap_shader, matcap_image):
            return None

        mm.manageMatcap(matcap_shader, matcap_image, matcap_to_import)


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(CmdMyCustomCommand, "tila.matcap.manager")

