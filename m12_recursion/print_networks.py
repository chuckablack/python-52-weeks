from m01_basics.util.create_utils import create_network
from random import randint


def traverse_and_print(node, indent):

    global visited

    # First check if we've been here before; if so, return immediately (don't recurse)
    if type(node) not in {str, int, bool, float, tuple}:
        if id(node) in visited:
            print("--- ### loop detected, returning ##########")
            return True

    # Add these data objects to the list of visited nodes
    visited.add(id(node))

    indent += 4
    if isinstance(node, dict):
        for key, value in node.items():
            print(f"{' '*indent}--+-{key}")
            traverse_and_print(node[key], indent)

    elif isinstance(node, list) or isinstance(node, tuple):
        for index in range(0, len(node)):
            print(f"{' '*indent}--+-{index}")
            traverse_and_print(node[index], indent)

    else:
        print(f"{' '*indent}----{node}")


def traverse_and_print_flat(node, indent):

    global visited

    # First check if we've been here before; if so, return immediately (don't recurse)
    if type(node) not in {str, int, bool, float, tuple}:
        if id(node) in visited:
            print("--- ### loop detected, returning ##########")
            return True

    # Add these data objects to the list of visited nodes
    visited.add(id(node))

    if isinstance(node, dict):
        first_time = True
        for key, value in node.items():
            if first_time:
                print(f"--+-{key}", end="")
                first_time = False
            else:
                print(f"{' '*indent}    {key}", end="")

            new_indent = indent + len("--+-") + len(key)
            traverse_and_print_flat(node[key], new_indent)

    elif isinstance(node, list) or isinstance(node, tuple):
        first_time = True
        for index in range(0, len(node)):
            if first_time:
                print(f"--+-{index}", end="")
                first_time = False
            else:
                print(f"{' '*indent}    {index}", end="")

            new_indent = indent + len("--+-") + len(str(index))
            traverse_and_print_flat(node[index], new_indent)

    else:
        print(f"----{node}")


if __name__ == "__main__":
    try:
        stack = list()
        visited = set()

        while True:
            network = create_network(num_devices=randint(2, 4), num_subnets=randint(4, 6))
            visited.clear()
            traverse_and_print(network, 4)
            print("\n\n")
            visited.clear()
            traverse_and_print_flat(network, 0)

            print(f"\n\n----- Printing Network ---------------------------------------------")
            do_another = input("Another? <cr> to do another, <ctrl-c> to quit")

    except KeyboardInterrupt:
        print("\n\nExiting print_networks")
        exit()
