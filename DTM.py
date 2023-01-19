import os
import laspy
import scipy
import numpy as np
import startinpy
from numpy import genfromtxt
import math
import csv


def cloth_dtm(cloth_file):
    cloth_pts = genfromtxt(cloth_file, delimiter=',')
    x_array = cloth_pts[:, :1]
    y_array = cloth_pts[:, 1:2]
    xmin, ymin = min(x_array)[0], min(y_array)[0]
    xmax, ymax = max(x_array)[0], max(y_array)[0]
    step_x = int((xmax - xmin) / 0.5)
    step_y = int((ymax - ymin) / 0.5)
    grid_x = np.linspace(xmin, xmax, step_x)
    grid_y = np.linspace(ymin, ymax, step_y)
    x, y = np.meshgrid(grid_x, grid_y)
    new_grid = np.c_[x.ravel(), y.ravel()]
    dt = startinpy.DT()
    for line in cloth_pts:
        p = list(map(float, line))
        assert(len(p) == 3)
        dt.insert_one_pt(p[0], p[1], p[2])
    z = []
    for i in range(len(new_grid)):
        ptx = new_grid[i][0]
        pty = new_grid[i][1]
        ptz = dt.interpolate_laplace(ptx, pty)
        z.append(ptz)
    z_ = np.array(z).reshape(-1, 1)
    cloth_dtm = np.concatenate((new_grid, z_), axis=1)
    np.savetxt('cloth_dtm_0.5.csv', cloth_dtm, delimiter=',')
    # breakpoint()


cloth_dtm('cloth_50.csv')