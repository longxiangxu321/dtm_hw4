import numpy as np
import scipy
import laspy
import startinpy


def cloth_fitting(resolution, las, max_iter, tension, gravity, threshold):
    xmin = las.header.mins[0]
    ymin = las.header.mins[1]
    xmax = las.header.maxs[0]
    ymax = las.header.maxs[1]
    height = ymax-ymin
    width = xmax-xmin
    steps_x = int(width / resolution)
    steps_y = int(height / resolution)
    grid_x = np.linspace(xmin, xmax, steps_x)
    grid_y = np.linspace(ymin, ymax, steps_y)
    x, y = np.meshgrid(grid_x, grid_y)
    particle_tree = scipy.spatial.KDTree(np.c_[x.ravel(), y.ravel()])
    point_coords = np.vstack((las.x, las.y, las.z)).transpose()
    point_tree = scipy.spatial.KDTree(point_coords[:, 0:2])
    dist, indices = point_tree.query(particle_tree.data)
    lowest_ = -point_coords[indices][:, 2]
    start_z = max(lowest_)
    lowest_2d = np.reshape(lowest_, (steps_x, steps_y))
    start_particles = np.full((steps_x, steps_y), start_z) + 1
    threshold = np.full((steps_x, steps_y), threshold)
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
    header = las.header
    header.point_count = 0
    cloth_las = laspy.LasData(las.header)
    cloth_las.x = cloth[:, 0]
    cloth_las.y = cloth[:, 1]
    cloth_las.z = cloth[:, 2]
    cloth_las.write("cloth_points.laz")
    return cloth


def internal_force(particle_arr, tension):
    t = tension
    kernel = [[0, t / 2, 0],
              [t / 2, -2 * t, t / 2],
              [0, t / 2, 0]]
    internal_forces = scipy.signal.convolve2d(particle_arr, kernel, mode='same', boundary="wrap")
    return internal_forces


def ground_filter(cloth, las, threshold):
    cloth_dt = startinpy.DT()
    cloth_dt.insert(cloth)
    standard_ = []
    for i in range(len(las.x)):
        z = cloth_dt.interpolate_tin_linear(las.x[i], las.y[i])
        standard_.append(z)
    standard = np.array(standard_)
    ground_idx = np.where(np.abs(standard - las.z) <= threshold)[0]
    non_ground_idx = np.where(np.abs(standard - las.z) > threshold)[0]

    ground_point = las.points[ground_idx]
    non_ground_point = las.points[non_ground_idx]

    ground_las = laspy.LasData(las.header)
    non_ground_las = laspy.LasData(las.header)

    ground_las.points = ground_point.copy()
    non_ground_las.points = non_ground_point.copy()

    ground_las.write("ground_points.laz")
    non_ground_las.write("non_ground_points.laz")


def main():
    resolution = 4
    tension = 0.5
    gravity = 0.3
    max_iter = 500
    threshold = 0.1
    z_tolerance = 0.3
    las = laspy.read('roi.laz')
    cloth = cloth_fitting(resolution, las, max_iter, tension, gravity, threshold)
    ground_filter(cloth, las, z_tolerance)


if __name__ == '__main__':
    main()
