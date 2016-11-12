import lx
import os
from os.path import isfile
import Tila_MatcapManagerModule as t


def loadImage(filepath, width, height):

    if width == 0 or height ==0:
        raise AttributeError("Width or Height must be higher than 0")

    img_svc = lx.service.Image()
    matcap_filename = os.path.basename(filepath)

    thumb_filename = os.path.join(t.matcap_thumb_path, 'th_' + matcap_filename)
    thumb_path = os.path.split(thumb_filename)[0]
    thumb_ext = os.path.splitext(thumb_filename)[1][1:]
    thumb_ext = thumb_ext.upper()

    if not os.path.exists(thumb_path):
        os.makedirs(thumb_path)

    image = img_svc.Load(filepath)

    w, h = image.Size()
    ch = image.Components()

    pixel = lx.object.storage()
    pixel.setType('f')
    pixel.setSize(width * height * ch)

    export_image = img_svc.Create(width, height, lx.symbol.iIMP_RGBAFP, 0)
    img_output = lx.object.ImageWrite(export_image)

    # Iterate over pixels and convert them into sRGB
    for ih in range(height):
        for iw in range(width):

            rw = (iw*w)/width
            rh = (ih*h)/height

            image.GetPixel(rw, rh, lx.symbol.iIMP_RGBAFP, pixel)
            iR = pixel[0]
            iG = pixel[1]
            iB = pixel[2]
            # set the RGBA pixels
            img_output.SetPixel(iw, ih, lx.symbol.iIMP_RGBAFP, pixel)
            pixel.set((iR, iG, iB, pixel[3]))

    # Save the image to disk
    img_svc.Save(img_output, thumb_filename, thumb_ext, 0)

    return img_svc.Load(thumb_filename)


def cleanFolder(path):
    if os.path.exists(path):
        files = [f for f in os.listdir(path) if isfile(os.path.join(path, f))]

        for f in files:
            os.remove(os.path.join(path, f))

