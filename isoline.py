import rasterio
import numpy as np
import math


def isoline_extraction(raster, isoline_interval, filename):
    data = raster.read(1)
    z_min = np.min(data)
    z_max = np.max(data)
    resolution = (raster.bounds.top - raster.bounds.bottom) / raster.height
    with open('{}_isoline.wkt'.format(filename), 'w') as fh:
        fh.write("geometry;height\n")
        for i in range(int(z_min), int(z_max), isoline_interval):
            for j in range(raster.width - 1):  # data[p,j] represent ynum=p, xnum=j
                for p in range(raster.height - 1):
                    wkt = []
                    if data[j][p + 1] < i <= data[j, p] or data[j][p + 1] > i >= data[j, p]:
                        x1 = raster.xy(j, p)[0] + math.fabs(i - data[j, p]) / math.fabs(
                            data[j, p + 1] - data[j, p]) * resolution
                        y1 = raster.xy(j, p)[1]
                        wkt.append([x1, y1])
                    if data[j][p + 1] <= i < data[j + 1, p + 1] or data[j][p + 1] >= i > data[j + 1, p + 1]:
                        x4 = raster.xy(j, p + 1)[0]
                        y4 = raster.xy(j, p + 1)[1] - math.fabs(i - data[j, p + 1]) / math.fabs(
                            data[j + 1, p + 1] - data[j, p + 1]) * resolution
                        wkt.append([x4, y4])
                    if data[j + 1][p + 1] <= i < data[j + 1, p] or data[j + 1][p + 1] >= i > data[j + 1, p]:
                        x3 = raster.xy(j + 1, p + 1)[0] - math.fabs(i - data[j + 1, p + 1]) / math.fabs(
                            data[j + 1, p + 1] - data[j + 1, p]) * resolution
                        y3 = raster.xy(j + 1, p + 1)[1]
                        wkt.append([x3, y3])
                    if data[j][p] < i <= data[j + 1, p] or data[j][p] > i >= data[j + 1, p]:
                        x2 = raster.xy(j + 1, p)[0]
                        y2 = raster.xy(j + 1, p)[1] + math.fabs(i - data[j + 1, p]) / math.fabs(
                            data[j + 1, p] - data[j, p]) * resolution
                        wkt.append([x2, y2])
                    if len(wkt) > 0:
                        coordinates = ["{0} {1}".format(pt[0], pt[1]) for pt in wkt]
                        coordinates = ", ".join(coordinates)
                        wkt = "LINESTRING ({0})".format(coordinates)
                        fh.write("{};{}\n".format(wkt, i))


def main():
    raster = rasterio.open("./data/dtm/cloth_dtm.tif")
    isoline_extraction(raster, isoline_interval=2, filename="./data/isoline/cloth")
    point_dtm = rasterio.open("./data/dtm/ground_dtm.tif")
    isoline_extraction(point_dtm, isoline_interval=2, filename="./data/isoline/ground")


if __name__ == '__main__':
    main()
