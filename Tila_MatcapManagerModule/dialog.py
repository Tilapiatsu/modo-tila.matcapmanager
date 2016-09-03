import lx
import os
import sys
import subprocess

if sys.platform == 'darwin':
    def open_folder(path):
        subprocess.check_call(['open', '--', path])

elif sys.platform == 'linux2':
    def open_folder(path):
        subprocess.check_call(['xdg-open', '--', path])

elif sys.platform == 'win32':
    def open_folder(path):
        os.startfile(path)

def parentPath(path):
    return os.path.abspath(os.path.join(path, os.pardir))


# http://modo.sdk.thefoundry.co.uk/wiki/Dialog_Commands

def init_custom_dialog(type, title, format, uname, ext, save_ext=None, path=None, init_dialog=False):
    ''' Custom file dialog wrapper function

        type  :   Type of dialog, string value, options are 'fileOpen' or 'fileSave'
        title :   Dialog title, string value.
        format:   file format, tuple of string values
        uname :   internal name
        ext   :   tuple of file extension filter strings
        save_ext: output file extension for fileSave dialog
        path  :   optional default loacation to open dialog

    '''
    lx.eval("dialog.setup %s" % type)
    lx.eval("dialog.title {%s}" % (title))
    lx.eval("dialog.fileTypeCustom {%s} {%s} {%s} {%s}" % (format, uname, ext, save_ext))
    if type == 'fileSave' and save_ext != None:
        lx.eval("dialog.fileSaveFormat %s extension" % save_ext)
    if path is not None:
        lx.eval('dialog.result {%s}' % path)

    if init_dialog:
        try:
            lx.eval("dialog.open")
            return lx.eval("dialog.result ?")
        except:
            return None


def init_message(type, title, message):
    lx.eval('dialog.setup {%s}' % type)
    lx.eval('dialog.title {%s}' % title)
    lx.eval('dialog.msg {%s}' % message)
    lx.eval('dialog.open')