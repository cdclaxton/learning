# Von Mises distribution
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

if __name__ == "__main__":
    loc = 0
    kappa = 1

    sample_size = 1000
    sample = stats.vonmises(loc=loc, kappa=kappa).rvs(sample_size)

    fig = plt.figure(figsize=(12, 6))
    left = plt.subplot(121)
    right = plt.subplot(122, projection="polar")
    x = np.linspace(-np.pi, np.pi, 500)
    vonmises_pdf = stats.vonmises.pdf(x, loc=loc, kappa=kappa)
    ticks = [0, 0.15, 0.3]

    left.plot(x, vonmises_pdf)
    left.set_yticks(ticks)
    number_of_bins = int(np.sqrt(sample_size))
    left.hist(sample, density=True, bins=number_of_bins)
    left.set_title("Cartesian plot")
    left.set_xlim(-np.pi, np.pi)
    left.grid(True)

    right.plot(x, vonmises_pdf, label="PDF")
    right.set_yticks(ticks)
    right.hist(sample, density=True, bins=number_of_bins, label="Histogram")
    right.set_title("Polar plot")
    right.legend(bbox_to_anchor=(0.15, 1.06))

    plt.show()
