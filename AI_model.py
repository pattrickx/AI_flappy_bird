from argparse import Action
import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

class QNet(nn.Module):
    def __init__(self,input_size=2, output_size=1, hidden_size=20):
        super().__init__()

        self.fc = nn.Sequential(

            nn.Linear(in_features=input_size,out_features=hidden_size),
            nn.Tanh(),
            nn.Linear(in_features=hidden_size,out_features=hidden_size),
            nn.ReLU(),
            nn.Linear(in_features=hidden_size,out_features=output_size),
            )
        
    def forward(self, X):
        Y = self.fc(X)
        return Y
    
    def save_model(self,file_name="QNet_model.pth"):
        torch.save(self.state_dict(),file_name)
    
class QTrainer:
    def __init__(self,model,gamma=0.9,lr=0.001) -> None:
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(),lr=self.lr)
        self.criterion = nn.MSELoss() # Mean Squared Error
    
    def train_step(self, state,action, reward, next_state,done):

        # Process data
        state  = torch.tensor(state , dtype= torch.float)
        next_state = torch.tensor(next_state, dtype= torch.float)
        action = torch.tensor(action, dtype= torch.long)
        reward = torch.tensor(reward, dtype= torch.float)
        
        if len(state.shape)==1:
            state = torch.unsqueeze(state,0)
            next_state = torch.unsqueeze(next_state,0)
            action = torch.unsqueeze(action,0)
            reward = torch.unsqueeze(reward,0)
            done = (done,)

        # predict
        pred = self.model(state)
        # part2
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action).item()] = Q_new
        #part3

        self.optimizer.zero_grad()
        loss = self.criterion(target,pred)
        loss.backward()

        self.optimizer.step()

