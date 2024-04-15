import numpy as np
import copy
from collections import deque

# Function to print the current state of the puzzle
def print_state(state):
    for row in state:
        print(row)
    print()

# Function to generate all possible next states from the current state
def generate_next_states(state):
    next_states = []
    zero_row, zero_col = None, None
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                zero_row, zero_col = i, j
                break

    # Generate next states by moving the blank space (0) up, down, left, or right
    for drow, dcol in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_row, new_col = zero_row + drow, zero_col + dcol
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = copy.deepcopy(state)
            new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[zero_row][zero_col]
            next_states.append(new_state)
            next_states.sort(key=heuristic)
    return next_states

# Function to evaluate the heuristic value (number of tiles out of place) of a state
def heuristic(state):
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    misplaced = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal_state[i][j]:
                misplaced += 1
    return misplaced

# Hill Climbing Search algorithm with queue
def hill_climbing(initial_state):
    queue = deque([(heuristic(initial_state), [initial_state])])
    explored_states = set()

    while queue:
        current_cost, current_solution = queue.popleft()
        current_state = current_solution[-1]
        
        if current_cost == 0:
            return current_solution
        
        explored_states.add(str(current_state))

        next_states = generate_next_states(current_state)
        for next_state in next_states:
            if str(next_state) not in explored_states:
                new_solution = current_solution + [next_state]
                queue.append((heuristic(next_state), new_solution))
                explored_states.add(str(next_state))
    
    return None

# Main function
def main():
    initial_state = [[1, 6, 3], [4, 2, 0], [8, 5, 7]]

    final_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    print("Initial State:")
    print_state(initial_state)

    print("Final State:")
    print_state(final_state)

    print("Solving using Hill Climbing Search with Queue:")
    solution = hill_climbing(initial_state)
    if solution:
        print("Solution found:")
        for state in solution:
            print_state(state)
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
