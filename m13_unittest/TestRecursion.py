import unittest
import inspect
from recursion.compare_networks import compare_data
from recursion.print_networks import traverse_and_print_flat
from m01_basics.util.create_utils import create_network
from copy import deepcopy
from random import randint
import io
from contextlib import redirect_stdout


def check_output(output, node, visited, num_checks):

    if type(node) not in {str, int, bool, float, tuple} and id(node) in visited:
        return True, num_checks
    visited.add(id(node))

    new_num_checks = num_checks

    if isinstance(node, dict):
        for key, value in node.items():
            success, new_num_checks = check_output(output, node[key], visited, new_num_checks)
            if not success: return False, new_num_checks

    elif isinstance(node, list) or isinstance(node, tuple):
        for index in range(0, len(node)):
            success, new_num_checks = check_output(output, node[index], visited, new_num_checks)
            if not success: return False, new_num_checks

    else:
        if node not in output: return False, new_num_checks
        else: return True, new_num_checks+1

    return True, new_num_checks


class TestRecursion(unittest.TestCase):

    def test_compare_data(self):

        print(f"\n\n===== {self.__class__.__name__}: {inspect.stack()[0][3]} =================================")

        stack = list()
        visited = set()
        network1 = create_network(num_devices=4, num_subnets=4)
        network2 = deepcopy(network1)

        print("\nCompare networks: should be identical --------------------")
        stack.clear()
        visited.clear()
        compare_result = compare_data(network1, network2, stack, visited)
        self.assertTrue(compare_result, f"!!! test failed at {''.join(stack)}")
        print(f"---> compare_data identical: successful")

        print("\nCompare networks: change name --------------------")
        stack.clear()
        visited.clear()
        network2["subnets"]["10.0.1.0"]["devices"][2]["name"] = "silly name"
        compare_result = compare_data(network1, network2, stack, visited)

        self.assertFalse(compare_result, f"!!! test failed at {''.join(stack)}")
        print(f"---> compare_data modified name: successful")

        print("\nCompare networks: remove item --------------------")
        stack.clear()
        visited.clear()
        network2 = deepcopy(network1)
        del network2["subnets"]["10.0.1.0"]["devices"][0]
        compare_result = compare_data(network1, network2, stack, visited)

        self.assertFalse(compare_result, f"!!! test failed at {''.join(stack)}")
        print(f"---> compare_data deleted device: successful")

        print("\nCompare networks: loops in network --------------------")

        # Create loop in network, test to make sure we don't recurse through visited nodes
        network_looped_1 = create_network(num_devices=24, num_subnets=4)
        # pprint(network1)

        network_looped_1["subnets"]["10.0.1.0"]["devices"][10]["interfaces"][0]["link"] = network_looped_1
        network_looped_1["subnets"]["10.0.1.0"]["devices"][11]["interfaces"][0]["link"] = network_looped_1
        network_looped_2 = deepcopy(network_looped_1)

        stack.clear()
        visited.clear()
        compare_result = compare_data(network_looped_1, network_looped_2, stack, visited)

        self.assertTrue(compare_result, f"!!! test failed at {''.join(stack)}")
        print(f"---> compare_data with loops: successful")

    def test_print_network(self):

        print(f"\n\n===== {self.__class__.__name__}: {inspect.stack()[0][3]} =================================")

        visited = set()
        network = create_network(num_devices=randint(12, 24), num_subnets=randint(4, 6))

        visited.clear()
        print("\nPrint network --------------------")
        with io.StringIO() as buf, redirect_stdout(buf):
            traverse_and_print_flat(network, 0, visited)
            output = buf.getvalue()

        success, num_checks = check_output(output, network, set(), 0)
        self.assertTrue(success, f"!!! output does not look correct: {output}")
        print(f"---> network print: successfully checked output for {num_checks} items")

        network["subnets"]["10.0.1.0"]["devices"][0]["interfaces"][0]["link"] = network
        network["subnets"]["10.0.1.0"]["devices"][1]["interfaces"][0]["link"] = network
        visited.clear()
        print("\nPrint network: with loops --------------------")
        with io.StringIO() as buf, redirect_stdout(buf):
            traverse_and_print_flat(network, 0, visited)
            output = buf.getvalue()

        success, num_checks = check_output(output, network, set(), 0)
        self.assertTrue(success, f"!!! output does not look correct: {output}")
        print(f"---> network print with loops: successfully checked output for {num_checks} items")


if __name__ == "__main__":
    unittest.main()
