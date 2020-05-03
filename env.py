import random
import numpy as np
from Board import *
from itertools import permutations
import pickle
import matplotlib.pyplot as plt

# Parameters
Training = 50000
epsilon = 0.9
DISCOUNT = 0.95
EPS_DECAY = 0.9998
WIN_REWARD = 100
LOSE_REWARD = -200
TIE_REWARD = 50
CHANCE_PENALTY = -1
SHOW_EVERY = 100
LEARNING_RATE = 0.1
with open('QTable.pickle', 'rb') as handle:
    q_table = pickle.load(handle)
rewards = [] # keeps a track of the rewards over different training examples

if q_table is None:
    q_table = {}
    strings = ['X--------', 'XO-------', 'XXO------', 'XXOO-----', 'XXXOO----', 'XXXOOO---', 'XXXXOOO--', 'XXXXOOOO-', 'XXXXXOOOO']
    states = ['---------']
    for i in strings:
        p = permutations(i)
        for j in list(p):
            stringA = ''.join(j)
            if stringA not in states:
                states.append(stringA)
    print('Number of states:',len(states))
    values = []
    for i in states:
        value = list(np.random.uniform(-5,0,size=9))
        for index,j in enumerate(i):
            if j == 'X' or j == 'O':
                value[index] = None
        values.append(value)

    for i in range(len(states)):
        q_table[states[i]] = values[i]


    with open('QTable.pickle', 'wb') as handle:
        pickle.dump(q_table, handle, protocol=pickle.HIGHEST_PROTOCOL)


for episode in range(Training):
    reward = 0
    episode_reward = 0
    game = GameBoard()
    over = False
    while game.openPositions() != []: # Game has tied
        #print(game.openPositions())
        curState = game.currentState()
        positions = game.openPositions()
        if np.random.random() > epsilon:
            maxQ = -999
            for index, qValue in enumerate(q_table[curState]):
                if qValue == None:
                    continue
                if qValue > maxQ:
                    maxQ = qValue
                    moveMain = index + 1
        else:
            moveMain = random.choice(positions)
            maxQ = q_table[curState][moveMain - 1]
        game.chance(moveMain)
        #print('X:', moveMain, end=' ')
        reward += CHANCE_PENALTY
        if game.win() == True:
            reward += WIN_REWARD
            over = True
        elif len(game.openPositions()) == 0:
            reward += TIE_REWARD
        else:
            game.playerChange()
            positions = game.openPositions()
            move = random.choice(positions)
            game.chance(move)
            #print('Y:',move)
            reward += CHANCE_PENALTY
            newState = game.currentState()
            if game.win() == True:
                reward += LOSE_REWARD
                over = True
            elif game.openPositions == []:
                reward += TIE_REWARD
            else:
                game.playerChange()

        if reward != WIN_REWARD and reward != LOSE_REWARD and reward != TIE_REWARD:
            maxFQ = -999
            for i in q_table[newState]:
                if i == None:
                    continue
                if i > maxFQ:
                    maxFQ = i

        if reward == WIN_REWARD + CHANCE_PENALTY:
            newQ = WIN_REWARD
        elif reward == TIE_REWARD + CHANCE_PENALTY:
            newQ = TIE_REWARD
        else:
            newQ = (1 - LEARNING_RATE) * maxQ + LEARNING_RATE * (reward + DISCOUNT * maxFQ)
        q_table[curState][moveMain-1] = newQ

        episode_reward += reward
        if over:
            break

    rewards.append(episode_reward)
    if episode % SHOW_EVERY == 0:
        print('EPISODE NUMBER:', episode, 'REWARD:', reward)
        game.printState()
    epsilon *= EPS_DECAY

moving_avg = np.convolve(rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')
plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel('Rewards every 100')
plt.xlabel("Episode #")
plt.show()

    # UPDATION OF THE Q VALUE

user = 'Y'
while user == 'Y':
    game = GameBoard()
    print('PLAY:')
    game.printState()
    while game.openPositions() != []:
        curState = game.currentState()
        maxQ = -999
        for index, qValue in enumerate(q_table[curState]):
            if qValue == None:
                continue
            if qValue > maxQ:
                maxQ = qValue
                move = index + 1
        game.chance(move)
        game.printState()
        if game.win():
            print("AGENT WINS")
            break
        elif game.openPositions() == []:
            print("TIE")
            break
        else:
            game.playerChange()
            move = int(input('Enter 1-9: (You are X)'))
            positions = game.openPositions()
            while move not in positions:
                move = int(input('Enter 1-9: (You are X)'))
            game.chance(move)
            game.printState()
            if game.win():
                print('USER WINS')
                break
            elif game.openPositions() == []:
                print('TIE')
                break
            else:
                game.playerChange()
    user = input('Y to play again:')




