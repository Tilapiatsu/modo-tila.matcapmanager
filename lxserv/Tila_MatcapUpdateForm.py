#!/usr/bin/env python

import lx
import lxifc
import lxu.command
import Tila_MatcapManagerModule as t

from Tila_MatcapManagerModule import manage_matcaps

class PopUp(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._items[0])

    def uiv_PopIconImage(self, index):
        return self._items[2][index]

    def uiv_PopUserName(self, index):
        return self._items[0][index]

    def uiv_PopIconSize(self):
        return (True, 32, 32)

    def PopToolTip(self, index):
        return self._items[3][index]

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
        return t.TILA_MATCAP_UPDATE_FORM_NOFIFIER_CMD

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


lx.bless(UpdateFormNotifier, t.TILA_MATCAP_UPDATE_FORM_NOFIFIER_CMD)

class CmdTilaMatcapFormManager(lxu.command.BasicCommand):
    cmdlist = manage_matcaps.generateMatcapCommandName()
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        # Add an integer attribute. The attribute is required
        self.dyna_Add('matcap', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

        # Setup notifier
        self.not_svc = lx.service.NotifySys()
        self.notifier = lx.object.Notifier()

        reload(manage_matcaps)

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
            popup = PopUp(self.cmdlist)
            return popup

    def cmd_Execute(self, flags):
        if not self.dyna_IsSet(0):
            return

        cls = self.__class__

        matcap = self.dyna_Int(0, None)

        if matcap == 0:
            reload(manage_matcaps)
            cls.cmdlist = manage_matcaps.generateMatcapCommandName()
            UpdateFormNotifier.reset()
            UpdateFormNotifier().Notify(lx.symbol.fCMDNOTIFY_DATATYPE)
        else:
            lx.eval('%s' % (self.cmdlist[1][matcap]))

    def cmd_Query(self, index, vaQuery):
        # dummy query method
        pass

    def cmd_NotifyAddClient(self, argument, object):
        self.notifier = self.not_svc.Spawn(t.TILA_MATCAP_UPDATE_FORM_NOFIFIER_CMD, "")
        self.notifier.AddClient(object)

    def cmd_NotifyRemoveClient(self, object):
        self.notifier.RemoveClient(object)

lx.bless(CmdTilaMatcapFormManager, t.TILA_MATCAP_MANAGER_CMD)