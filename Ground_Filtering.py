import os
import laspy
import scipy
import numpy as np
from numpy import genfromtxt
import csv
import startinpy
import math


def dist_to_dt(p0, p1, p2, tp):
    # calculate the normal vector of the incident triangle
    vector_a = p1 - p0
    vector_b = p2 - p0
    normal_vector = np.cross(vector_a, vector_b)
    # the distance from point(tp) to the triangle equals to orthogonal projection of tp_p0 on the normal vector
    vector_tp_po = tp - p0
    normal_length = np.linalg.norm(normal_vector)
    dist = abs(np.dot(vector_tp_po, normal_vector)) / normal_length
    return dist


def ground_filtering_dt(cloth_file, roi, dist_max):
    cloth_pts = genfromtxt(cloth_file, delimiter=',')
    roi_pt = np.vstack((roi.x, roi.y, roi.z)).transpose()
    dt = startinpy.DT()
    for line in cloth_pts:
        p = list(map(float, line))
        assert(len(p) == 3)
        dt.insert_one_pt(p[0], p[1], p[2])
    # pts = dt.points[1:]

    ground = []
    non_ground = []
    for i in range(len(roi_pt)):
        triangle = dt.locate(roi_pt[i][0], roi_pt[i][1])
        p0 = dt.get_point(triangle[0])
        p1 = dt.get_point(triangle[1])
        p2 = dt.get_point(triangle[2])
        dist_dt = dist_to_dt(p0, p1, p2, roi_pt[i])
        if dist_dt < dist_max:
            ground.append([roi_pt[i][0], roi_pt[i][1], roi_pt[i][2]])
        else:
            non_ground.append([roi_pt[i][0], roi_pt[i][1], roi_pt[i][2]])
    ground_ = np.array(ground)
    non_ground_ = np.array(non_ground)
    # breakpoint()
    np.savetxt('ground_filter_1.csv', ground_, delimiter=',')
    np.savetxt('non_ground_filter_1.csv', non_ground_, delimiter=',')
    return ground_, non_ground_


las = laspy.read(os.path.abspath('roi.laz'))
ground_filtering_dt('cloth_50.csv', las, 1)
