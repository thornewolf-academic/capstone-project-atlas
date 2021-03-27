import numpy as np
import math
import progressbar
from time import sleep

def surface_match(dataset1, dataset2):

    overlap_plane1 = []
    overlap_plane2 = []
    dataset2_rotated = np.zeros([len(dataset2),3])
    qhat = np.zeros([1,3])
    print('FINDING OVERLAP...')
    for u in range(0,len(dataset1)):
        for v in range(0,len(dataset2)):
            x_1 = dataset1[u,1]
            y_1 = dataset1[u,2]
            x_2 = dataset2[v,1]
            y_2 = dataset2[v,2]
            dist = math.sqrt(((x_2-x_1)**2 + ((y_2-y_1)**2)))
            if dist <= 0.5:
                overlap_plane1val = dataset1[u,:]
                overlap_plane2val = dataset2[v,:]
                overlap_plane1.append(overlap_plane1val)
                overlap_plane2.append(overlap_plane2val)
            elif len(overlap_plane1) == 9 and len(overlap_plane2) == 9:
                break

    overlap_plane1_1 = overlap_plane1[0]
    overlap_plane1_2 = overlap_plane1[1]
    overlap_plane1_3 = overlap_plane1[2]
    overlap_plane1_4 = overlap_plane1[3]
    overlap_plane1_5 = overlap_plane1[4]
    overlap_plane1_6 = overlap_plane1[5]
    overlap_plane1_7 = overlap_plane1[6]
    overlap_plane1_8 = overlap_plane1[7]
    overlap_plane1_9 = overlap_plane1[8]
    overlap_plane2_1 = overlap_plane2[0]
    overlap_plane2_2 = overlap_plane2[1]
    overlap_plane2_3 = overlap_plane2[2]
    overlap_plane2_4 = overlap_plane2[3]
    overlap_plane2_5 = overlap_plane2[4]
    overlap_plane2_6 = overlap_plane2[5]
    overlap_plane2_7 = overlap_plane2[6]
    overlap_plane2_8 = overlap_plane2[7]
    overlap_plane2_9 = overlap_plane2[8]

    A_1_1 = overlap_plane1_1[[1,2,3]]
    A_1_2 = overlap_plane1_4[[1,2,3]]
    A_1_3 = overlap_plane1_7[[1,2,3]]
    A_2_1 = overlap_plane2_1[[1,2,3]]
    A_2_2 = overlap_plane2_4[[1,2,3]]
    A_2_3 = overlap_plane2_7[[1,2,3]]
    B_1_1 = overlap_plane1_2[[1,2,3]]
    B_1_2 = overlap_plane1_5[[1,2,3]]
    B_1_3 = overlap_plane1_8[[1,2,3]]
    B_2_1 = overlap_plane2_2[[1,2,3]]
    B_2_2 = overlap_plane2_5[[1,2,3]]
    B_2_3 = overlap_plane2_8[[1,2,3]]
    C_1_1 = overlap_plane1_3[[1,2,3]]
    C_1_2 = overlap_plane1_6[[1,2,3]]
    C_1_3 = overlap_plane1_9[[1,2,3]]
    C_2_1 = overlap_plane2_3[[1,2,3]]
    C_2_2 = overlap_plane2_6[[1,2,3]]
    C_2_3 = overlap_plane2_9[[1,2,3]]

    plane1_vec1_1 = B_1_1-A_1_1
    plane1_vec1_2 = B_1_2-A_1_2
    plane1_vec1_3 = B_1_3-A_1_3
    plane1_vec2_1 = C_1_1-B_1_1
    plane1_vec2_2 = C_1_2-B_1_2
    plane1_vec2_3 = C_1_3-B_1_3
    n_1_1 = np.cross(plane1_vec1_1,plane1_vec2_1)
    n_1_2 = np.cross(plane1_vec1_2,plane1_vec2_2)
    n_1_3 = np.cross(plane1_vec1_3,plane1_vec2_3)
    norm_n_1_1 = np.linalg.norm(n_1_1)
    norm_n_1_2 = np.linalg.norm(n_1_2)
    norm_n_1_3 = np.linalg.norm(n_1_3)
    n_1_1 = n_1_1/norm_n_1_1
    n_1_2 = n_1_2/norm_n_1_2
    n_1_3 = n_1_3/norm_n_1_3
    n_1 = np.array([np.mean([n_1_1[0],n_1_2[0],n_1_3[0]]), np.mean([n_1_1[1],n_1_2[1],n_1_3[1]]), np.mean([n_1_1[2],n_1_2[2],n_1_3[2]])])
    norm_n_1 = np.linalg.norm(n_1)
    plane2_vec1_1 = B_2_1-A_2_1
    plane2_vec1_2 = B_2_2-A_2_2
    plane2_vec1_3 = B_2_3-A_2_3
    plane2_vec2_1 = C_2_1-B_2_1
    plane2_vec2_2 = C_2_2-B_2_2
    plane2_vec2_3 = C_2_3-B_2_3
    n_2_1 = np.cross(plane2_vec1_1,plane2_vec2_1)
    n_2_2 = np.cross(plane2_vec1_2,plane2_vec2_2)
    n_2_3 = np.cross(plane2_vec1_3,plane2_vec2_3)
    norm_n_2_1 = np.linalg.norm(n_2_1)
    norm_n_2_2 = np.linalg.norm(n_2_2)
    norm_n_2_3 = np.linalg.norm(n_2_3)
    n_2_1 = n_2_1/norm_n_2_1
    n_2_2 = n_2_2/norm_n_2_2
    n_2_3 = n_2_3/norm_n_2_3
    n_2 = np.array([np.mean([n_2_1[0],n_2_2[0],n_2_3[0]]), np.mean([n_2_1[1],n_2_2[1],n_2_3[1]]), np.mean([n_2_1[2],n_2_2[2],n_2_3[2]])])
    norm_n_2 = np.linalg.norm(n_2)
    rot_angle = np.arccos(np.dot(n_1,n_2)/(norm_n_1*norm_n_2)) + (math.pi/2)
    n_0 = np.cross(n_1,n_2)
    qhat = [n_0[0]*np.sin(rot_angle/2), n_0[1]*np.sin(rot_angle/2), n_0[2]*np.sin(rot_angle/2)]
    u = np.asarray(qhat)
    q4 = np.cos(rot_angle/2)
    s = q4
    quat = np.append(qhat,q4)
    quat = np.asarray(quat)
    qstar = np.conj(quat)
    original_x = dataset2[:,1]
    original_y = dataset2[:,2]
    print('MOVING DATASET...')
    for kk in range(0,len(dataset2)):
        v = dataset2[kk,1:4]
        dataset2_rotated[kk,:] = 2*np.dot(u,v)*u + (s**2 - np.dot(u,u))*v + 2*s*np.cross(u,v)
    new_z = dataset2_rotated[:,2]
    new_L = np.ones(len(dataset2_rotated))
    dataset2_rotated = np.column_stack((new_L,original_x,original_y,new_z))

    return dataset2_rotated 