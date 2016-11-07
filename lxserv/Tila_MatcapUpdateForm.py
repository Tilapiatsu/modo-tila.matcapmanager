#!/usr/bin/env python

import lx
import lxifc
import lxu.command
import Tila_MatcapManagerModule as t

from Tila_MatcapManagerModule import form_template

# This is our list of commands. You can generate this list any way you like
# including procedurally - in fact the most common use case for a Form Command
# List would be to generate a list of commands to show in a form procedurally.
cmdlist = form_template.generateMatcapCommandName()

# The UIValueHints object that returns the items in the list of commands
# to the form.

class PopUp(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._items[0])

    def uiv_PopUserName(self,index):
        return self._items[1][index]

    def uiv_PopInternalName(self,index):
        return self._items[0][index]

    def uiv_PopIconImage(self, index):
        print self._items[2][index]
        return self._items[2][index]

    def uiv_PopUserName(self, index):
        return self._items[0][index]

    def uiv_PopIconSize(self):
        return [32, 32]


class UpdateFormNotifier(lxifc.Notifier):
    masterList = {}
    _presetValuesChanged = False

    @classmethod
    def reset(cls):
        '''
        This method is called every time the user selects/creates/deletes a preset.
        It causes the next preset change to redraw the UI and update the Asterisk once.
        This is to reduce the flicker cause by the absense of double buffering in the form.
        '''
        cls._presetValuesChanged = False

    def noti_Name(self):
        return t.TILA_MATCAP_UPDATE_FORM_CMD

    def noti_AddClient(self, event):
        self.masterList[event.__peekobj__()] = event

    def noti_RemoveClient(self, event):
        del self.masterList[event.__peekobj__()]

    def Notify(self, flags):
        for event in self.masterList:
            evt = lx.object.CommandEvent(self.masterList[event])
            evt.Event(flags)

    def NotifyPresetChanged(self):
        '''To avoid re-building the entire form too often which causes flickering, we only do it once'''

        cls = self.__class__
        if not cls._presetValuesChanged:
            self.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

        cls._presetValuesChanged = True


lx.bless(UpdateFormNotifier, t.TILA_MATCAP_UPDATE_FORM_CMD)


class MatcapCommandList(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        # This is a series of flags, although in this case we're only returning
        # ''fVALHINT_FORM_COMMAND_LIST'' to indicate that there's a Form Command
        # List implemented.
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self, index):
        return self._items[index]

    def uiv_FormCommandUserName(self, index):
        return self._items[index]



# This is the command that will be replaced by the commands in MyCommandsList
# in any form in which it's embedded as a query. It requires a queriable
# attribute/argument but neither of the command's ''cmd_Execute'' or ''cmd_Query'' methods
# need to be implemented as neither will be called when the argument is queried
# in a form.  You can still implement them, but they will only be used when
# executing/querying from scripts or CHist etc.
class CmdTilaMatcapFormCommandList(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        # Add an integer attribute. The attribute is required
        self.dyna_Add('matcap', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

        # Setup notifier
        self.not_svc = lx.service.NotifySys()
        self.notifier = lx.object.Notifier()

    def cmd_Flags(self):
        return lx.symbol.fCMD_UI

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def arg_UIValueHints(self, index):
        # create an instance of our commands list object passing it the
        # list of commands.
        if index == 0:
            print cmdlist[2]
            return PopUp(cmdlist)

    def cmd_Execute(self, flags):
        if not self.dyna_IsSet(0):
            return

        matcap = self.dyna_Int(0, None)

        lx.eval('%s %s' % (t.TILA_MATCAP_MANAGER_CMD, matcap))

    def cmd_Query(self, index, vaQuery):
        # dummy query method
        pass

    def cmd_NotifyAddClient(self, argument, object):
        self.notifier = self.not_svc.Spawn(t.TILA_MATCAP_UPDATE_FORM_CMD, "")
        self.notifier.AddClient(object)

    def cmd_NotifyRemoveClient(self, object):
        self.notifier.RemoveClient(object)

lx.bless(CmdTilaMatcapFormCommandList, t.TILA_MATCAP_FORM_CMD)