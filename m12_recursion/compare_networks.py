from m01_basics.util.create_utils import create_network
from copy import deepcopy
import inspect

current_data1 = current_data2 = None

def compare_data(data1, data2):

    # print(f"data1: {data1}")
    # print(f"data2: {data2}")

    global current_data1, current_data2
    current_data1 = data1
    current_data2 = data2

    if isinstance(data1, dict):
        if not isinstance(data2, dict): return False
        for key, value in data1.items():
            if key not in data2: return False
            stack.append("['"+key+"']")
            if not compare_data(data1[key], data2[key]): return False
            stack.pop()
        return True

    elif isinstance(data1, list) or isinstance(data1, tuple):
        if type(data1) != type(data2): return False
        for index, _ in enumerate(data1):
            stack.append("["+str(index)+"]")
            if not compare_data(data1[index], data2[index]): return False
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


network1 = create_network(num_devices=4, num_subnets=4)
network2 = deepcopy(network1)

stack = list()
print(compare_data(network1, network2))
print(f"final stack: network1{''.join(stack)}")

stack = list()
network2["subnets"]["10.0.1.0"]["devices"][2]["name"] = "this is a silly and not real name"
print(compare_data(network1, network2))
print(f"data1: network1{''.join(stack)}: {current_data1}")
print(f"data2: network1{''.join(stack)}: {current_data2}")
