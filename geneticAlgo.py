"""
The file that contains the framework for the genetic algorithm
for optimizing this game of tetris
"""
import random
import pprint
import sys
import csv
from tetris import *







def generate_initial_heuristic_vals(h_size, pop_size=10):
    h_vals_list = []
    for i in range(pop_size):
        h_vals_list.append([])
        for h_val in range(h_size):
            h_vals_list[i].append(random.randint(-100,100))
    
    return h_vals_list

def run_generation(h_lists, pop_size=10):
    """
    runs a generation of agents
    and records the results to a .csv file
    """
    h_val_lists = []
    turn_counts = []
    for population in range(pop_size):
        #print('        POP #: {}'.format(population))
        h_vals = h_lists[population]

        sim_count = 1
        game = TetrisBoard(h_vals)
        turn_count = 0
        for i in range(sim_count):
            turn_count += game.run_simulation()
        if sim_count != 1:
            turn_count = turn_count / sim_count

        h_val_lists.append(h_vals)
        turn_counts.append(turn_count)
    
    return turn_counts, h_val_lists

def display_gen_details(gen_info, gen_count):
    turn_counts = gen_info[0]
    h_val_lists = gen_info[1]

    turn_count_avg = 0
    for count in turn_counts:
        turn_count_avg += count 
    
    turn_count_avg = turn_count_avg / len(turn_counts)
    #print('AVERAGE TURN COUNT: {}'.format(turn_count_avg))
    max_turn_count = max(turn_counts)
    max_hval = h_val_lists[turn_counts.index(max_turn_count)]
    #print('MAX TURN COUNT: {}'.format(max_turn_count))
    #print('H VALS: {}'.format(max_hval))


    print("GEN: {} | AVG TURN COUNT: {} | MAX TURN COUNT: {}".format(gen_count, turn_count_avg, max_turn_count))
    return [gen_count, turn_count_avg, max_turn_count]
    

def make_next_gen(prev_gen_info):
    """
    creates a population of the same size with features
    from the top half the current generation
    returns a list of h_val_lists
    """
    gen_size = len(prev_gen_info[0])
    top_half = int(gen_size/2)
    if top_half % 2 != 0:
        #ensure that gen_size is even
        top_half += 1
    
    turn_counts = prev_gen_info[0]
    h_vals = prev_gen_info[1]
    #print(turn_counts)
    gen_parents = []
    
    #print(top_half)
    for i in range(top_half):
        max_turn_count = max(turn_counts)
        index = turn_counts.index(max_turn_count)
        turn_counts.pop(index)
        gen_parents.append(h_vals[index])
        h_vals.pop(index)
    
    #print('CURRENT PARENTS _--------------')
    #pprint(gen_parents)
    h_size = len(gen_parents[0])
    new_gen_hvals = []
    for gen_index in range(gen_size):
        new_gen_hvals.append(create_child(gen_parents))

    #print('new gen ---------------')
    #pprint(new_gen_hvals)
    return new_gen_hvals  

def create_child(parents):
    """
    creates a child of the parents 
    using randomly selected attributes from them
    """
    
    child = []
    h_size = len(parents[0])

    for i in range(h_size):
        mutation_chance = random.randint(0,1000)
        parent_choices = []
        for parent in parents:
            parent_choices.append(parent[i])
        if mutation_chance == 3:
            print("MUTATION")
            child.append(random.randint(-500,500))
        else:
            child.append(random.choice(parent_choices))

    return child

    

def main():
    h_size = 5
    max_turns = []
    max_h_vals = []
    pop_size = int(sys.argv[1])
    gen_size = int(sys.argv[2])
    csvFile = open('gen_data[{}][{}].csv'.format(pop_size,gen_size), 'w')
    dataWriter = csv.writer(csvFile)
    dataWriter.writerow(['GEN #', 'TURN AVG', 'MAX TURN'])

    #take care of the initial generation
    initial_h = generate_initial_heuristic_vals(h_size, pop_size)
    gen = run_generation(initial_h, pop_size)
    dataWriter.writerow(display_gen_details(gen, 0))
    #pprint(gen)
    gen_size = int(sys.argv[2])
    for i in range(gen_size - 1):
        new_hvals = make_next_gen(gen)
        gen = run_generation(new_hvals, pop_size)
        max_turn = max(gen[0])
        max_turns.append(max_turn)
        max_h_vals.append(gen[1][gen[0].index(max_turn)])
        #write the data
        dataWriter.writerow(display_gen_details(gen, i + 1))
        #pprint(gen)
        #time.sleep(5)
    
    max_index = max_turns.index(max(max_turns))
    max_h = max_h_vals[max_index]
    print('max_h: {}'.format(max_h))
    print('max turn: {}'.format(max_turns[max_index]))
    final_game = TetrisBoard(max_h, height=11)
    final_game.run_simulation(print_progress=True)
    print('---------------')
    
if __name__ == '__main__':
    main()