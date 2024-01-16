"""

Consider a thief who has a knapsack that can carry a maximum weight of `W = 50` units. He breaks into a house and finds `n = 5` items. Each item `i` has a certain weight `w_i` and a certain value `v_i`. The weights and values of the items are as follows:

```plaintext
Item:   1   2   3   4   5
Weight: 10  20  30  40  50
Value:  60  100 120 160 200
```

The thief wants to maximize the total value of the items he steals, but he can't exceed the maximum weight of his knapsack. Which items should he take?

"""
import random
import numpy as np


class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value


class Knapsack:
    def __init__(self, state_bit_array, cumulative_weight = 0):
        self.state_bit_array = state_bit_array

        self.cumulative_weight = cumulative_weight


def create_items(items_tuples):
    possible_items = []
    for i in items_tuples:
        item = Item(i[0], i[1])
        possible_items.append(item)
    return possible_items


def generate_initial_problem(items_to_consider, capacity):
    knapsack = Knapsack(np.zeros(len(items_to_consider)))
    while True:
        knapsack.state_bit_array = np.zeros(len(items_to_consider))
        knapsack.cumulative_weight = 0
        for index, value in enumerate(knapsack.state_bit_array):
            random_number = random.randint(0, 1)
            if random_number == 1 and knapsack.cumulative_weight + items_to_consider[index].weight <= capacity:
                knapsack.cumulative_weight += items_to_consider[index].weight
                knapsack.state_bit_array[index] = random_number

        if knapsack.cumulative_weight <= 50:
            return knapsack.state_bit_array


def generate_successors(state_bits, capacity, items):
    untrimmed_successors = []
    for i in range(len(state_bits)):
        copy_state_bits = state_bits.copy()
        if copy_state_bits[i] == 1:
            copy_state_bits[i] = 0
        else:
            copy_state_bits[i] = 1
        untrimmed_successors.append(copy_state_bits)
    return [successor for successor in untrimmed_successors if within_constraint(successor, capacity, items)]


def within_constraint(state, capacity, items):
    return calculate_weight(state, items) <= capacity


def calculate_weight(state, items):
    cumulative_weight = 0
    for index, value in enumerate(state):
        if value == 1:
            cumulative_weight += items[index].weight
    return cumulative_weight


def calculate_value(state, items):
    cumulative_value = 0
    for index, value in enumerate(state):
        if value == 1:
            cumulative_value += items[index].value
    return cumulative_value


def get_maximum_valued_successor(possibilities, items):
    max_successor_index = 0
    max_value = 0
    for index, value in enumerate(possibilities):
        if calculate_value(value, items) > max_value:
            max_successor_index = index
            max_value = calculate_value(value, items)
    return possibilities[max_successor_index]


def hill_climbing(items_to_consider, capacity):
    current_problem = generate_initial_problem(items_to_consider, capacity)
    while True:
        successors = generate_successors(current_problem, capacity, items_to_consider)
        neighbour = get_maximum_valued_successor(successors, items_to_consider)
        if calculate_value(neighbour, items_to_consider) <= calculate_value(current_problem, items_to_consider):
            for index, value in enumerate(current_problem):
                if value == 1:
                    print(f"Item: {index + 1}")
                    print(f"Weight: {items_to_consider[index].weight}")
                    print(f"Value: {items_to_consider[index].value}")
                    print()
            print(f"Cumulative value of items: {calculate_value(current_problem, items_to_consider)}")
            break
        current_problem = neighbour


first_items = create_items([
    (10, 60),
    (20, 100),
    (30, 120),
    (40, 160),
    (50, 200)
])
second_items = create_items([(7, 42), (14, 84), (21, 126), (28, 168), (35, 210)]
)
third_items = create_items([(5, 30), (10, 60), (15, 90), (20, 100), (25, 150)])

hill_climbing(first_items, 50)
print()
hill_climbing(second_items, 70)
print()
hill_climbing(third_items, 40)
