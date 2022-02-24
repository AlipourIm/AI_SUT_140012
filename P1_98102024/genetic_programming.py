import random
import math
import copy # For copying objects... :)
import time

# Utility helper functions
def argsort(seq):
    # Substitute for numpy argsort function.
    return sorted(range(len(seq)), key=seq.__getitem__)
def get_min_of_a_list(values):
    index_min = min(range(len(values)), key=values.__getitem__)
    return index_min
def get_max_of_a_list(values):
    index_min = max(range(len(values)), key=values.__getitem__)
    return index_min
def return_closest_item_in_list(array, asked_number):
    # Returns closest item to an asked number in a python list
    item = min(array, key=lambda x:abs(x - asked_number))
    return array.index(item)
def random_number_between_0_and_1():
    return random.uniform(0, 1)
def get_length_of_tree(root, current_length):
    try:
        if root.right == None:
            return 0
        else:
            return 1 + get_length_of_tree(root.right, current_length)
    except:
        return 1
## End of utility helper functions

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

def preorder(node):
    if node:
        print(node.data, end = ' ')
        preorder(node.left)
        preorder(node.right)
def inorder(node):
    if node:
        print('(', end = '')
        inorder(node.left)
        print(node.data, end = '')
        inorder(node.right)
        print(')', end = '')
def postorder(node):
    if node:
        postorder(node.left)
        postorder(node.right)
        print(node.data, end = ' ')


def generate_random_number(starting_range, ending_range):
    return random.randint(starting_range,ending_range)

def generate_random_inner_node():
    probability = generate_random_number(1, 100)
    if probability <= 20:
        return '+'
    elif probability <= 40:
        return '-'
    elif probability <= 60:
        return '*'
    elif probability <= 80:
        return '/'
    else:
        return '^'

def generate_random_leaf_node():
    probability = generate_random_number(1, 100)
    if probability <= 70:
        return generate_random_number(0, 10)
    elif probability <= 90:
        return 'x'
    elif probability <= 95:
        return 'sin(x)'
    else:
        return 'cos(x)'

def create_initial_generation(size_of_generation, max_tree_length = 5):
    initial_generation = []

    for i in range(size_of_generation):
        length_of_tree = generate_random_number(1, max_tree_length)
        tree_leaves = []
        root = Node(generate_random_inner_node())
        tree_leaves.append(root)
        initial_generation.append(root)

        for _ in range(length_of_tree - 1):
            tmp_tree_leaves_copy = tree_leaves
            for i in range(len(tmp_tree_leaves_copy)):
                left_child = Node(generate_random_inner_node())
                right_child = Node(generate_random_inner_node())
                parent = tree_leaves.pop(0)
                parent.right = right_child
                parent.left = left_child
                tree_leaves.append(parent.right)
                tree_leaves.append(parent.left)

        tmp_tree_leaves_copy = tree_leaves
        for _ in range(len(tree_leaves)):
            left_child = Node(generate_random_leaf_node())
            right_child = Node(generate_random_leaf_node())
            parent = tree_leaves.pop(0)
            parent.right = right_child
            parent.left = left_child
    return initial_generation

def evaluate_expression_tree(root, x = 0):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        if root.data == 'x':
            data = x
        elif root.data == 'sin(x)':
            data = math.sin(x)
        elif root.data == 'cos(x)':
            data = math.cos(x)
        else:
            data = root.data
        return data
    left_sum = evaluate_expression_tree(root.left, x)
    right_sum = evaluate_expression_tree(root.right, x)
    if root.data == '+':
        try:
            return left_sum + right_sum
        except:
            return float('inf') # If overflow happens i return infinite...
    elif root.data == '-':
        try:
            return left_sum - right_sum
        except:
            return float('inf') # If overflow happens i return infinite...
    elif root.data == '*':
        try:
            return left_sum * right_sum
        except:
            return float('inf') # If overflow happens i return infinite...
    elif root.data == '^':
        if abs(right_sum) > 1000:
            return float('inf')
        try:
            return left_sum ** right_sum
        except:
            return float('inf') # This means that overflow has happened so I return infinite
    else:
        try:
            return left_sum / right_sum
        except:
            return float('inf') # Division by 0 kinda means the result is infinite, so I return infinite.
    # I still can't figure out how nan might happen :((((

def fittness_score(generation, x_values, expectation):
    fittness_values = []
    
    for i in range(len(generation)):
        difference = 0
        for j in x_values:
            try:
                difference += abs(evaluate_expression_tree(generation[i], j))
            except:
                difference = 0
        try:
            distance = abs(expectation[i] - difference)
            fittness_values.append(1000/distance)
        except:
            fittness_values.append(0)
    return fittness_values

def parent_selector(generation, fittness_values, next_generation_size = 100): # This ugly code tries to not select the same parents over and over again :(((((
    next_generation_parents = []
    next_gen_size = next_generation_size//2
    for i in range(next_gen_size):
        chosen_fittness = random_number_between_0_and_1()*1000
        parent_1_index = return_closest_item_in_list(fittness_values, chosen_fittness)
        parent_1 = generation[parent_1_index]
        chosen_fittness = random_number_between_0_and_1()*1000
        parent_2_index = return_closest_item_in_list(fittness_values, chosen_fittness)
        while parent_2_index == generation[parent_1_index]:
            chosen_fittness = random_number_between_0_and_1()*1000
            parent_2_index = return_closest_item_in_list(fittness_values, chosen_fittness)
        parent_2 = generation[parent_2_index]
        while (parent_1, parent_2) in next_generation_parents:
            chosen_fittness = random_number_between_0_and_1()*1000
            parent_1_index = return_closest_item_in_list(fittness_values, chosen_fittness)
            parent_1 = generation[parent_1_index]
            chosen_fittness = random_number_between_0_and_1()*1000
            parent_2_index = return_closest_item_in_list(fittness_values, chosen_fittness)
            while parent_2_index == generation[parent_1_index]:
                chosen_fittness = random_number_between_0_and_1()*1000
                parent_2_index = return_closest_item_in_list(fittness_values, chosen_fittness)
            parent_2 = generation[parent_2_index]
        next_generation_parents.append((parent_1, parent_2))
    return next_generation_parents
        
def make_next_generation(selected_parents, new_generation_rate = 0.7):
    new_generation = []
    for i in selected_parents:
        parent_1 = i[0]
        parent_2 = i[1]
        probability = random_number_between_0_and_1()
        if probability <= new_generation_rate:
            child_1, child_2 = cross_over(parent_1, parent_2)
            mutation_probability = random_number_between_0_and_1()
            if mutation_probability > 5:
                new_generation.append(child_1)
            else:
                mutated_child_1 = mutation(child_1)
                new_generation.append(mutated_child_1)
            mutation_probability = random_number_between_0_and_1()
            if mutation_probability > 5:
                new_generation.append(child_2)
            else:
                mutated_child_2 = mutation(child_2)
                new_generation.append(mutated_child_2)
        else:
            new_generation.append(parent_1)
            new_generation.append(parent_2)
    return new_generation

def cross_over(parent_1, parent_2):
    probability = generate_random_number(1, 100) # Better crossover?
    copy_of_parent_1 = copy.deepcopy(parent_1)
    copy_of_parent_2 = copy.deepcopy(parent_2)
    try:
        right_node_of_parent_1 = parent_1.right
        copy_of_parent_1.right = parent_2.right
        copy_of_parent_2.right = right_node_of_parent_1
    except:
        copy_of_parent_1 = copy_of_parent_1
        copy_of_parent_2 = copy_of_parent_2
    return copy_of_parent_1, copy_of_parent_2

def mutation(child_node):
    probability = generate_random_number(1, 100)    # Better mutation?
    node = child_node
    if probability <= 25:   # Cut the node
        node = Node(generate_random_leaf_node())
    elif probability <= 50: # Extend the node
        new_node = create_initial_generation(1, 4)
        node = new_node[0]
    else:   # Change nodes data
        how_far_to_go = generate_random_number(1, 5)
        while node.right != None and how_far_to_go != 0:
            if random_number_between_0_and_1() < 0.5:
                node = node.right
            elif node.left != None:
                node = node.left
        if node.right == None:
            node.data = generate_random_leaf_node()
        else:
            node.data = generate_random_inner_node()
    return node
            

def get_fittest_member(generation, x_values, y_values):
    fittness = fittness_score(generation, x_values, y_values)
    index_of_fittest_member = get_max_of_a_list(fittness)
    return generation[index_of_fittest_member], fittness[index_of_fittest_member]

def genetic_algorithm_driver(x_values, y_values, new_generation_rate = 0.7, generation_size = 100, expected_fittness = 1000, max_number_of_iterations = 1000):
    iteration = 0
    initial_generation = create_initial_generation(generation_size)
    fittest_node, fittness_of_fittest_node = get_fittest_member(initial_generation, x_values, y_values)
    generation = initial_generation
    fittness = fittness_score(generation, x_values, y_values)
    while fittness_of_fittest_node < expected_fittness and iteration != max_number_of_iterations:
        iteration += 1
        print("#### iteration = " + str(iteration))
        next_generation_parents = parent_selector(generation, fittness, generation_size)
        print("Selection of parents completed.")
        generation = make_next_generation(next_generation_parents, new_generation_rate)
        print("Creation of new generation completed.")
        fittest_node, fittness_of_fittest_node = get_fittest_member(generation, x_values, y_values)
        print("Fittest member of new generation selected and evaluated.")
        fittness = fittness_score(generation, x_values, y_values)
        print('Best tree after this iteration: ')
        inorder(fittest_node)
        print()
        print("Fittness of this tree: " + str(fittness_of_fittest_node))

    print("Algorithm execution finished, total # of iterations: " + str(iteration))
    print()
    return fittest_node


# Driver code:
start = time.time()

x_values = []
expectation = []

for i in range(1, 100):
    x_values.append(i)
    
    #expectation.append(math.cos(i) + 2*math.sin(i) + i**3 + 2*i + 12)
    expectation.append(2*i)
    #expectation.append(math.sin(i))
    #expectation.append(math.log(i))

"""
for i in range(100):
    x_values.append(i)
    y_value = generate_random_number(0, 1000)
    expectation.append(y_value)
    print((i, y_value), end = '')
    if i % 10 == 9:
        print()
"""
"""
range_1 = (0, 20)
range_2 = (21, 50)
range_3 = (51, 100)
for i in range_1:
    x_values.append(i)
    expectation.append(i*i)
for i in range_2:
    x_values.append(i)
    expectation.append(-i-10)
for i in range_3:
    x_values.append(i)
    expectation.append(0)
"""

formula = genetic_algorithm_driver(x_values, expectation, new_generation_rate = 0.7, generation_size = 100, expected_fittness = 10000, max_number_of_iterations = 100)
inorder(formula)
print()

end = time.time()
print(f"Runtime of the program is {end - start}")

# End of driver code

# My test codes(left this here just in case I need them for presentation day...)

"""
root = Node(10)

root.left = Node(34)
root.right = Node(89)
root.left.left = Node(45)
root.left.right = Node(50)
root.right.left = Node(45)
root.right.right = Node(50)

root2 = Node(10)

root2.left = Node(5)
root2.right = Node(4)
root2.left.left = Node(6)
root2.left.right = Node(1)
root2.right.left = Node(2)
root2.right.right = Node(3)
inorder(root)
print()
"""
"""
initial_generation = create_initial_generation(100)
x_values = []
expectation = []
for i in range(100):
    x_values.append(i)
    expectation.append(math.sin(i))

for i in initial_generation:
    fittness = fittness_score(initial_generation, x_values, expectation)
    print()
    print()
    print(x_values)
    print()
    print(expectation)
    print()
print(parent_selector(initial_generation, fittness, 100))


root = Node(10)

root.left = Node(34)
root.right = Node(89)
root.left.left = Node(45)
root.left.right = Node(50)
root.right.left = Node(45)
root.right.right = Node(50)

print(get_length_of_tree(root, 0))
"""

"""
x_values = []
expectation = []
for i in range(100):
    x_values.append(i)
    expectation.append(i)
gen = create_initial_generation(100)
print(gen)
print()
fittness = fittness_score(gen, x_values, expectation)
next_generation_parents = parent_selector(gen, fittness, 100)
print(next_generation_parents)
print()
generation = make_next_generation(next_generation_parents, 0.7)
print(generation)
print(type(generation[0]))
print(type(generation[1]))
print(type(generation[2]))
print(type(generation[3]))
print(type(generation[4]))
"""