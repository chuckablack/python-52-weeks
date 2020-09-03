i = 1
print(f"i: {i}, id(i): {id(i)}")
i = i + 1
print(f"i: {i}, id(i): {id(i)}")
j = i
print(f"\ni: {i}, id(i): {id(i)}")
print(f"j: {j}, id(j): {id(j)}")
i = i + 1
print(f"\ni: {i}, id(i): {id(i)}")
print(f"j: {j}, id(j): {id(j)}")

print("\n\n")

l1 = [1]
print(f"l1: {l1}, id(l1): {id(l1)}")
l1.append(2)
print(f"l1: {l1}, id(l1): {id(l1)}")
l2 = l1
print(f"\nl1: {l1}, id(l1): {id(l1)}")
print(f"l2: {l2}, id(l2): {id(l2)}")
l1.append(3)
print(f"\nl1: {l1}, id(l1): {id(l1)}")
print(f"l2: {l2}, id(l2): {id(l2)}")

