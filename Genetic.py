import numpy as np
from AI_model import QNet
from random import random 
from Flap_bird import flap_bird
from Flap_bird import Bird
import torch
import time
from plot_train import plot
class specimen:
    def __init__(self,screen,screen_size) -> None:
        self.net = QNet(input_size=2, output_size=2, hidden_size=2)
        self.points = 0
        self.bird = Bird(screen,screen_size)
        self.is_alive = True
    
    def get_action(self,state):
        final_move = [0,0]
        state0 = torch.tensor(state,dtype= torch.float)
        prediction = self.net(state0)
        move = torch.argmax(prediction).item()
        # print(move)
        final_move[move] = 1 
        return final_move


class Genetic:
    def __init__(self,screen,population_size=1000) -> None:
        self.screen = screen
        self.screen_size = self.width, self.height =  600,600
        self.population_size = population_size
        self.population = self.generate_population()
        self.population_fitness=0
        self.elitism_count = 5
        self.crossover_rate = 0.97
        self.mutation_rate = 0.01
        self.n_games=0
        self.record = 0
        

    def generate_population(self):
        new_population =[]
        for n in range(self.population_size):
            new_population.append(specimen(self.screen,self.screen_size))
        return new_population

    def evaluate_population(self):
        self.population_fitness=0
        for indivuduo in self.population:
            self.population_fitness += indivuduo.points

    def select_parent(self):
        roulette_whell_position= random()*self.population_fitness
        spin_whell = 0
        for i in range(self.population_size):
            # print(f"{len(self.population)} : {self.population_size} : {i}")
            spin_whell += self.population[i].points
            if spin_whell >= roulette_whell_position:
                return self.population[i]
        return self.population[-1]

    def crossover_population(self):
        new_population = self.population[0:self.elitism_count]

        for i in range(self.population_size-self.elitism_count):
            parent1 = self.population[i]
            if self.crossover_rate >random():
                parent2 = self.select_parent()
                child = specimen(self.screen,self.screen_size)
                child.net.input = parent1.net.input

                child.net.output = parent2.net.output
                new_population.append(child)
            else: 
                new_population.append(parent1)
        self.population = new_population

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
        if self.record<self.population[0].points:
            self.record = self.population[0].points
            self.population[0].net.save_model()
        self.crossover_population()
        self.mutate_population()


def train():
    plot_caught_points=[]
    plot_scores=[]
    plot_mean_scores = []
    total_score = 0
    # agent = ai_agent()
    # agent = ai_agent("best.pth")
    game = flap_bird()
    genetic = Genetic(game.screen,100)

    genetic.generate_population()
    save_last = False
    while True:
        state = game.inputs_AI()
        game.game_draw_genetic()
        lives = 0
        # print(len(genetic.population))
        for individual in  genetic.population:
            if individual.is_alive:
                lives+=1
                action = individual.get_action(state)
                game.bird = individual.bird
                reward, done, score,caught_points = game.game_step_ai(action)
                individual.points += reward
                if done:
                    individual.is_alive=False
                else: 
                    game.bird.draw_bird()
        game.pipe.update_position()
        game.game_update_screen()
        if lives == 1 and not save_last:
            for individual in genetic.population:
                if individual.is_alive:
                    individual.net.save_model("last_alive.pth")
            save_last = True
        if lives == 0:
            save_last = False
            genetic.n_games+=1
            game.reset()
            genetic.evaluate_population()
            epoch_score = genetic.population_fitness/genetic.population_size
            genetic.generate_new_population()

            
            plot_scores.append(epoch_score)
            total_score += epoch_score
            mean_score = total_score/ genetic.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores,plot_mean_scores)
        # time.sleep(0.005)


if __name__ == "__main__":

    train()
    
    # genetic.generate_new_population()
    