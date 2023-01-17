import os
import laspy
import scipy
import numpy as np
import math


# cloth simulation
# particles being represented grids
# the lowest possible value will be found using nearest neighbour functions

def cloth_fitting(xmin, ymin, steps, las, max_iter, tension, gravity):
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
    threshold = np.full((steps,steps), 0.1)
    # breakpoint()
    for i in range(max_iter):
        internal = internal_force(start_particles, tension)
        new_particles = np.where((start_particles > lowest_2d) & (np.fabs(internal - gravity) > threshold),
                                 start_particles + internal - gravity,
                                 start_particles)
        # new_particles = np.where(new_particles > lowest_2d, new_particles + internal, new_particles)
        start_particles = np.where(new_particles < lowest_2d, lowest_2d, new_particles)


    particles = start_particles.ravel()
    particles_ = np.reshape(particles.ravel(), (-1, 1))
    # breakpoint()
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


def main():
    xmin = 191952.4
    ymin = 325068.9
    spacing = 4
    steps = int(500 / spacing)
    tension = 0.3
    gravity = 0.3
    max_iter = 500
    # breakpoint()
    las = laspy.read('roi.laz')
    cloth = cloth_fitting(xmin, ymin, steps, las, max_iter, tension, gravity)


if __name__ == '__main__':
    main()