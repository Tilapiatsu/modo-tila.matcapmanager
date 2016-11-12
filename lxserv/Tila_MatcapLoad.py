import lx
import lxu.command
import modo
import os
from os.path import isfile
import Tila_MatcapManagerModule as t
from Tila_MatcapManagerModule import dialog
from Tila_MatcapManagerModule import manage_matcaps as mm
from Tila_MatcapManagerModule import user_value


class CmdTilaMatcapLoad(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('matcapIndex', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('clearMatcap', lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('affectSelection_sw', lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

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

    def assignMatcapToScene(self, matcap_to_import, matcap_shader):
        matcap_image = None

        if matcap_shader is not None:
            try:
                matcap_image = matcap_shader.channel(t.matcap_imageChannelName).get()
            except:
                matcap_image = None

        mm.manageSceneMatcap(matcap_shader, matcap_image, matcap_to_import)

    def assignMatcapToSelection(self, matcap_to_import, matcap_shaderGroup, matcap_image):
        mm.manageSelectionMatcap(matcap_shaderGroup, matcap_image, matcap_to_import)

    def basic_Execute(self, msg, flags):
        reload(t)
        reload(mm)

        scn = modo.Scene()

        args = user_value.query_User_Values(self, 'tilaMatcapMan.')

        affectSelection_sw = args[2]

        try:
            matcap_to_import = self.matcaps[self.dyna_Int(0)]
        except:
            dialog.init_message('error', 'Matcap is not found',
                                "Matcap isn't in the folder anymore. Please restart Modo to refresh the UI.")
            lx.eval('tila.matcap.folderscan True')
            return None

        matcap_shader = None
        matcap_masterGroup = None
        matcap_image = []


        try:
            matcap_masterGroup = modo.Item(t.matcap_grp_name)
        except:
            matcap_masterGroup = None

        try:
            matcap_shader = modo.Item(t.matcap_name)
        except:
            matcap_shader = None

        matcap_image = []

        try:
            for i in self.scn.items(modo.c.VIDEOSTILL_TYPE):
                for j in self.matcaps:
                    name = os.path.basename(os.path.splitext(j)[0])
                    if i.name == name:
                        matcap_image.append(i.name)
        except:
            matcap_image = []

        if self.dyna_Bool(1):
            if mm.clearScene(matcap_masterGroup, matcap_shader, matcap_image):
                return None

        if not affectSelection_sw:
            self.assignMatcapToScene(matcap_to_import, matcap_shader)

        else:
            self.assignMatcapToSelection(matcap_to_import, matcap_masterGroup, matcap_image)

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(CmdTilaMatcapLoad, t.TILA_MATCAP_LOAD_CMD)

