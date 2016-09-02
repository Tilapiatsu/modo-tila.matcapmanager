import lx
import modo
import os
from os.path import isfile


def parentPath(path):
    return os.path.abspath(os.path.join(path, os.pardir))


def printLog(message):
    lx.out("TILA_MATCAP_MANAGER : " + message)


def printMatcapList(list):
    for i in range(len(list)):
        printLog('Matcap ' + str(i) + ' : ' + list[i])


def scanMatcapFolder():
    curr_path = os.path.dirname(os.path.realpath(__file__))
    matcap_path = os.path.join(parentPath(curr_path), "Matcaps")
    matcaps = [f for f in os.listdir(matcap_path) if isfile(os.path.join(matcap_path, f))]

    printMatcapList(matcaps)

    return matcaps


def generateForm():
    matcaps = scanMatcapFolder()
    scn = modo.Scene()
    selection = scn.selected

    clearForm()

    lx.eval('select.attr {91694808927:sheet} set')

    for i in range(len(matcaps)):
        lx.eval('attr.addCommand "tila.matcapmanager %s"' % i)
        lx.eval('attr.label %s' % os.path.splitext(matcaps[i])[0])
        lx.eval('attr.iconImage {attricon:Tila_MatcapManager/Matcaps/%s}' % matcaps[i])

    printLog('Form Updated')

    scn.select(selection)

def clearForm():
    matcap_count = 0

    if matcap_count > 0:
        for i in range(matcap_count):
            if i == 0:
                mode = 'set'
            else:
                mode = 'add'

            lx.eval('select.attr {91694808927:sheet/%s} %s' % (i, mode))

        lx.eval('!!attr.delete')
