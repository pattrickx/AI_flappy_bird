import numpy as np
from AI_model import QNet
from random import random 
class specimen:
    def __init__(self) -> None:
        self.net = QNet(input_size=2, output_size=2, hidden_size=2)
        self.points = random()*100

class Genetic:
    def __init__(self,population_size=1000) -> None:
        self.population_size = population_size
        self.population = self.generate_population()
        self.population_fitness=0
        self.elitism_count = 50
        self.crossover_rate = 0.97
        self.mutation_rate = 0.01
        

    def generate_population(self):
        new_population =[]
        for n in range(self.population_size):
            new_population.append(specimen())
        return new_population

    def evaluate_population(self):
        self.population_fitness=0
        for indivuduo in self.population:
            self.population_fitness += indivuduo.points

    def select_parent(self):
        roulette_whell_position= random()*self.population_fitness
        spin_whell = 0
        for i in range(self.population_size):
            spin_whell += self.population[i].points
            if spin_whell >= roulette_whell_position:
                return self.population[i]
        return self.population[-1]

    def crossover_population(self):
        self.population = self.population[0:self.elitism_count]

        for i in range(self.population_size-self.elitism_count):
            parent1 = self.population[i]
            if self.crossover_rate >random():
                parent2 = self.select_parent()
                child = specimen()
                child.net.input = parent1.net.input
                child.net.output = parent2.net.output
                self.population.append(child)
            else: 
                self.population.append(parent1)

    def mutate_population(self):
        random_population = self.generate_population()
        for indivuduo,random_individuo in zip(self.population,random_population):
            if self.mutation_rate>random():
                if random()>0.5:
                    indivuduo.net.input = random_individuo.net.input
                else:
                    indivuduo.net.output = random_individuo.net.output
        

    def generate_new_population(self):
        self.population.sort(key = lambda s: s.points, reverse=True)
        self.crossover_population()
        self.mutate_population()


    


if __name__ == "__main__":

    genetic = Genetic(100)
    genetic.generate_population()
    genetic.generate_new_population()