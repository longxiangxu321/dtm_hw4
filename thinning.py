import numpy as np
import laspy


def random_thinning(las, remain_percentage, outfolder):
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
    file_name = '{}/random_thinned_{}%.laz'.format(outfolder, remain_percentage)
    points_thinned_las.write(file_name)
    return points_thinned


def nth_point_thinning(las, remain_percentage, outfolder):
    points = np.vstack((las.x, las.y, las.z)).transpose()
    original_pt_number = points.shape[0]
    indices = np.linspace(0, original_pt_number, int(original_pt_number * (remain_percentage / 100)),
                          endpoint=False, dtype=int)
    points_thinned = points[indices]
    header = las.header
    header.point_count = 0
    points_thinned_las = laspy.LasData(header)
    points_thinned_las.x = points_thinned[:, 0]
    points_thinned_las.y = points_thinned[:, 1]
    points_thinned_las.z = points_thinned[:, 2]
    file_name = '{}/nth_thinned_{}%.laz'.format(outfolder, remain_percentage)
    points_thinned_las.write(file_name)
    return points_thinned


def main():
    # crop(pdok_file)
    las = laspy.read('./data/pointcloud/roi.laz')
    nth_point_thinning(las, 10, outfolder="./data/pointcloud")
    nth_point_thinning(las, 50, outfolder="./data/pointcloud")
if __name__ == '__main__':
    main()


