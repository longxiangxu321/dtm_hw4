import numpy as np
import scipy
import laspy
import startinpy


def random_thinning(las, remain_percentage, outputfoldder):
    points = np.vstack((las.x, las.y, las.z)).transpose()
    original_pt_number = points.shape[0]
    remove_pt_number = original_pt_number - int(round(original_pt_number * (remain_percentage / 100), 0))
    random_indices = np.random.choice(original_pt_number, size=remove_pt_number, replace=False)
    points_thinned = np.delete(points, random_indices, 0)

    # export thinned points laz file
    header = las.header
    header.point_count = 0
    points_thinned_las = laspy.LasData(header)
    points_thinned_las.x = points_thinned[:, 0]
    points_thinned_las.y = points_thinned[:, 1]
    points_thinned_las.z = points_thinned[:, 2]
    file_name = '{}/random_thinned_{}%.laz'.format(outputfoldder, remain_percentage)
    points_thinned_las.write(file_name)
    return points_thinned


def nth_point_thinning(las, n_th):
    pass


def main():
    las = laspy.read('./data/pointcloud/roi.laz')
    random_thinning(las, 10, outputfoldder="./data/pointcloud")


if __name__ == '__main__':
    main()
