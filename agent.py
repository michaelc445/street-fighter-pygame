import torch
import random
import math
import numpy as np
from collections import deque

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.num_games=0
        self.epsilon=0  #randomness
        self.gamma = 0 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY) #pop left
        self.state_old = []
        self.final_move =[]
        self.reward=0
        self.done=False
        pass

    def get_state(self,  enemy_state,current_state,gamestate):
        current_char_nom=0
        current_char_wiz=0
        current_char_war=0
        opponent_char_nom=0
        opponent_char_wiz=0
        opponent_char_war=0
        map_mountain=0
        map_church=0
        map_cliffs=0
        print(gamestate)
        map = gamestate[0]
        current_char=gamestate[1]
        opponent_char=gamestate[2]
        current_char=0
        if gamestate[0] == "church":
            map_church=1
            map_mountain = 0
            map_cliffs = 0
        elif gamestate[0] == "cliffs":
            map_cliffs=1
            map_church = 0
            map_mountain = 0
        elif gamestate[0] == "mountain":
            map_mountain=1
            map_church = 0
            map_cliffs = 0
        #current char
        print(gamestate[2]," hey")
        if gamestate[2] == "nomad":
            current_char_nom = 1
            current_char_war = 0
            current_char_wiz = 0
        elif gamestate[2] =="wizard":
            current_char_wiz = 1
            current_char_nom = 0
            current_char_war = 0
        elif gamestate[2] == "Warrior":
            current_char_war = 1
            current_char_nom = 0
            current_char_wiz = 0

        # current char
        if gamestate[1] == "nomad":
            opponent_char_nom = 1
            opponent_char_war = 0
            opponent_char_wiz = 0
        elif gamestate[1] == "wizard":
            opponent_char_wiz = 1
            opponent_char_nom = 0
            opponent_char_war = 0
        elif gamestate[1] == "Warrior":
            opponent_char_war = 1
            opponent_char_nom = 0
            opponent_char_wiz = 0

        #opononent close:

        # d = √((x2 – x1)² + (y2 – y1)²)
        d = math.sqrt(((int(enemy_state[0])-int(current_state[0])))**2+((int(enemy_state[1])-int(current_state[1]))**2))
        print(d,"  hey ")
        if d < 200:
            opponent_close = 1
        else:
            opponent_close = False
        if d > 700:
            opponent_long = 1
        else:
            opponent_long = 0
        if enemy_state[0] < current_state[0]:
            opponent_left = 1
        else:
            opponent_left = 0
        if enemy_state[0] > current_state[0]:
            opponent_right = 1
        else:
            opponent_right = 0

        if enemy_state[1] > current_state[1]:
            opponent_up = 1
        else:
            opponent_up = 0

        if enemy_state[1] < current_state[1]:
            opponent_down = 1
        else:
            opponent_down = 0

        if enemy_state[4] == False:
            opponent_projectiles = 1
        else:
            opponent_projectiles = 0

        if enemy_state[5] == False:
            opponent_attack = 1
        else:
            opponent_attack = 0

        if enemy_state[6] == False:
            opponent_run = 1
        else:
            opponent_run = 0

        if current_state[2]<0:
            mov_l = 1
            mov_r = 0
        elif current_state[2]>0:
            mov_l = 0
            mov_r = 1
        else:
            mov_l = 0
            mov_r = 0
        if current_state[7] == True:
            jumping = 1
        else:
            jumping = 0
        if current_state[8] == True:
            block = 1
        else:
            block=0

        states = [
            current_char_nom,
            current_char_wiz,
            current_char_war,
            opponent_char_nom,
            opponent_char_wiz,
            opponent_char_war,
            map_mountain,
            map_church,
            map_cliffs,
            opponent_close,
            opponent_long,
            opponent_left,
            opponent_right,
            opponent_up,
            opponent_down,
            opponent_projectiles,
            opponent_run,
            opponent_attack,
            mov_l,mov_r,
            jumping,
            block,
        ]
        print(np.array(states, dtype=int))
        return np.array(states, dtype=int)
        pass

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
            states, actions, rewards, next_states, dones = zip(*mini_sample)
            self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self,state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
        pass

    def get_action(self, state):
        self.epsilon = 80 - self.num_games
        final_move = [0,0,0,0,0,0]#more moves
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0, 5)
            final_move[move] = 1

            move1 = random.randint(0, 5)
            final_move[move1] = 1
        #else:
            #state0 = torch.tensor(state, dtype=torch.float)
            #prediction= self.model.predict(state0)
            #move = torch.argmax(prediction)#.item()
            #final_move = move
        return final_move

    def train(self,fighter_1,fighter_2,state):
        print(fighter_1)
        #mainstate= game.return_state()
        fighter_1_s = fighter_1.return_state()
        fighter_2_s = fighter_2.return_state()
        gameState = state
        print(fighter_1_s,fighter_2_s,gameState)
        # get old state:
        self.state_old = self.get_state(fighter_1_s,fighter_2_s,gameState)

        # get move
        self.final_move = self.get_action(self.state_old)
        print(self.final_move)
        # perform move
        return self.final_move
        #reward, done ,score = game.playestep(final_move)

    def train_save(self,fighter_1,fighter_2,state):
        fighter_1_s = fighter_1.return_state()
        fighter_2_s = fighter_2.return_state()
        gameState = state
        state_new = self.get_state(fighter_1_s,fighter_2_s,gameState)
        self.train_short_memory(self.state_old, self.final_move, self.reward, state_new,self.done)

        self.remember(self.state_old, self.final_move, self.reward, self.state_new,self.done)

        '''
        if done:
            #train long memory plot results
            #game.reset()
            agent.num_games+=1
            agent.train_long_memory()

            if score>record:
                record = score
                #agent.model.save(0)
            print("game", agent.num_games,"score", score, "record ", record)
        #TODO: plot'''
        pass


