from AI_model import QNet
from Flap_bird import flap_bird
import torch
import time

net = QNet(input_size=2, output_size=2, hidden_size=2)
net.load_state_dict(torch.load("last_alive.pth"))
net.eval()
game = flap_bird()
def get_action(net,state):
    final_move = [0,0]
    state0 = torch.tensor(state,dtype= torch.float)
    prediction = net(state0)
    move = torch.argmax(prediction).item()
    # print(move)
    final_move[move] = 1 
    return final_move
while True:
    game.game_draw()
    state = game.inputs_AI()
    final_move = get_action(net,state)
    
    
    _ , done, _, _ = game.game_step_ai(final_move)
    game.pipe.update_position()
    game.game_update_screen()
    if done: 
        game.reset()
    time.sleep(0.001)