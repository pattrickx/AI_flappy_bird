from matplotlib.pyplot import plot
import torch
import random
from collections import deque
import numpy as np
import time
from plot_train import plot
from Flap_bird import flap_bird
from AI_model import QNet, QTrainer

MAX_MEMORY = 100_000
BACH_SIZE = 1000
LR = 0.001

class ai_agent:
    def __init__(self,state_dict=None) -> None:
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 #discont rate
        self.memory = deque(maxlen=MAX_MEMORY) # pop left if memory take biger them MAX_MEMORY
        self.model = QNet(2,2,10)
        if state_dict:
            self.model.load_state_dict(torch.load(state_dict))
        self.trainer = QTrainer(self.model)

    def remember(self,state,action,reward,next_state,done):
        """ 
        this function create de Q table
        Args:
            state (Array): actual state of agent sensores
            action (int): action take by agent for the state
            reward (int): reward next them action
            next_state (Array): state next them action
            done (Bool): if the game and or not next them action
        """
        self.memory.append((state,action,reward,next_state,done))

    def train_long_memory(self):
        if len(self.memory)>BACH_SIZE:
            mini_sample =  random.sample(self.memory,BACH_SIZE)
        else:
            mini_sample = self.memory
            states,actions,rewards,next_states,dones = zip(*mini_sample)
            self.trainer.train_step(states,actions,rewards,next_states,dones)

    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)
    
    def get_action(self,state):
        self.epsilon = 100 - self.n_games
        final_move = [0,0]
        if random.randint(0,200)<self.epsilon:
            # print("random")
            move = random.uniform(0, 1)
            # print(move)
            final_move =[1,0]
            if move>0.97:
                final_move =[0,1] 
            # print(f"random {move} {final_move}")
        else:
            
            state0 = torch.tensor(state,dtype= torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            # print(move)
            final_move[move] = 1 
            # print(f"AI {prediction} {move} {final_move}")
        # print(final_move)
        return final_move
    
    def get_play_action(self,state):
        final_move = [0,0]
        state0 = torch.tensor(state,dtype= torch.float)
        prediction = self.model(state0)
        move = torch.argmax(prediction).item()
        # print(move)
        final_move[move] = 1 
        return final_move

def train():
    plot_caught_points=[]
    plot_scores=[]
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = ai_agent()
    game = flap_bird()
    while True:
        
        state_old = game.inputs_AI()

        final_move = agent.get_action(state_old)
        game.game_draw()
        reward, done, score,caught_points = game.game_step_ai(final_move)
        state_new = game.inputs_AI()

        agent.train_short_memory(state_old,final_move,reward,state_new,done)

        # remember
        agent.remember(state_old,final_move,reward,state_new,done)
        
        if done:
            game.reset()
            agent.n_games+=1
            agent.train_long_memory()
            if score > record:
                record = score
                agent.model.save_model()
            
            print(f"Game: {agent.n_games} Score: {score} Record: {record} caught points: {caught_points} ")

            plot_scores.append(score)
            total_score += score
            mean_score = total_score/ agent.n_games
            plot_mean_scores.append(mean_score)
            plot_caught_points.append(caught_points)
            plot(plot_scores,plot_mean_scores,plot_caught_points)
        # time.sleep(0.5)



if __name__ == "__main__":
    train()

