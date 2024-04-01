import pandas as pd
import numpy as np

def read_matrix(path):
	
	df = pd.read_csv(path, header=None)
	df = df.replace({',': '.'}, regex=True).astype(float)

    
	dists_mat = df.values
	dists_mat = np.nan_to_num(dists_mat)
	dists_mat += dists_mat.T
	
    # treates every zeroes, except the ones in the diagonal, as inf
	mask = (dists_mat == 0) & ~np.eye(dists_mat.shape[0], dtype=bool)
	dists_mat[mask] = np.inf

	return dists_mat