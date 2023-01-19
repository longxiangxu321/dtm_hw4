import laspy
import numpy as np


def main():
    xmin = 191952.41724297937
    ymin = 325068.92101974826

    with laspy.open("C_68GZ1.LAZ") as f:
        with laspy.open("roi.laz", mode="w", header=f.header) as writer:
            for points in f.chunk_iterator(50000000):
                X_in_valid = (xmin <= points.x) & (xmin + 500 >= points.x)
                Y_in_valid = (ymin <= points.y) & (ymin + 500 >= points.y)
                good_indices = np.where(X_in_valid & Y_in_valid)
                good_indices = good_indices[0].ravel()
                good_points = points[good_indices].copy()
                writer.write_points(good_points)
                print("done")


if __name__ == '__main__':
    main()
