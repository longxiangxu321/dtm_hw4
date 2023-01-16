import os
import laspy
import scipy
import numpy as np


def cloth_fitting(xmin, ymin, steps, las):
    # creating grids over the pts
    grid_x = np.linspace(xmin, xmin + 500, steps)
    grid_y = np.linspace(ymin, ymin + 500, steps)
    x, y = np.meshgrid(grid_x, grid_y)  # the 4 vertices of each grid
    particle_tree = scipy.spatial.KDTree(np.c_[x.ravel(), y.ravel()])
    # Access the xyz values of each pt as array
    point_coords = np.vstack((las.x, las.y, las.z)).transpose()
    point_tree = scipy.spatial.KDTree(point_coords[:, 0:2])
    dist, indices = point_tree.query(particle_tree.data)
    lowest = -point_coords[indices][:,2]
    breakpoint()


def main():
    xmin = 191952.41724297937
    ymin = 325068.92101974826
    step = 0.5
    steps = int(500 / step)
    las = laspy.read(os.path.abspath('roi.laz'))
    cloth_fitting(xmin, ymin, steps, las)


if __name__ == '__main__':
    main()