import lx
import lxifc
import lxu.command
import modo
import os
from os.path import isfile, join


class CmdMyCustomCommand(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('matcapIndex', lx.symbol.sTYPE_INTEGER)

        self.scn = modo.Scene()
        currScn = modo.scene.current()

        self.curr_path = os.path.dirname(os.path.realpath(__file__))
        self.matcap_path = os.path.join(self.parentPath(self.curr_path), "Matcaps")

        self.matcaps = [f for f in os.listdir(self.matcap_path) if isfile(os.path.join(self.matcap_path, f))]

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def matcapIndex(self):
        return self.dyna_Int(0)

    @staticmethod
    def parentPath(path):
        return os.path.abspath(os.path.join(path, os.pardir))

    @staticmethod
    def print_log(message):
        lx.out("TILA_MATCAP_MANAGER : " + message)

    def manageMatcap(self, shader, image, image_to_import):
        if image == None:
            image = self.importImage(image_to_import)
        elif image.name != os.path.splitext(image_to_import)[0]:
            self.replaceImage(image, image_to_import)

        if shader == None:
            shader = self.scn.addItem('matcapShader')
            shader.name = 'tila_matcap'
            self.placeShaderOnTop(shader)

        self.assignImage(shader, image)

    def placeShaderOnTop(self, item):
        selection = self.scn.selected
        self.scn.select(item)
        lx.eval('texture.parent polyRender006 -1')
        lx.eval('item.channel matcapShader$glOnly true')
        self.scn.select(selection)

    def replaceImage(self, image, image_to_import):
        selection = self.scn.selected
        self.scn.select(image)
        lx.eval('clip.replace clip:%s type:videoStill' % image_to_import)
        self.scn.select(selection)

    def assignImage(self, shader, image):
        selection = self.scn.selected
        self.scn.select(shader)
        lx.eval('matcap.image {%s:videoStill001}' % image.name)
        self.scn.select(selection)

    def importImage(self, image_to_import):
        image = os.path.join(self.matcap_path, image_to_import)

        lx.eval('clip.addStill "%s"' % image)
        self.print_log('Import Image : ' + os.path.basename(image))

        matcap_image = [i for i in self.scn.items('videoStill') if i.name ==
                             os.path.basename(os.path.splitext(image_to_import)[0])]
        return matcap_image[0]

    def basic_Execute(self, msg, flags):

        matcap_to_import = self.matcaps[self.dyna_Int(0)]

        try:
            matcap_shader = modo.Item('tila_matcap')
        except:
            matcap_shader = None

        try:
            matcap_image = [i for i in self.scn.items('videoStill') if i.name ==
                            os.path.basename(os.path.splitext(matcap_to_import)[0])]
            matcap_image = matcap_image[0]
        except:
            matcap_image = None

        self.manageMatcap(matcap_shader, matcap_image, matcap_to_import)

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(CmdMyCustomCommand, "tila.matcapmanager")

