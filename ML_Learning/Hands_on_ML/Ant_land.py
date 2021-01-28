import random
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

MAX_LAND = 4
HEAD = 1
TAIL = 0

pmf = [0.2, 0.15, 0.4, 0.25]
label = ['rose', 'violet', 'sunflower', 'lotus']

def flip_a_coin():
    return random.randint(0,1)
def to_the_west(index):
    if index - 1 == -1:
        return MAX_LAND - 1
    else:
        return index - 1
def to_the_east(index):
    if index + 1 == MAX_LAND:
        return 0
    else:
        return index + 1
def heuristics_solution(n_samples = 1000):
    samples = []

    current_land = random.randint(0, MAX_LAND - 1)
    samples.append(current_land)

    for i in range(n_samples):
        coin = flip_a_coin()
        if coin == HEAD:
            proposal_land = to_the_east(current_land)
        else:
            proposal_land = to_the_west(current_land)
        if pmf[proposal_land] > pmf[current_land]:
            samples.append(proposal_land)
            current_land = proposal_land
        else:
            if random.uniform(0,1) <= pmf[proposal_land] / pmf[current_land]:
                samples.append(proposal_land)
                current_land = proposal_land
            else:
                samples.append(current_land)
    return samples

if __name__ == '__main__':
    n_samples = 100000
    samples = heuristics_solution(n_samples)
    counter = Counter(samples)
    for i in range(MAX_LAND):
        print('%s: %f' %(label[i], counter[i]/n_samples))
    s = random.uniform(0,1)
    print(s)


