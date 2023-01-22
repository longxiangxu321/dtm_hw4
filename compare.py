import numpy as np
import rasterio
import matplotlib.pyplot as plt
from rasterio.windows import Window


def crop(pdok_file):
    with rasterio.open(pdok_file) as gz:
        xsize, ysize = 1000, 1000
        xoff, yoff = 3904, 11360

        window = Window(xoff, yoff, xsize, ysize)
        transform = gz.window_transform(window)
        # transform = Affine.translation(191952.0, 325070.0) * Affine.scale(0.5, 0.5)

        profile = gz.profile
        profile.update({
            'height': xsize,
            'width': ysize,
            'transform': transform
        })

        with rasterio.open('roi_dtm.tif', 'w', **profile) as dst:
            dst.write(gz.read(window=window))


def compare_dtm(dtm1, dtm2):
    dtm1_tif = rasterio.open(dtm1)
    dtm2_tif = rasterio.open(dtm2)
    dtm1_h = dtm1_tif.read(1)
    if dtm2 == 'roi_dtm.tif':
        # origin at the upper left, it should be flipped to do matrix subtraction
        dtm2_h = np.flipud(dtm2_tif.read(1))
    else:
        dtm2_h = dtm2_tif.read(1)

    difference_h = np.where(dtm2_h == dtm2_tif.nodatavals, np.nan, abs(dtm1_h - dtm2_h))
    breakpoint()
    difference_h_rmse = np.where(dtm2_h == dtm2_tif.nodatavals, 0, (dtm1_h - dtm2_h) ** 2)
    # breakpoint()
    # if compared to roi_dtm.tif, calculate RMSE
    if dtm2 == 'roi_dtm.tif':
        RMSE = round(np.sum(difference_h_rmse) / dtm2_h.size, 4)
        print('The RMSE value of {0} and {1} is: {2}.'.format(dtm1, dtm2, RMSE))
    else:
        pass

    # plotting the difference in raster
    file_name = 'Difference in height \n {} & {} comparison'.format(dtm1, dtm2)
    plt.imshow(difference_h, origin='lower', cmap='viridis')
    plt.colorbar().ax.set_title('m', size=8)
    plt.title(file_name)
    plt.xlabel('col')
    plt.ylabel('row')
    plt.show()


def main():
    compare_dtm('./data/dtm/cloth_dtm.tif', './data/dtm/ground_dtm.tif')
    compare_dtm('./data/dtm/cloth_dtm.tif', './data/dtm/roi_dtm.tif')
    compare_dtm('./data/dtm/ground_dtm.tif', './data/dtm/roi_dtm.tif')


if __name__ == '__main__':
    main()
