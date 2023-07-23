import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GameOfLife:
    map_side = 130
    alive_value = 255
    dead_value = 0
    # als = [ON, OFF]

    def __init__(self):
        values = [self.alive_value, self.dead_value]
        self.grid = np.random.choice(
            values, (self.map_side, self.map_side), p=[0.3, 0.7])

    def count_alive_neighbors(self, i: int, j: int,map_sise) -> int:
        ans = 0
        if(i+1 < map_sise):
            if(j+1 < map_sise):
                ans += self.grid[i+1, j+1]//255
            ans += self.grid[i+1, j]//255
            if(j-1 > -1):
                ans += self.grid[i+1, j-1]//255
        if(i-1 > -1):
            if(j+1 < map_sise):
                ans += self.grid[i-1, j+1]//255
            ans += self.grid[i-1, j-1]//255
            if(j-1 > -1):
                ans += self.grid[i-1, j]//255
        if(j+1 < map_sise):
            ans += self.grid[i, j+1]//255
        if(j-1>-1):
            ans += self.grid[i, j-1]//255
        
        
        return ans
    
    def update(self):
        new_grid = np.zeros_like(self.grid)
        for i in range(self.map_side):
            for j in range(self.map_side):
                alive_neighbours = self.count_alive_neighbors(i, j,self.map_side)
                #print(alive_neighbours , i , j)
                if(self.grid[i,j] == 0):
                    if alive_neighbours == 3:
                        new_grid[i, j] = self.alive_value
                else:
                    if alive_neighbours < 2 or alive_neighbours > 3:
                        new_grid[i,j] = self.dead_value
                    else:
                        new_grid[i,j] = self.alive_value
        #print(type(self.grid()) , type(new_grid))
        self.grid = new_grid



def update_animatiom(frame, mat, game: GameOfLife):
    game.update()
    mat.set_data(game.grid)
    return [mat]

def animate():
    fig, ax = plt.subplots()
    game = GameOfLife()
    mat = ax.matshow(game.grid)
    ani = animation.FuncAnimation(fig, update_animatiom, interval=100,
                              save_count=100, fargs=(mat, game,))
    plt.show()
    
animate()
