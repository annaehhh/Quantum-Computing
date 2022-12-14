import dwavebinarycsp





def get_label(start, end, length):
    """Provides a string that follows a standard format for naming constraint variables in Maze.
    Namely, "<row_index>,<column_index><north_or_west_direction>".
    Args:
        row: Integer. Index of the row.
        col: Integer. Index of the column.
        direction: String in the set {'n', 'w'}. 'n' indicates north and 'w' indicates west.
    """
    return "{start},{end}{length}".format(**locals())

def sum_to_two_or_zero(*args):
    """Checks to see if the args sum to either 0 or 2.
    """
    sum_value0 = sum(args[0])
    sum_value1 = sum(args[1])
    return ((sum_value0 == 1 and sum_value1 == 1) or (sum_value0 == 0 and sum_value1 == 0))

class Ferrylines:

    def __init__(self, Routes):
        self.Routes   = Routes
        self.ports      = set([])
        for route in self.Routes:
            self.ports.add(route[0])
            self.ports.add(route[1])
        self.csp        = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

    def create_constraints(self):
        for port in self.ports:
            directions = [[],[]]
            for route in self.Routes:
                if (route[0]==port):
                    directions[0].append("to"+get_label(route[0],route[1],route[2]))
                if (route[1]==port):
                    directions[1].append("from"+get_label(route[1],route[0],route[2]))
            self.csp.add_constraint(sum_to_two_or_zero, directions)
                

    def get_bqm(self):
        self._apply_valid_move_constraint()

        bqm = dwavebinarycsp.stitch(self.csp)

        print(bqm.to_polystring())
        return bqm


if __name__ == "__main__":
    routes = [
        ["Hamburg"  , "Helgoland", 20],
        ["Hamburg"  , "Romo", 60],
        ["Romo"     , "Esberg", 20],
        ["Helgoland", "Esberg", 10],
        ["Hamburg"  , "London", 10],
    ]

    f = Ferrylines(routes)
    bqm = f.get_bqm



