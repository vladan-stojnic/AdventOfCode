class Node:
    def __init__(self, name, node_type, parent=None, size=None):
        self.name = name
        self.type = node_type
        self.parent = parent
        self.children = []
        self.size = size


def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    data = data.splitlines()

    return data


def calculate_sizes(loc):
    if loc.size is None:
        loc.size = sum(calculate_sizes(c) for c in loc.children)

    return loc.size


def traverse_filesys(loc, find_dirs=None, dir_size=100000):
    # print(loc.name, loc.size)
    if find_dirs is not None:
        if loc.type == "dir" and loc.size <= dir_size:
            find_dirs.append(loc.size)
    if loc.children is not None:
        for child in loc.children:
            traverse_filesys(child, find_dirs=find_dirs, dir_size=dir_size)


data = read_input("day7")

head = None
current = head

for line in data:
    if line.startswith("$"):
        # TODO: this is a command so it need to be processed like that
        if line[2:4] == "cd":
            location = line[5:]
            if location == "/":
                if head == None:
                    head = Node("/", node_type="dir")
                    current = head
                else:
                    current = head
            elif location == "..":
                current = current.parent
            else:
                found = False
                for node in current.children:
                    if node.name == location:
                        current = node
                        found = True
                if not found:
                    raise ValueError("Specified location not found")
        elif line[2:4] == "ls":
            # do ls
            pass
        else:
            raise NotImplementedError("this command is not implemented")
    else:
        # TODO: this is just output of the previous command so it should be treated like that
        if line.startswith("dir"):
            current.children.append(
                Node(line[4:], node_type="dir", parent=current)
            )
        else:
            size, name = line.split(" ")
            current.children.append(
                Node(name, node_type="file", parent=current, size=int(size))
            )

calculate_sizes(head)

# Part 1

small_dirs = []
traverse_filesys(head, find_dirs=small_dirs)

print(f"Sum of sizes of small directories: {sum(small_dirs)}")

# Part 2

left_space = 70000000 - head.size
needed_space = 30000000
missing_space = needed_space - left_space

dir_sizes = []
traverse_filesys(head, find_dirs=dir_sizes, dir_size=float("inf"))

big_enough = []

for ds in dir_sizes:
    if ds > missing_space:
        big_enough.append(ds)

print(f"Minimal size that can be deleted: {min(big_enough)}")
