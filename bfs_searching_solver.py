import random
import copy

class LinearDiskMovement(object):
    def __init__(self, length, n, disk):
        self.length = length
        self.n = n
        self.disk = disk
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
                else:
                    return False
            else:
                return False

    def is_solve_identical_disks(self):
        c = 0
        for i in range(self.length - self.n, self.length):
            if self.disk[i] == 0:
                return False
            c += 1
        return True

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
        successors_list =[]
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


def solve_identical_disks(length, n):
    disk = LinearDiskMovement(length, n, [])
    sol_list = []
    visited_node = {}
    frontier_list = [disk]
    while len(frontier_list) != 0:
        parent_node = frontier_list.pop(0)
        for move, children_node in parent_node.disk_successors():
            children_node_key = tuple(children_node.disk)
            if children_node_key not in visited_node:
                visited_node[children_node_key] = [move]
                if children_node.is_solve_identical_disks():
                    while disk.disk != children_node.disk:
                        temp_children_node_key = tuple(children_node.disk)
                        move_list = visited_node[temp_children_node_key]
                        sol_list = sol_list + move_list
                        children_node.perform_disk_move(move_list[0][1], move_list[0][0])
                    return list(reversed(sol_list))
            else:
                continue
            frontier_list.append(children_node)


def solve_distinct_disks(length, n):
    disk = LinearDiskMovement(length, n, [])
    sol_list = []
    visited_node = {}
    frontier_list = [disk]
    while len(frontier_list) != 0:
        parent_node = frontier_list.pop(0)
        for move, children_node in parent_node.disk_successors():
            children_node_key = tuple(children_node.disk)
            if children_node_key not in visited_node:
                visited_node[children_node_key] = [move]
                if children_node.is_solve_distinct_disks():
                    while disk.disk != children_node.disk:
                        temp_children_node_key = tuple(children_node.disk)
                        move_list = visited_node[temp_children_node_key]
                        sol_list = sol_list + move_list
                        children_node.perform_disk_move(move_list[0][1], move_list[0][0])
                    return list(reversed(sol_list))
            else:
                continue
            frontier_list.append(children_node)
