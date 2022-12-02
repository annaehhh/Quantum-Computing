from dimod.generators import and_gate
from dimod import ExactSolver

import re

from maze import get_maze_bqm, Maze

# Create maze
n_rows = 3
n_cols = 3
start = '0,1n'              # maze entrance location
end = '2,0w'                # maze exit location
walls = ['2,2w']            # maze interior wall locations

# Construct BQM
m = Maze(n_rows, n_cols, start, end, walls)
bqm = and_gate('in1', 'in2', 'out')

# Submit BQM to a D-Wave sampler
sampler = ExactSolver()
result = sampler.sample(bqm,
                        num_reads=1000,
                        chain_strength=2,
                        label='Example - Maze')

sampleset = sampler.sample(bqm)
# Interpret result
# Note: when grabbing the path, we are only grabbing path segments that have
#   been "selected" (i.e. indicated with a 1).
# Note2: in order construct the BQM such that the maze solution corresponds to
#   the ground energy, auxiliary variables
#   may have been included in the BQM. These auxiliary variables are no longer
#   useful once we have our result. Hence, we can just ignore them by filtering
#   them out with regex (i.e. re.match(r"^aux(\d+)$", k)])
path = [k for k, v in result.first.sample.items() if v==1
            and not re.match(r"^aux(\d+)$", k)]

print(sampleset)
# Visualize maze path
m.visualize(path)
print("\n")
print(result.first.sample)