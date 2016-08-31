import lx
import lxifc
import lxu.command
import modo
import os
import sys
from os.path import isfile, join


class CmdMyCustomCommand(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('matcapIndex', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('clearMatcap', lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

        self.matcap_name = 'tila_matcap'
        self.matcap_image_name = 'tila_matcap_image'

        self.scn = modo.Scene()

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
        assign_image = False

        if shader is None:
            shader = self.createShader()
            assign_image = True

        if image is None:
            self.importImage(image_to_import)
            self.assignImage(shader, os.path.basename(image_to_import)[:-4])
        elif image == os.path.splitext(image_to_import)[0]:
            if assign_image:
                self.assignImage(shader, os.path.basename(image_to_import)[:-4])
            else:
                self.print_log('This matcap image is already assign')
            return None
        elif image != os.path.splitext(image_to_import)[0]:
            self.replaceImage(image, image_to_import)
            if assign_image:
                self.assignImage(shader, os.path.basename(image_to_import)[:-4])

    def updateImageNameHolder(self, shader, image):
        if shader.channel('image_name_holder').get is not image:
            shader.channel('image_name_holder').set(image)

    def createShader(self):
        shader = self.scn.addItem('matcapShader')
        shader.name = self.matcap_name
        self.placeShaderOnTop(shader)

        return shader

    def placeShaderOnTop(self, item):
        selection = self.scn.selected
        self.scn.select(item)
        lx.eval('texture.parent polyRender006 -1')
        lx.eval('item.channel matcapShader$glOnly true')
        self.scn.select(selection)

    def replaceImage(self, image, image_to_import):
        lx.eval('clip.replace clip:{%s} filename:{%s} type:videoStill' % (image, os.path.join(self.matcap_path, image_to_import)))
        self.print_log('Replace Image by : ' + image_to_import)

    def assignImage(self, shader, image):
        selection = self.scn.selected
        self.scn.select(shader)
        lx.eval('matcap.image {%s:videoStill001}' % image)
        self.print_log('Assigning ' + image + ' to Matcap Shader')
        self.scn.select(selection)

    def importImage(self, image_to_import):
        image = os.path.join(self.matcap_path, image_to_import)

        lx.eval('clip.addStill "%s"' % image)
        self.print_log('Import Image : ' + os.path.basename(image))

    def getMatcapImageName(self, shader):
        selection = self.scn.selected
        self.scn.select(shader)
        image_name = lx.eval('matcap.image ?')[:-14]   #Sooooo tricky
        self.scn.select(selection)
        return image_name

    def clearScene(self, shader, image):
        if not self.dyna_Bool(1):
            return False

        else:
            if shader is not None:
                self.scn.removeItems(shader)
                self.print_log('Matcap shader Deleted')
            else:
                self.print_log('No matching matcap shader in the scene')
            if image is not None:
                self.scn.removeItems(image)
                self.print_log('Matcap image Deleted')
            else:
                self.print_log('No matching matcap image in the scene')

            return True

    def basic_Execute(self, msg, flags):

        matcap_to_import = self.matcaps[self.dyna_Int(0)]

        try:
            matcap_shader = modo.Item(self.matcap_name)
        except:
            matcap_shader = None

        matcap_image = None
        try:
            for i in self.scn.items(modo.c.VIDEOSTILL_TYPE):
                for j in self.matcaps:
                    name = os.path.basename(os.path.splitext(j)[0])
                    if i.name == name:
                        matcap_image = os.path.splitext(i.name)[0]
                        break
        except:
            matcap_image = None

        if self.clearScene(matcap_shader, matcap_image):
            return None

        self.manageMatcap(matcap_shader, matcap_image, matcap_to_import)

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

lx.bless(CmdMyCustomCommand, "tila.matcapmanager")
