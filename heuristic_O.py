# %%
import numpy as np
import time
from game import ConsoleGame
import random
# %%


class stepPlay:
    def __init__(self, xy, notlist=None):
        self.xy = xy
        if notlist == None:
            self.notlist = []
        else:
            self.notlist = notlist
        self.Map = None


# %%
def HFunction(Prob, L, game, r_c):
    rx = len(game.column_counts)
    ry = len(game.row_counts)
    x = 0

    while(x < rx):
        s = []
        while len(s) < sumS(L[x], rx):
            a = []
            for i in L[x]:
                a.append(i)
                a.append(0)
            a.pop(-1)
            b = [0 for i in range(rx-sum(L[x]))]
            c = [x.pop(0) for x in random.sample(
                [a]*len(a) + [b]*len(b), len(a)+len(b))]
            if c not in s:
                s.append(c)

        for i in range(len(s)):
            for j in range(rx):
                if s[i][j] > 1:
                    p = s[i].pop(j)
                    for k in range(p):
                        s[i].insert(j, 1)

        si = []
        r = []
        for j in range(len(s)):
            if r_c:
                r = np.array(game.map[:, x])
            else:
                r = np.array(game.map[x])
            a = np.where(r == 1)[0]
            t = True
            for k in a:
                if s[j][k] == 0:
                    t = False

            if t == True:
                si.append(s[j])

        s = si.copy()
        for i in range(ry):
            e = 0
            for j in range(len(s)):
                if s[j][i] == 1:
                    e = e+1
            if len(s) == 0:
                Prob[x][i] = 0
            else:
                Prob[x][i] = (e/len(s))

        # print(s)
        x = x + 1
    return Prob


def minProb(prob, game, list):
    y = len(prob)
    x = len(prob[0])
    min_prob = 1

    for i in range(y):
        for j in range(x):
            if game.map[i][j] == False:
                if (j, i) not in list:
                    if prob[i][j] < min_prob:
                        min_prob = prob[i][j]

    for i in range(y):
        for j in range(x):
            if game.map[i][j] == False:
                if prob[i][j] == min_prob:
                    if (j, i) not in list:
                        #print(f'Min: {min_prob}')
                        return (j, i)


def sumS(L, r):
    s = 0
    if len(L) > 1:
        t = r-L[0]-1
        for i in range(t+1):
            s = s + sumS(L[1:], i)
    elif len(L) == 1:
        t = r-L[0]+1
        if t > 0:
            s = s + t
    return s


def sum(L):
    a = 0
    for i in L:
        a = a + i + 1
    return a-1


def getProb(game: ConsoleGame):
    ry, rx = game.shape 

    Probx = [[0 for i in range(rx)] for j in range(ry)]
    Proby = [[0 for i in range(rx)] for j in range(ry)]
    Lx = game.column_counts
    Ly = game.row_counts
    Probx = HFunction(Probx, Lx, game, True)
    Proby = HFunction(Proby, Ly, game, False)

    Probxy = [[0 for i in range(rx)] for j in range(ry)]
    for i in range(rx):
        for j in range(ry):
            Probxy[i][j] = Probx[j][i] * Proby[i][j]

    return Probxy