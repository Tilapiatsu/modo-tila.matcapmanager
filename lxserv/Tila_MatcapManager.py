import lx
import lxu.command
import modo
import os
from os.path import isfile
import Tila_MatcapManagerModule as t

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

        self.matcap_name = 'tila_matcap'

        self.scn = modo.Scene()

        self.curr_path = os.path.dirname(os.path.realpath(__file__))

        self.matcaps = [f for f in os.listdir(t.matcap_path) if isfile(os.path.join(t.matcap_path, f))]


    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO


    def basic_Enable(self, msg):
        return True


    def cmd_Interact(self):
        pass


    def matcapIndex(self):
        return self.dyna_Int(0)


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
                t.printLog('This matcap image is already assign')
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
        lx.eval('clip.replace clip:{%s} filename:{%s} type:videoStill' % (image, os.path.join(t.matcap_path, image_to_import)))
        t.printLog('Replace Image by : ' + image_to_import)


    def assignImage(self, shader, image):
        selection = self.scn.selected
        self.scn.select(shader)
        lx.eval('matcap.image {%s:videoStill001}' % image)
        t.printLog('Assigning ' + image + ' to Matcap Shader')
        self.scn.select(selection)


    def importImage(self, image_to_import):
        image = os.path.join(t.matcap_path, image_to_import)

        lx.eval('clip.addStill "%s"' % image)
        t.printLog('Import Image : ' + os.path.basename(image))


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
                t.printLog('Matcap shader Deleted')
            else:
                t.printLog('No matching matcap shader in the scene')
            if image is not None:
                self.scn.removeItems(image)
                t.printLog('Matcap image Deleted')
            else:
                t.printLog('No matching matcap image in the scene')

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


lx.bless(CmdMyCustomCommand, "tila.matcap.manager")

