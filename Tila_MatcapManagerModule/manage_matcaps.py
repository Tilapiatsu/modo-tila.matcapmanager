import lx
import modo
import os
import Tila_MatcapManagerModule as t


IndexStyle = ['brak-sp', 'brak', 'sp', 'uscore', 'none']

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
        replaceImage(image, image_to_import)
        if assign_image:
            assignImage(shader, os.path.basename(image_to_import)[:-4])


def manageSelectionMatcap(shader, image, image_to_import):
    assign_image = False

    if shader is None:
        group = CreateShaderGroup()
        placeShaderOnTop(group, False)
        name = os.path.basename(image_to_import)[:-4]
        shader = assignMaterial(name)

        print getLatestMaterialCreated().name
        #lx.eval('item.parent %s %s inPlace:1' % (shader.id, group.id))

        assign_image = True
    '''
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
        replaceImage(image, image_to_import)
        if assign_image:
            assignImage(shader, os.path.basename(image_to_import)[:-4])
    '''


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

def assignMaterial(name):
    return lx.eval('poly.setMaterial %s {0.0 0.0 0.0} 0.0 0.0 false false false' % name)


def getLatestMaterialCreated():
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
    iterator = ''

    if lx.eval('pref.value application.indexStyle ?') == IndexStyle[0]:
        iterator = ' (' + i + ')'

    elif lx.eval('pref.value application.indexStyle ?') == IndexStyle[1]:
        iterator = '(' + i + ')'

    elif lx.eval('pref.value application.indexStyle ?') == IndexStyle[2]:
        iterator = ' ' + i

    elif lx.eval('pref.value application.indexStyle ?') == IndexStyle[3]:
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


def replaceImage(image, image_to_import):
    lx.eval(
        'clip.replace clip:{%s} filename:{%s} type:videoStill' % (image, os.path.join(t.matcap_path, image_to_import)))
    t.printLog('Replace Image by : ' + image_to_import)


def assignImage(shader, image):
    scn = modo.Scene()
    selection = scn.selected
    scn.select(shader)
    lx.eval('matcap.image {%s:videoStill001}' % image)
    t.printLog('Assigning ' + image + ' to Matcap Shader')
    scn.select(selection)


def importImage(image_to_import):
    image = os.path.join(t.matcap_path, image_to_import)

    lx.eval('clip.addStill "%s"' % image)
    t.printLog('Import Image : ' + os.path.basename(image))


def clearScene(clear, shader, image, affectSelection):
    scn = modo.Scene()
    if not clear:
        return False

    else:
        if not affectSelection:
            if shader is not None:
                scn.removeItems(shader)
                t.printLog('Matcap shader Deleted')
            else:
                t.printLog('No matching matcap shader in the scene')
            if image is not None:
                scn.removeItems(image)
                t.printLog('Matcap image Deleted')
            else:
                t.printLog('No matching matcap image in the scene')

            return True
        else:
            if shader is not None:
                scn.removeItems(shader)
                t.printLog('Matcap Group Deleted')
            else:
                t.printLog('No matching matcap group in the scene')
            if image is not None:
                for i in image:
                    scn.removeItems(i)
                t.printLog('Matcap images Deleted')
            else:
                t.printLog('No matching matcaps image in the scene')

            return True
