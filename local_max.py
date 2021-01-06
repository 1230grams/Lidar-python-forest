import numpy as np

def local_max(pd_array, radius, density_threshold=0):
    '''

    Returns points that are local max values

    Parameters
    ----------
    pd_array - array created with pdal
    radius - local max radius
    '''

    box = pd_array.loc[:,['X_0','Y_0','Z_0','HeightAboveGround']]
    for i in range(2):
        box['X{}'.format(i)] = ((box['X_0']/radius + i) /2).astype(int)*2
        box['Y{}'.format(i)] = ((box['Y_0']/radius + i) /2).astype(int)*2
    box['X_'] = (box['X_0']/radius).astype(int)
    box['Y_'] = (box['Y_0']/radius).astype(int)
    for i in range(2):
        for j in range(2):
            box[str(i)+str(j)] = box.groupby(['X{}'.format(i), 'Y{}'.format(j)])['Z_0'].transform(np.max)
    density = box.groupby(['X_','Y_'])['Z_0'].transform(len)
    is_max = (box['00'] == box['10']) & (box['10'] == box['01']) & (box['01'] == box['11']) & (box['11'] == box['Z_0'])
    return pd_array[is_max & (density >= (density_threshold))]