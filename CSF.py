import numpy as np
import scipy
import laspy
from copy import copy


# cloth simulation
# particles being represented grids
# the lowest possible value will be found using nearest neighbour functions

def cloth_fitting(steps, las, max_iter, tension, gravity, threshold):
    xmin = las.header.mins[0]
    ymin = las.header.mins[1]
    grid_x = np.linspace(xmin, xmin + 500, steps)
    grid_y = np.linspace(ymin, ymin + 500, steps)
    x, y = np.meshgrid(grid_x, grid_y)
    particle_tree = scipy.spatial.KDTree(np.c_[x.ravel(), y.ravel()])
    point_coords = np.vstack((las.x, las.y, las.z)).transpose()
    point_tree = scipy.spatial.KDTree(point_coords[:, 0:2])
    dist, indices = point_tree.query(particle_tree.data)
    lowest_ = -point_coords[indices][:, 2]
    start_z = max(lowest_)
    lowest_2d = np.reshape(lowest_, (-1, steps))
    start_particles = np.full((steps, steps), start_z) + 1
    threshold = np.full((steps, steps), threshold)
    # breakpoint()
    for i in range(max_iter):
        internal = internal_force(start_particles, tension)
        new_particles = np.where((start_particles > lowest_2d) & (np.fabs(internal - gravity) > threshold),
                                 start_particles + internal - gravity,
                                 start_particles)
        start_particles = np.where(new_particles < lowest_2d, lowest_2d, new_particles)

    particles = start_particles.ravel()
    particles_ = np.reshape(particles.ravel(), (-1, 1))
    particles_ = - particles_
    cloth = np.concatenate((particle_tree.data, particles_), axis=1)
    np.savetxt("cloth_50.csv", cloth, delimiter=",")
    return cloth


def internal_force(particle_arr, tension):
    t = tension
    kernel = [[0, t / 2, 0],
              [t / 2, -2 * t, t / 2],
              [0, t / 2, 0]]
    internal_forces = scipy.signal.convolve2d(particle_arr, kernel, mode='same', boundary="wrap")
    return internal_forces


def ground_filter(cloth, las, threshold):
    point_coords = np.vstack((las.x, las.y, las.z)).transpose()
    cloth_tree = scipy.spatial.KDTree(cloth[:, 0:2])
    dist, indices = cloth_tree.query(point_coords[:, 0:2])
    standard_ = cloth[indices][:, 2]
    idx = np.where(np.abs(standard_ - las.z) <= threshold)[0]
    ground_point = point_coords[idx]
    header = copy(las.header)
    header.point_count = 0
    ground_las = laspy.LasData(header)
    las.header.point_count = idx.shape[0]
    ground_las.X = ground_point[:, 0]
    ground_las.Y = ground_point[:, 1]
    ground_las.Z = ground_point[:, 2]

    ground_las.write("ground_points.laz")
    return ground_point


def main():
    spacing = 4
    steps = int(500 / spacing)
    tension = 0.5
    gravity = 0.3
    max_iter = 500
    threshold = 0.1
    z_tolerance = 0.5
    las = laspy.read('roi.laz')
    cloth = cloth_fitting(steps, las, max_iter, tension, gravity, threshold)
    ground_point = ground_filter(cloth, las, z_tolerance)
    print("total ground points:", ground_point.shape[0])


if __name__ == '__main__':
    main()
