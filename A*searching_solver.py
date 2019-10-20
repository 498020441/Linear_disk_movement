class LinearDiskMovement(object):
    def __init__(self, length, n, disk):
        self.length = length
        self.n = n
        self.f = 0
        self.disk = disk
        self.move = []
        if len(disk) == 0:
            self.disk = [0 for i in range(self.length)]
            for i in range(n):
                self.disk[i] = i+1

    def get_disk(self):
        return self.disk

    def perform_disk_move(self, disk_from, disk_to):
        if (abs(disk_from - disk_to) > 2) or (abs(disk_from - disk_to) == 0) \
                or (disk_from < 0) or (disk_to < 0) or(disk_to > (self.length-1)):
            return False
        else:
            if self.disk[disk_to] == 0 and self.disk[disk_from] > 0:
                if abs(disk_to - disk_from) == 1:
                    self.disk[disk_to] = self.disk[disk_from]
                    self.disk[disk_from] = 0
                    return True
                elif (disk_to - disk_from == 2) and not self.disk[disk_from+1] == 0:
                    self.disk[disk_to] = self.disk[disk_from]
                    self.disk[disk_from] = 0
                    return True
                elif (disk_to - disk_from == -2) and not self.disk[disk_from-1] == 0:
                    self.disk[disk_to] = self.disk[disk_from]
                    self.disk[disk_from] = 0
                    return True
        return False

    def is_solve_distinct_disks(self):
        c = 0
        for i in range(self.length-self.n, self.length):
            if not self.disk[i] == self.n-c:
                return False
            c += 1
        return True

    def disk_copy(self):
        return LinearDiskMovement(copy.deepcopy(self.length), copy.deepcopy(self.n), copy.deepcopy(self.disk))

    def disk_successors(self):
        successors_list = []
        i = 0
        while i < self.length:
            successors = self.disk_copy()
            if successors.perform_disk_move(i, i + 1):
                successors_list.append([(i, i+1), successors])
            successors = self.disk_copy()
            if successors.perform_disk_move(i, i-1):
                successors_list.append([(i, i-1), successors])
            successors = self.disk_copy()
            if successors.perform_disk_move(i, i+2):
                successors_list.append([(i, i+2), successors])
            successors = self.disk_copy()
            if successors.perform_disk_move(i, i-2):
                successors_list.append([(i, i-2), successors])
            i += 1
        result = (elem for elem in successors_list)
        return result

    def get_h_value(self):
        check_dict = {}
        c, h = 0, 0
        for i in range(self.length-self.n, self.length):
            check_dict[self.n-c] = i
            c += 1
        for i in range(self.length):
            if self.disk[i] > 0:
                h += abs(i - check_dict[self.disk[i]])
        return h


def solve_distinct_disks(length, n):
    if length == n:
        return []
    disk = LinearDiskMovement(length, n, [])
    visited = set()
    open_q = PQ()
    index = 0
    disk.f = disk.get_h_value()
    open_q.put((disk.f, index, disk))
    while not open_q.empty():
        get_node = open_q.get()
        parent_node = get_node[2]
        if parent_node.is_solve_distinct_disks():
            return parent_node.move
        for move, children_node in parent_node.disk_successors():
            if children_node not in visited:
                index += 1
                children_node.f = parent_node.f + children_node.get_h_value()
                children_node.move = parent_node.move + [move]
                visited.add(children_node)
                open_q.put((children_node.f, index, children_node))
    return None
