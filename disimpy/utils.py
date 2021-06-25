"""This module contains general useful functions."""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def vec2vec_rotmat(v, k):
    """Return a rotation matrix defining a rotation that aligns v with k.

    Parameters
    -----------
    v : numpy.ndarray
        1D array of length 3.
    k : numpy.ndarray
        1D array of length.

    Returns
    ---------
    R : numpy.ndarray
        3 by 3 rotation matrix.
    """
    v = v / np.linalg.norm(v)
    k = k / np.linalg.norm(k)
    axis = np.cross(v, k).astype(np.float)
    if np.linalg.norm(axis) < np.finfo(float).eps:
        if np.linalg.norm(v - k) > np.linalg.norm(v):
            return -np.eye(3)
        else:
            return np.eye(3)
    axis /= np.linalg.norm(axis)
    angle = np.arcsin(np.linalg.norm(np.cross(v, k)) /
                      (np.linalg.norm(k) * np.linalg.norm(v)))
    if np.dot(v, k) < 0:
        angle = np.pi - angle
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]],
                  [-axis[1], axis[0], 0]])
    R = np.eye(3) + \
        np.sin(angle) * K + \
        (1 - np.cos(angle)) * np.matmul(K, K)  # Rodrigues' rotation formula
    return R


def show_traj(traj_file, show=True):
    """Visualize walker trajectories saved in a trajectories file.

    Parameters
    ----------
    traj_file : str
        Path to trajectories file that contains walker trajectories. Every line
        represents a time point. Every line contains the positions as follows:
        walker_1_x walker_1_y walker_1_z walker_2_x walker_2_y walker_2_z...
    show : bool
        Whether to render the figure.

    Returns
    -------
    None
    """
    trajectories = np.loadtxt(traj_file)
    trajectories = trajectories.reshape((trajectories.shape[0],
                                         int(trajectories.shape[1] / 3),
                                         3))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(trajectories.shape[1]):
        ax.plot(trajectories[:, i, 0],
                trajectories[:, i, 1],
                trajectories[:, i, 2],
                alpha=.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.ticklabel_format(style='sci', scilimits=(0, 0))
    fig.tight_layout()
    if show:
        plt.show()
    else:
        plt.close(fig)
    return


def show_mesh(mesh, show=True):
    """Visualize the triangular mesh with random triangle colours.

    Parameters
    ----------
    mesh : numpy.ndarray
        Mesh array of shape (n of triangles, 3, 3) where the second dimension
        indices correspond to different triangle points and the third dimension
        is the Cartesian coordinates of triangle.
    show : bool
        Whether to render figure or not.

    Returns
    -------
    None
    """
    np.random.seed(123)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    mesh_min = np.min(np.min(mesh, 0), 0)
    mesh_max = np.max(np.max(mesh, 0), 0)
    ax.set_xlim([mesh_min[0], mesh_max[0]])
    ax.set_ylim([mesh_min[1], mesh_max[1]])
    ax.set_zlim([mesh_min[2], mesh_max[2]])
    for triangle in mesh:
        A = triangle[0, :]
        B = triangle[1, :]
        C = triangle[2, :]
        vtx = np.array([A, B, C])
        tri = Poly3DCollection([vtx], alpha=.5)
        face_color = np.random.random(3)
        tri.set_facecolor(face_color)
        ax.add_collection3d(tri)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.ticklabel_format(style='sci', scilimits=(0, 0))
    fig.tight_layout()
    if show:
        plt.show()
    else:
        plt.close(fig)
    return
