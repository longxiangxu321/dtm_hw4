import os
import laspy
import numpy as np


def ground_roi():
    las = laspy.read(os.path.abspath('roi.laz'))
    ground_file = laspy.create(point_format=las.header.point_format, file_version=las.header.version)
    ground_file.points = las.points[las.classification == 2]
    g_pt = np.vstack((ground_file.x, ground_file.y, ground_file.z)).transpose()
    # breakpoint()
    np.savetxt(os.path.abspath("roi_ground.csv"), g_pt, delimiter=",")


ground_roi()