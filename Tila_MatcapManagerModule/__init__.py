import lx
import os
from os.path import isfile
import dialog

matcap_name = 'tila_matcap'
matcap_grp_name = 'tila_matcap_GRP'

matcap_imageChannelName = 'Image'

curr_path = os.path.dirname(os.path.realpath(__file__))
matcap_path = os.path.join(dialog.parentPath(curr_path), "Tila_Matcaps")
matcap_thumb_path = os.path.join(dialog.parentPath(curr_path), "Tila_MatcapsIcon")
matcap_icon_path = os.path.join(dialog.parentPath(curr_path), "Tila_Icon")
renderer_path = os.path.join(dialog.parentPath(curr_path), "Tila_MatcapRenderer")

renderer_path = os.path.join(renderer_path,"Tila_MatcapRenderer.lxo")

indexStyle = ['brak-sp', 'brak', 'sp', 'uscore', 'none']

TILA_MATCAP_UPDATE_FORM_NOFIFIER_CMD = 'tila.matcap.updateformnotifier'
TILA_MATCAP_UPDATE_FORM_CMD = 'tila.matcap.updateform'
TILA_MATCAP_LOAD_CMD = 'tila.matcap.load'
TILA_MATCAP_MANAGER_CMD = 'tila.matcap.manager'
TILA_MATCAP_OPEN_CMD = 'tila.matcap.open'
TILA_MATCAP_TOGGLE_CMD = 'tila.matcap.toggle'


def printLog(message):
    lx.out("TILA_MATCAP_MANAGER : " + message)


def printMatcapList(list):
    for i in range(len(list)):
        printLog('Matcap ' + str(i) + ' : ' + list[i])


def scanMatcapFolder():
    global matcap_path
    matcaps = [f for f in os.listdir(matcap_path) if isfile(os.path.join(matcap_path, f))]

    return matcaps

'''
def generateFormTemplate(silent=True):
    reload(ft)
    global curr_path
    global matcap_path
    cfg_path = dialog.parentPath(curr_path)
    matcaps = scanMatcapFolder()
    ft.generateForm(cfg_path, '91694808927', matcaps, matcap_path)


    printLog('Form Updated! Please, restart Modo to refresh it')

    if not silent:
        dialog.init_message('info', 'Done', 'Form Updated! Please, restart Modo to refresh it.')
'''
