import numpy as np


class ScenarioGenerator:
  '''Class for generating sets of scenarios.'''

  def __init__(self, dists):
    '''
    Constructor for ScenarioGenerator class.

    Parameters
    ----------
    dists : list
      lists of scipy.stats distributions. Can include multivariate distributions.

    '''
    self.dists = dists

  def sample(self):
    '''Sample single outcome from each distribution, and
    return as list.'''
    samp = []
    for d in self.dists:
      s = d.rvs()
      if isinstance(s, np.ndarray):
        samp.extend(s)
      else:
        samp.append(s)
    return samp

  def generate(self, n):
    '''Sample n scenarios'''
    samples = []
    for i in range(n):
      samp = self.sample()
      samples.append(samp)
    return samples


if __name__ == '__main__':
  from scipy.stats import multivariate_normal, expon, uniform

  d1 = multivariate_normal([0.5, -0.2],
                           [[2.0, 0.3], [0.3, 0.5]])
  d2 = expon(scale=0.2)  # scale = 1/rate
  d3 = uniform()

  scengen = ScenarioGenerator([d1, d2, d3])
  samples = scengen.generate(5)
  print(samples)
