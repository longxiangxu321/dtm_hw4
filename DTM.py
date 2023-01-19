import laspy
import numpy as np
import rasterio
import startinpy


def generate_dtm(las, resolution, output_name):
    ll_x = min(las.x)
    ll_y = min(las.y)
    ur_x = max(las.x)
    ur_y = max(las.y)
    height = ur_y - ll_y
    width = ur_x - ll_x
    las_pts = np.vstack((las.x, las.y, las.z)).transpose()
    dt = startinpy.DT()
    dt.insert(las_pts)

    steps_x = int(width / resolution)
    steps_y = int(height / resolution)

    grid_x = np.linspace(ll_x, ur_x, steps_x)
    grid_y = np.linspace(ll_y, ur_y, steps_y)
    x, y = np.meshgrid(grid_x, grid_y)
    new_grid = np.c_[x.ravel(), y.ravel()]
    z = []
    for i in range(new_grid.shape[0]):
        ptx = new_grid[i][0]
        pty = new_grid[i][1]
        if dt.is_inside_convex_hull(ptx, pty):
            ptz = dt.interpolate_laplace(ptx, pty)
            z.append(ptz)
        else:
            z.append(np.nan)
    z_ = np.array(z).reshape(-1, 1)
    dtm = np.reshape(z_, (steps_x, steps_y))
    # dtm[dtm == -9999] = np.nan
    transform = rasterio.transform.from_origin(west=ll_x, north=ur_y, xsize=steps_x, ysize=steps_y)
    new_dataset = rasterio.open(
        output_name,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=dtm.dtype,
        transform=transform, )
    new_dataset.write(dtm, 1)


def main():
    cloth = laspy.read("cloth_points.laz")
    ground = laspy.read("ground_points.laz")
    resolution = 0.5
    # generate_dtm(cloth, resolution=resolution, output_name="cloth_dtm.tif")
    generate_dtm(ground, resolution=resolution, output_name="ground_dtm.tif")


if __name__ == '__main__':
    main()
