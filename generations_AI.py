## Author: Taylor Olson

## Synopsis: Genetic algorithm program that uses a best fit algorithm and guesses the users
## initial input rgb color value, using selection, mutation, and newblood.

## Details: The program takes in a 24 bit string. This should be an RGB color.
## For example: 111111111111111111111111 would correspond to 255,255,255 rgb.
## The user then enters the amount of initial chromosomes in population.
## Then users enter desired generations of selection, mutation, newblood.
## The program will then run through the desired number of generations
## and return the rgb value of the best fit chromosome.

import math
import random
from operator import itemgetter

def main():
    
    color = input("24 bit string (or X to exit): ")
    while color != "X":
        while len(color) != 24:
            color = input("Please enter a 24 bit string: ")
        color_rgb = get_rgb(color)
        print("Your RGB value is: r=" + str(color_rgb[0]) + " g=" + str(color_rgb[1]) + " b=" + str(color_rgb[2]))

        pop_size = int(input("Number of chromosomes in population: "))
        selection = int(input("Number of chromosomes for selection (per generation): "))
        mutation = int(input("Number of chromosomes for mutation (per generation): "))
        newblood = int(input("Number of chromosomes for newblood (per generation): "))
        crossover = int(input("Number of crossover pairs (per generation): "))
        generations = int(input("Number of generations: "))

        chromosomes = generate_population(pop_size, color)

        for x in range(generations):
            chromosomes = generation(chromosomes, selection, mutation, newblood, crossover, color)
            if x != (generations - 1):
                print("The best fit chromosome of generation " + str(x+1) + " is " + chromosomes[0][0])
            else:
                print("Done...")
                print("The best fit chromosome after " + str(generations) + " generations is " + chromosomes[0][0])
                color_rgb = get_rgb(chromosomes[0][0])
                print("Which has an RGB value of: r=" + str(color_rgb[0]) + " g=" + str(color_rgb[1]) + " b=" + str(color_rgb[2]))
        color = input("24 bit string (or X to exit): ") 

def generate_population(pop_size, goal_color):
    chromosomes = []
    for x in range(pop_size):
        chromosome = ""
        for x in range(24):
            number = random.randint(0, 1)
            chromosome += str(number)
        chromosomes.append([chromosome, fitness_function(goal_color, chromosome)])
    return chromosomes

def get_rgb(byte):
    ## Takes in a 24 bit string
    ## Returns a list of rgb value
    byte = str(byte)
    red_dec = int(byte[0:8], 2)
    green_dec = int(byte[8:16], 2)
    blue_dec = int(byte[16:24], 2)

    return [red_dec, green_dec, blue_dec]
    
def fitness_function(byte1, byte2):
    rgb1 = get_rgb(byte1)
    rgb2 = get_rgb(byte2)

    return math.sqrt((rgb1[0] - rgb2[0])**2 + (rgb1[1] - rgb2[1])**2 +
                     (rgb1[2] - rgb2[2])**2)
    
def tournament_selection(chromosomes):
    ## Takes in list of lists containing 24 bit string and current fitness function score
    ## Returns index of greatest fitness function score between two random chosen chromosomes
    
    num1 = random.randint(0, len(chromosomes) - 1)
    num2 = random.randint(0, len(chromosomes) - 1)
    if num1 == num2:
        return num1
    elif chromosomes[num1][1] <= chromosomes[num2][1]:
        return num1
    elif chromosomes[num2][1] <= chromosomes[num1][1]:
        return num2

def generation(chromosomes, selection_val, mutation_val, newblood, crossover, color):
    for x in range(crossover):
        chromosomes = cross_over(chromosomes, color)

    for x in range(mutation_val):
        chromosomes = mutation(chromosomes, color)

    for x in range(selection_val):
        chromosomes = selection(chromosomes)

    for x in range(newblood):
        chromosomes = new_blood(chromosomes, color)
        
    chromosomes = sorted(chromosomes, key=itemgetter(1))
    return chromosomes
    
        

def cross_over(chromosomes, color):
    index1 = tournament_selection(chromosomes)
    chromosome1 = chromosomes[index1]
    index2 = tournament_selection(chromosomes)
    while index2 == index1:
        index2 = tournament_selection(chromosomes)
    chromosome2 = chromosomes[index2]
    
    crosspoint = random.randint(1, len(chromosome1[0])-2)
    new_chromosome1 = chromosome1[0][0: crosspoint] + chromosome2[0][crosspoint:]
    new_chromosome1 = [new_chromosome1, fitness_function(color, new_chromosome1)]
    new_chromosome2 = chromosome2[0][0:crosspoint] + chromosome1[0][crosspoint:]
    new_chromosome2 = [new_chromosome2, fitness_function(color, new_chromosome2)]
    chromosomes[index1] = new_chromosome1
    chromosomes[index2] = new_chromosome2

    return chromosomes

def mutation(chromosomes, color):
    index = tournament_selection(chromosomes)
    chromosome = chromosomes[index]
    point = random.randint(0, len(chromosome)-1)
    char_at_point = chromosome[0][point]
    if char_at_point == "0":
        character = "1"
    else:
        character = "0"
    new_chromosome = chromosome[0][0: point] + character + chromosome[0][point+1:]
    new_chromosome = [new_chromosome, fitness_function(color, new_chromosome)]
    chromosomes[index] = new_chromosome
    return chromosomes

def selection(chromosomes):
    index = tournament_selection(chromosomes)
    chromosome = chromosomes[index]
    chromosomes[index] = chromosome
    return chromosomes

def new_blood(chromosomes, color):
    index = tournament_selection(chromosomes)
    chromosome = chromosomes[index]
    new_chromosome = ""
    for x in range(0, len(chromosome[0])):
        if chromosome[0][x] == "0":
            new_chromosome += "1"
        elif chromosome[0][x] == "1":
            new_chromosome += "0"
    new_chromosome = [new_chromosome, fitness_function(color, new_chromosome)]
    chromosomes[index] = new_chromosome
    return chromosomes
       
       
main()


      
