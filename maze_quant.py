from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dwave.inspector
import itertools
import re

from maze import get_maze_bqm, Maze

# Create maze
n_rows = 2
n_cols = 3
start = '0,0n'              # maze entrance location
end = '1,0w'                # maze exit location
walls = []            # maze interior wall locations

# Construct BQM
m = Maze(n_rows, n_cols, start, end, walls)
bqm = m.get_bqm() #AE: schmeißt alle Werte raus, die Mauern haben etc. 
#list(bqm) #AE:listet alle Variablen des BQM auf

# Submit BQM to a D-Wave sampler
sampler = EmbeddingComposite(DWaveSampler())
result = sampler.sample(bqm,
                        num_reads=1000,
                        chain_strength=2,
                        label='Example - Maze')

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

# Visualize maze path
m.visualize(path)
print("\n")
print(result.first.sample)

print(bqm)

dwave.inspector.show(result)
