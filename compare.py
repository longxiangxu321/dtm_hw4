import numpy as np
import rasterio
import matplotlib.pyplot as plt
from rasterio.windows import Window
import os


def crop(pdok_file):
    with rasterio.open(pdok_file) as gz:
        xsize, ysize = 1000, 1000
        xoff, yoff = 3904, 11360

        window = Window(xoff, yoff, xsize, ysize)
        transform = gz.window_transform(window)

        profile = gz.profile
        profile.update({
            'height': xsize,
            'width': ysize,
            'transform': transform
        })

        with rasterio.open('./data/dtm/roi_dtm.tif', 'w', **profile) as dst:
            dst.write(gz.read(window=window))


def compare_dtm(dtm1, dtm2, dtm1flip=False, dtm2flip=False):
    dtm1_tif = rasterio.open(dtm1)
    dtm2_tif = rasterio.open(dtm2)
    if dtm1flip:
        # origin at the upper left, it should be flipped to do matrix subtraction
        dtm1_h = np.flip(dtm1_tif.read(1), axis=0)
    else:
        dtm1_h = dtm1_tif.read(1)
    if dtm2flip:
        dtm2_h = np.flip(dtm2_tif.read(1), axis=0)
    else:
        dtm2_h = dtm2_tif.read(1)
    difference_h = np.where(dtm2_h == dtm2_tif.nodatavals, np.nan, abs(dtm1_h - dtm2_h))
    difference_h_rmse = np.where(dtm2_h == dtm2_tif.nodatavals, 0, (dtm1_h - dtm2_h) ** 2)
    name1 = os.path.basename(dtm1)
    name2 = os.path.basename(dtm2)
    name1 = os.path.splitext(name1)[0]
    name2 = os.path.splitext(name2)[0]
    # if compared to roi_dtm.tif, calculate RMSE

    RMSE = round(np.sum(difference_h_rmse) / dtm2_h.size, 4)
    print('The RMSE value of {0} and {1} is: {2}.'.format(name1, name2, RMSE))


    # plotting the difference in raster
    file_name = 'Difference in height \n {} & {} comparison'.format(name1, name2)
    plt.imshow(difference_h, origin='lower', cmap='Spectral_r', vmin=0, vmax=6)
    plt.colorbar().ax.set_title('m', size=8)
    plt.title(file_name)
    plt.xlabel('col')
    plt.ylabel('row')
    plt.show()


def main():
    # crop(pdok_file)
    compare_dtm('./data/dtm/ground_dtm.tif', './data/dtm/cloth_dtm.tif', dtm1flip=True,  dtm2flip=True)
    compare_dtm('./data/dtm/cloth_dtm.tif', './data/dtm/roi_dtm.tif', dtm1flip=True)
    compare_dtm('./data/dtm/ground_dtm.tif', './data/dtm/roi_dtm.tif', dtm1flip=True)


if __name__ == '__main__':
    main()
