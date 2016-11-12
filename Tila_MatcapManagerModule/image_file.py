import lx
import os
import Tila_MatcapManagerModule as t


def loadImage(filepath, width, height):

    if width == 0 or height ==0:
        raise AttributeError("Width or Height must be higher than 0")

    img_svc = lx.service.Image()
    img_prc = lx.service.ImageProcessing()
    matcap_filename = os.path.basename(filepath)

    file_resized_filename = os.path.join(t.matcap_thumb_path, 'th_' + matcap_filename)
    file_resized_path = os.path.split(file_resized_filename)[0]
    file_resized_ext = os.path.splitext(file_resized_filename)[1][1:]
    file_resized_ext = file_resized_ext.upper()

    if not os.path.exists(file_resized_path):
        os.makedirs(file_resized_path)

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
    img_svc.Save(img_output, file_resized_filename, file_resized_ext, 0)


    return img_svc.Load(file_resized_filename)



