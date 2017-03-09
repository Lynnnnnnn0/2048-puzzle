from random import randint
from BaseAI_3 import BaseAI
import time
import numpy as np

class PlayerAI(BaseAI):
    """docstring for PlayerAI"""
    

    def _init_(self):
        self.direction = -1


    def minimax(self, grid, ismax, depth, timelimit):
        if time.clock() > timelimit:
            return [self.evalfn(grid), -1]
        if depth == 0:
            return [self.evalfn(grid), -1]
        if grid.canMove() == False:
           return [self.evalfn(grid), -1]
        
        if ismax:
            [minmaxUtility, minimaxMove] = [-float('inf'), -1]
            moves = grid.getAvailableMoves()
            #if len(grid.getAvailableCells()) > 8:
            #    [minmaxUtility, minimaxMove] = [-float('inf'), -1]
            #    for i in moves:
            #        gridCopy = grid.clone()
            #        gridCopy.move(i)
            #        if self.evalfn(gridCopy) > minmaxUtility:
            #            [minmaxUtility, minimaxMove] = [self.evalfn(gridCopy), i]
            #    return [minmaxUtility, minimaxMove]
            for i in moves:
                gridCopy = grid.clone()
                gridCopy.move(i)
                [new_utility, new_move] = self.minimax(gridCopy, False, depth-1, timelimit)
                if new_utility > minmaxUtility:
                    [minmaxUtility, minimaxMove] = [new_utility, i]
        else:
            [minmaxUtility, minimaxMove] = [float('inf'), -1]
            cells = grid.getAvailableCells()
            if cells == []:
                return [minmaxUtility, minimaxMove]
            for i in cells:
                gridCopy2 = grid.clone()
                gridCopy2.insertTile(i,2)
                [new_utility, new_move] = self.minimax(gridCopy2, True, depth-1, timelimit)
                if new_utility < minmaxUtility:
                    [minmaxUtility, minimaxMove] = [new_utility, -1]
                gridCopy4 = grid.clone()
                gridCopy4.insertTile(i,4)
                [new_utility, new_move] = self.minimax(gridCopy4, True, depth-1, timelimit)
                if new_utility < minmaxUtility:
                    [minmaxUtility, minimaxMove] = [new_utility, -1]
        return [minmaxUtility, minimaxMove]
                
    

    def alphabeta(self, grid, ismax, alpha, beta, depth, timelimit):
        if time.clock() > timelimit:
            return [self.evalfn(grid), -1]
        if depth == 0:
            return [self.evalfn(grid), -1]
        if grid.canMove() == False:
           return [self.evalfn(grid), -1]
        if ismax:
            # at max level, initialize alpha
            [minmaxUtility, minimaxMove] = [-float('inf'), -1]
            moves = grid.getAvailableMoves()
            for i in moves:
                gridCopy = grid.clone()
                gridCopy.move(i)
                [new_utility, new_move] = self.alphabeta(gridCopy, False, alpha, beta, depth-1, timelimit)
                if new_utility > minmaxUtility:
                    [minmaxUtility, minimaxMove] = [new_utility, i]
                # pruning
                if minmaxUtility >= beta:
                    break
                # update alpha
                if minmaxUtility > alpha:
                    alpha = minmaxUtility
        else:
            # at min level, initialize beta
            [minmaxUtility, minimaxMove] = [float('inf'), -1]
            cells = grid.getAvailableCells()
            if cells == []:
                return [minmaxUtility, minimaxMove]
            for i in cells:
                gridCopy2 = grid.clone()
                gridCopy2.insertTile(i,2)
                [new_utility, new_move] = self.alphabeta(gridCopy2, True, alpha, beta, depth-1, timelimit)
                if new_utility < minmaxUtility:
                    [minmaxUtility, minimaxMove] = [new_utility, -1]
                if minmaxUtility <= alpha:
                    break
                gridCopy4 = grid.clone()
                gridCopy4.insertTile(i,4)
                [new_utility, new_move] = self.alphabeta(gridCopy4, True, alpha, beta, depth-1, timelimit)
                if new_utility < minmaxUtility:
                    [minmaxUtility, minimaxMove] = [new_utility, -1]
                if minmaxUtility <= alpha:
                    break
                if minmaxUtility < beta:
                    beta = minmaxUtility
        return [minmaxUtility, minimaxMove]

    def ids(self, grid, timelimit):
        [maxUtility, maxMove] = [-float('inf'), -1]
        depthlimit = 2
        while time.clock()<timelimit:
            [utility, move] = self.alphabeta(grid, True, -float('inf'), float('inf'), depthlimit, timelimit)
            if move == -1:
                print("break")
                break
            if utility > maxUtility:
                [maxUtility, maxMove] = [utility, move]
            depthlimit += 1
        return [maxUtility, maxMove]


    def heuristic1(self, grid):
        # grant bonuses for open squres
        cells = grid.getAvailableCells()
        return len(cells)/16

    def heuristic2(self, grid):
        bonus = 0
        for x in range(grid.size):
            for y in range(grid.size):
                # if the edge value large than 3/4 of the max tile, grant a bonus
                if (x == 0 or x == grid.size-1 or y == 0 or y == grid.size-1) and grid.map[x][y] > grid.getMaxTile()*0.75:
                    bonus += 1
        return bonus/16

    # Smoothness: count the number of equal neighbor tiles
    def heuristic4(self, grid):
        bonus = 0
        for x in range(grid.size):
            for y in range(grid.size):
                if x == 0 and y == 0:
                    if grid.map[x][y] == grid.map[x][y+1] or grid.map[x][y] == grid.map[x+1][y]:
                        bonus += 1
                elif x == 0 and y == grid.size-1:
                    if grid.map[x][y] == grid.map[x][y-1] or grid.map[x][y] == grid.map[x+1][y]:
                        bonus += 1
                elif x == grid.size-1 and y == 0:
                    if grid.map[x][y] == grid.map[x-1][y] or grid.map[x][y] == grid.map[x][y+1]:
                        bonus += 1
                elif x == grid.size-1 and y == grid.size-1:
                    if grid.map[x][y] == grid.map[x-1][y] or grid.map[x][y] == grid.map[x][y-1]:
                        bonus += 1
                elif x == 0:
                    if grid.map[x][y] == grid.map[x][y-1] or grid.map[x][y] == grid.map[x][y+1] or grid.map[x][y] == grid.map[x+1][y]:
                        bonus += 1
                elif x == grid.size-1:
                    if grid.map[x][y] == grid.map[x][y-1] or grid.map[x][y] == grid.map[x][y+1] or grid.map[x][y] == grid.map[x-1][y]:
                        bonus += 1
                elif y == 0:
                    if grid.map[x][y] == grid.map[x][y+1] or grid.map[x][y] == grid.map[x-1][y] or grid.map[x][y] == grid.map[x+1][y]:
                        bonus += 1
                elif y == grid.size-1:
                    if grid.map[x][y] == grid.map[x][y-1] or grid.map[x][y] == grid.map[x-1][y] or grid.map[x][y] == grid.map[x+1][y]:
                        bonus += 1
                else:
                    if grid.map[x][y] == grid.map[x][y-1] or grid.map[x][y] == grid.map[x][y+1] or grid.map[x][y] == grid.map[x-1][y] or grid.map[x][y] == grid.map[x+1][y]:
                        bonus += 1
        return bonus/16


    def heuristic5(self, grid):
        bonus = 0
        count = 0
        maxTile = grid.getMaxTile()
        if grid.map[0][0] == maxTile:  
            for x in range(grid.size):
                for y in range(grid.size):
                    if y == 3 or x == 3:
                        break
                    else:
                        count += 1
                    if grid.map[x][y] >= grid.map[x][y+1] and grid.map[x][y] >= grid.map[x+1][y]:
                        bonus += 1
            if bonus == count and grid.map[3][3] <= grid.map[2][3] and grid.map[3][3] <= grid.map[3][2]:
                bonus += maxTile      
        elif grid.map[0][3] == maxTile:
            for x in range(grid.size):
                for y in range(grid.size):
                    if y == 0 or x == 3:
                        break
                    else:
                        count += 1
                    if grid.map[x][y] >= grid.map[x][y-1] and grid.map[x][y] >= grid.map[x+1][y]:
                        bonus += 1
            if bonus == count and grid.map[3][0] <= grid.map[2][0] and grid.map[3][0] <= grid.map[3][1]:
                bonus += maxTile 
        elif grid.map[3][0] == maxTile:
            for x in range(grid.size):
                for y in range(grid.size):
                    if x == 0 or y == 3:
                        break
                    else:
                        count += 1
                    if grid.map[x][y] >= grid.map[x][y+1] and grid.map[x][y] >= grid.map[x-1][y]:
                        bonus += 1
            if bonus == count and grid.map[0][3] <= grid.map[0][2] and grid.map[0][3] <= grid.map[1][3]:
                bonus += maxTile 
        elif grid.map[3][3] == maxTile:
            for x in range(grid.size):
                for y in range(grid.size):
                    if x == 0 or y == 0:
                        break
                    else:
                        count += 1
                    if grid.map[x][y] <= grid.map[x][y-1] and grid.map[x][y] <= grid.map[x-1][y]:
                        bonus += 1
            if bonus == count and grid.map[0][0] <= grid.map[1][0] and grid.map[0][0] <= grid.map[0][1]:
                bonus += maxTile 
        return bonus

    # monotinic
    def heuristic6(self, grid):
        l = []
        for x in range(grid.size):
            for y in range(grid.size):
                l.append(grid.map[x][y])
        r = 0.125

        # max at [0][0]
        w4 = np.array([1,2,3,4,2,3,4,5,3,4,5,6,4,5,6,7])
        # max at [3][0]
        w2 = np.array([4,5,6,7,3,4,5,6,2,3,4,5,1,2,3,4])
        # max at [0][3]
        w3 = np.array([4,3,2,1,5,4,3,2,6,5,4,3,7,6,5,4])

        # max at [3][3]
        w1 = np.array([7,6,5,4,6,5,4,3,5,4,3,2,4,3,2,1])
        w1 = np.power(w1,r)
        w2 = np.power(w2,r)
        w3 = np.power(w3,r)
        w4 = np.power(w4,r)
        return max(np.sum(w1*l),np.sum(w2*l),np.sum(w3*l),np.sum(w4*l))

    # snake
    def heuristic7(self, grid):
        l = []
        for x in range(grid.size):
            for y in range(grid.size):
                l.append(grid.map[x][y])
        r = 0.125
        # max at [0][0]
        w7 = np.array([4,3,2,1,5,6,7,8,12,11,10,9,13,14,15,16])
        w8 = np.array([4,5,12,13,3,6,11,14,2,7,10,15,1,8,9,16])
        # max at [3][0]
        w3 = np.array([13,14,15,16,12,11,10,9,5,6,7,8,4,3,2,1])
        w4 = np.array([1,8,9,16,2,7,10,15,3,6,11,14,4,5,12,13])
        # max at [0][3]
        w5 = np.array([1,2,3,4,8,7,6,5,9,10,11,12,16,15,14,13])
        w6 = np.array([13,12,5,4,14,11,6,3,15,10,7,2,16,9,8,1])
        # max at [3][3]
        w1 = np.array([16,15,14,13,9,10,11,12,8,7,6,5,1,2,3,4])
        w2 = np.array([16,9,8,1,15,10,7,2,14,11,6,3,13,12,5,4])
        return max(np.sum(w1*l),np.sum(w2*l),np.sum(w3*l),np.sum(w4*l),np.sum(w5*l),np.sum(w6*l),np.sum(w7*l),np.sum(w8*l))

    def evalfn(self, grid):
        return 0.1*max(self.heuristic6(grid),self.heuristic7(grid))+self.heuristic1(grid)+0.1*grid.getMaxTile()#+self.heuristic4(grid)#+self.heuristic5(grid)#+self.heuristic5(grid)
        #return 0.1*self.heuristic7(grid)+self.heuristic1(grid)+0.1*grid.getMaxTile()
        #return self.heuristic7(grid)
        #return 0.1*self.heuristic6(grid)

    def getMove(self, grid):
        timelimit = time.clock()+0.19
        result = self.ids(grid, timelimit)
        #result = self.alphabeta(grid, True, -float('inf'), float('inf'),3, timelimit)
        #result = self.minimax(grid,True, 3, timelimit)
        return result[1]
