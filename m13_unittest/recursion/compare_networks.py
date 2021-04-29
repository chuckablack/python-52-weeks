from m01_basics.util.create_utils import create_network
from copy import deepcopy
import inspect
from pprint import pprint


def compare_data(data1, data2, stack, visited):

    # First check if we've been here before; if so, return immediately (don't recurse)
    if type(data1) not in {str, int, bool, float, tuple}:
        if id(data1) in visited or id(data2) in visited:
            print("--- ### loop detected, returning ##########")
            return True

    # Add these data objects to the list of visited nodes
    visited.add(id(data1)); visited.add(id(data2))

    if isinstance(data1, dict):
        if not isinstance(data2, dict): return False
        if len(data1) != len(data2): return False

        for key, value in data1.items():
            if key not in data2: return False
            stack.append("['"+key+"']")
            if not compare_data(data1[key], data2[key], stack, visited): return False
            stack.pop()

        return True

    elif isinstance(data1, list) or isinstance(data1, tuple):
        if type(data1) != type(data2): return False
        if len(data1) != len(data2): return False

        for index in range(0, len(data1)):
            stack.append("["+str(index)+"]")
            if not compare_data(data1[index], data2[index], stack, visited): return False
            stack.pop()

        return True

    elif isinstance(data1, set):
        if not isinstance(data2, set): return False
        for value in data1:
            if value not in data2: return False
        return True

    elif inspect.isclass(data1):
        if not inspect.isclass(data2): return False
        return True

    else:
        if data1 != data2: return False
        return True


def main():

    stack = list()
    visited = set()
    network1 = create_network(num_devices=4, num_subnets=4)
    network2 = deepcopy(network1)
    pprint(network1)

    print("\nCompare networks: should be identical --------------------")
    stack.clear(); visited.clear()
    compare_result = compare_data(network1, network2, stack, visited)
    print(f"--- compare_data result, should be True: {compare_result}")
    if not compare_result:
        print(f"--- --- comparison failed at location: network1{''.join(stack)}")

    print("\nCompare networks: change name --------------------")
    stack.clear(); visited.clear()
    network2["subnets"]["10.0.1.0"]["devices"][2]["name"] = "silly name"
    compare_result = compare_data(network1, network2, stack, visited)

    print(f"--- compare_data result, should be False: {compare_result}")
    if not compare_result:
        print(f"--- --- comparison failed at location: network1{''.join(stack)}")

    print("\nCompare networks: remove item --------------------")
    stack.clear(); visited.clear()
    network2 = deepcopy(network1)
    del network2["subnets"]["10.0.1.0"]["devices"][0]
    compare_result = compare_data(network1, network2, stack, visited)

    print(f"--- compare_data result, should be False: {compare_result}")
    if not compare_result:
        print()
        print(f"--- --- comparison failed at location: network1{''.join(stack)}:")

    print("\nCompare networks: loops in network --------------------")

    # Create loop in network, test to make sure we don't recurse through visited nodes
    network_looped_1 = create_network(num_devices=24, num_subnets=4)
    # pprint(network1)

    network_looped_1["subnets"]["10.0.1.0"]["devices"][10]["interfaces"][0]["link"] = network_looped_1
    network_looped_1["subnets"]["10.0.1.0"]["devices"][11]["interfaces"][0]["link"] = network_looped_1
    network_looped_2 = deepcopy(network_looped_1)

    stack.clear(); visited.clear()
    compare_result = compare_data(network_looped_1, network_looped_2, stack, visited)

    print(f"--- compare_data result, should be True: {compare_result}")
    if not compare_result:
        print(f"--- --- comparison failed at location: network1{''.join(stack)}")


if __name__ == "__main__":
    main()
