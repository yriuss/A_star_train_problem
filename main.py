import numpy as np

from utils import *
from A_star import *

DISTS_PATH = "dists.csv"
REAL_DISTS_PATH = "real_dists.csv"

# Velocity in km per hour
TRAIN_VELOCITY = 40


# Transforms distance (km) to time, considering 40 km/h
def convert_values(mat):
	return 60*mat/40

def main():
	m_dists = read_matrix(DISTS_PATH)
	m_real_dists = read_matrix(REAL_DISTS_PATH)


	m_dists = convert_values(m_dists)
	m_real_dists = convert_values(m_real_dists)

	#print(m_dists)

	algorithm = A_star("E1r", "E7b",m_real_dists, m_dists)

	path = algorithm.run()

	print(path)

	algorithm.plot_tree()

if(__name__ == "__main__"):
	main()
