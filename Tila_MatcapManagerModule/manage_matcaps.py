import lx
import modo
import os
import Tila_MatcapManagerModule as t
from Tila_MatcapManagerModule import image_file
from Tila_MatcapManagerModule import dialog

############## TODO ###################
'''
 - Get default material name from preference

'''

def manageSceneMatcap(shader, image, image_to_import):
    assign_image = False

    if shader is None:
        shader = createShader(t.matcap_name)
        placeShaderOnTop(shader, True)
        assign_image = True

    if image is None:
        importImage(image_to_import)
        assignImage(shader, os.path.basename(image_to_import)[:-4])
    elif image == os.path.splitext(image_to_import)[0]:
        if assign_image:
            assignImage(shader, os.path.basename(image_to_import)[:-4])
        else:
            t.printLog('This matcap image is already assign')
        return None
    elif image != os.path.splitext(image_to_import)[0]:
        if imageExistInMasterGroup(image):
            importImage(image_to_import)
            assign_image = True
        else:
            replaceImage(image, image_to_import, shader)

        if assign_image:
            assignImage(shader, os.path.basename(image_to_import)[:-4])


def manageSelectionMatcap(masterGroup, image, image_to_import):
    assign_image = False
    scn = modo.Scene()

    name = os.path.basename(image_to_import)[:-4]
    channelName = t.matcap_imageChannelName + '_' + str(len(image))

    if masterGroup is None:
        group = CreateShaderGroup()
        placeShaderOnTop(group, False)

        createUserChannel(channelName, group, 'string')
        group.channel(channelName).set(name)

        mat = createMaterialGroup(name, image_to_import, group)
    else:
        createUserChannel(channelName, masterGroup, 'string')
        masterGroup.channel(channelName).set(name)
        mat = createMaterialGroup(name, image_to_import, masterGroup)

    if image == []:
        importImage(image_to_import)
        assignImage(mat, os.path.basename(image_to_import)[:-4], False)
    else:
        for i in image:
            if i == os.path.splitext(image_to_import)[0]:
                break

        importImage(image_to_import)
        assignImage(mat, os.path.basename(image_to_import)[:-4], False)


def createShader(name):
    scn = modo.Scene()
    shader = scn.addItem('matcapShader')
    shader.name = name

    return shader


def CreateShaderGroup():
    scn = modo.Scene()
    group = scn.addItem('mask')
    group.name = t.matcap_grp_name

    return group


def createMaterialGroup(name, image_to_import, group):
    materialExist = itemExist(name + '_GRP')

    assignMaterial(name + '_GRP')

    mat = getLatestMaterialCreated(materialExist, name)

    matGrp = mat.parent
    mat.name = name + '_MAT'

    if not materialExist:
        parentShaderItem(matGrp, group)
        mat = convertMaterialToMatcap(mat)

    return mat


def itemExist(name):
    exist = True
    scn = modo.Scene()
    try:
        scn.item(name + ' (Material)')
        exist = True
    except LookupError:
        exist = False

    return exist


def imageExistInMasterGroup(image):
    scn = modo.Scene()
    try:
        masterGroup = scn.item(t.matcap_grp_name)

        for ch in masterGroup.channels(t.matcap_imageChannelName + '_*'):
            if ch.get() == image:
                return True

        return False

    except:
        return False

def parentShaderItem(item, group):
    lx.eval('item.parent %s %s inPlace:1' % (item.id, group.id))


def assignMaterial(name):
    return lx.eval('!!poly.setMaterial %s {0.0 0.0 0.0} 0.0 0.0 false false false' % name)


def convertMaterialToMatcap(mat):
    scn = modo.Scene()
    name = mat.name
    scn.select(mat)
    lx.eval('item.setType matcapShader textureLayer')
    mat = scn.item(name + getIteratorTemplate(2))
    mat.name = mat.name[:-2]
    return mat
    #scn.select(selection)


def getLatestMaterialCreated(exist, name):
    scn = modo.Scene()

    if exist:
        mat = scn.item(name + '_MAT')
    else:
        i = 1
        mat = None
        while True:
            try:
                if i == 1 :
                    mat = modo.Item('Material')
                else:
                    mat = modo.Item('Material%s' % getIteratorTemplate(i))

                i = i + 1
            except :
                break

    return mat


def getIteratorTemplate(i):
    i = str(i)
    iterator = ''

    if lx.eval('pref.value application.indexStyle ?') == t.indexStyle[0]:
        iterator = ' (' + i + ')'

    elif lx.eval('pref.value application.indexStyle ?') == t.indexStyle[1]:
        iterator = '(' + i + ')'

    elif lx.eval('pref.value application.indexStyle ?') == t.indexStyle[2]:
        iterator = ' ' + i

    elif lx.eval('pref.value application.indexStyle ?') == t.indexStyle[3]:
        iterator = '_' + i

    return iterator



def placeShaderOnTop(item, glOnly):
    scn = modo.Scene()
    selection = scn.selected
    scn.select(item)
    lx.eval('texture.parent polyRender006 -1')
    if glOnly:
        lx.eval('item.channel matcapShader$glOnly true')
    scn.select(selection)


def replaceImage(image, image_to_import, shader):
    lx.eval('clip.replace clip:{%s} filename:{%s} type:videoStill' % (image, os.path.join(t.matcap_path, image_to_import)))
    shader.channel('Image').set(image_to_import[:-4])
    t.printLog('Replace Image by : ' + image_to_import)


def assignImage(shader, image, createChannel=True):
    scn = modo.Scene()
    selection = scn.selected

    scn.select(shader)

    lx.eval('matcap.image {%s:videoStill001}' % image)

    if createChannel:
        createUserChannel(t.matcap_imageChannelName, shader, 'string')
        shader.channel(t.matcap_imageChannelName).set(image)

    t.printLog('Assigning ' + image + ' to Matcap Shader')
    scn.select(selection)


def importImage(image_to_import):
    image = os.path.join(t.matcap_path, image_to_import)

    lx.eval('clip.addStill "%s"' % image)
    t.printLog('Import Image : ' + os.path.basename(image))


def clearScene(shaderGroup, shader, image):
    scn = modo.Scene()

    result = False

    if shaderGroup is not None:
        scn.removeItems(shaderGroup, children=True)
        t.printLog('Matcap shader group Deleted')
        result = result or True
    else:
        t.printLog('No matching matcap shader group in the scene')

    if shader is not None:
        scn.removeItems(shader, children=True)
        t.printLog('Matcap Shader  Deleted')
        result = result or True
    else:
        t.printLog('No matching matcap shader in the scene')

    if image is not None:
        for i in image:
            scn.removeItems(i)
        t.printLog('Matcap images Deleted')
        result = result or True
    else:
        t.printLog('No matching matcaps image in the scene')

    return result


def atLeastOneMeshItemInSelection():
    scn = modo.Scene()

    meshItems = [i for i in scn.items(itype='mesh') or scn.items(itype='meshInst')]
    print meshItems
    print scn.selected

    result = False
    for mesh in meshItems:
        for s in scn.selected:
            if mesh == s:
                result = True
                break

    return result


def createUserChannel(name, item, chType='matrix'):
    try:
        if item.channel(name) is not None:
            pass
    except:
        lx.eval('channel.create name:%s type:%s item:%s' % (name, chType, item.id))


def generateMatcapCommandName():
    reload(image_file)
    command = []
    name = []
    matcap_image = []
    tooltip = []

    matcaps = t.scanMatcapFolder()

    image_file.cleanFolder(t.matcap_thumb_path)

    first_index = 0
    for i in xrange(len(matcaps)+5):

        if i == 0:
            first_index += 1
            command.append(t.TILA_MATCAP_UPDATE_FORM_CMD)
            name.append('Scan Matcap Folder')

            icon_path = os.path.join(t.matcap_icon_path, 'magnifyingglass.png')
            image = image_file.loadImage(icon_path, 32, 32)

            matcap_image.append(image)
            tooltip.append('Automatically scan the matcap folder and generate the form')

        elif i == 1:
            first_index += 1
            command.append('tila.matcap.open 0')
            name.append('Open Matcap Folder')

            icon_path = os.path.join(t.matcap_icon_path, 'folder.png')
            image = image_file.loadImage(icon_path, 32, 32)

            matcap_image.append(image)
            tooltip.append('Open Matcap Folder')

        elif i == 2:
            first_index += 1
            command.append('tila.matcap.open 1')
            name.append('Open Matcap Renderer Scene')

            icon_path = os.path.join(t.matcap_icon_path, 'modo_scene.png')
            image = image_file.loadImage(icon_path, 32, 32)

            matcap_image.append(image)
            tooltip.append('Open Matcap Renderer Scene')

        elif i == 3:
            first_index += 1
            command.append('tila.matcap.load 0 true')
            name.append('Clean Scene')

            icon_path = os.path.join(t.matcap_icon_path, 'broom.png')
            image = image_file.loadImage(icon_path, 32, 32)

            matcap_image.append(image)
            tooltip.append('Remove the matcap shader and the imported image')

        elif i == 4:
            first_index += 1
            command.append('tila.matcap.toggle')
            name.append('Toggle Matcap Visibility')

            icon_path = os.path.join(t.matcap_icon_path, 'enable.png')
            image = image_file.loadImage(icon_path, 32, 32)

            matcap_image.append(image)
            tooltip.append('Switch all matcap shader On or Off')

        else:
            j = i - first_index
            command.append('%s %s' % (t.TILA_MATCAP_LOAD_CMD, j))
            name.append(os.path.splitext(os.path.basename(matcaps[j]))[0])

            matcap_path = os.path.join(t.matcap_path, matcaps[j])

            image = image_file.loadImage(matcap_path, 32, 32)

            matcap_image.append(image)

            tooltip.append('Load matcap : %s' % name[j])

    dialog.print_log('Matcap folder scanned')

    return [name, command, matcap_image, tooltip]
