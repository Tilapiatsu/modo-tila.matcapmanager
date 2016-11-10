import lx
import lxifc

def LogOut(str):
    ls = lx.service.Log()
    log = ls.SubSystemLookup('scripts')
    log.AddEntry(ls.CreateEntryMessage(0, str))

def WasteTime(n,monitor):
    mon = lx.object.Monitor(monitor)
    mon.Initialize(n)
    for i in range(n):
        mon.Increment(1)

class SizeSaver(lxifc.Saver):
    def sav_Save(self,image,filename,monitor):
        img = lx.object.Image(image)
        w,h = img.Size()
        LogOut('saving ... ' + str (w * h))
        WasteTime(w * h, monitor)

tags = {
    lx.symbol.sSRV_USERNAME: "Size Saver",
    lx.symbol.sSAV_OUTCLASS:  lx.symbol.a_IMAGE,
    lx.symbol.sSAV_DOSTYPE : "PSS"
}
lx.bless(SizeSaver, "pySizeSaver", tags)