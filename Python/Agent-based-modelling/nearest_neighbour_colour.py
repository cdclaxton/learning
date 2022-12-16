# Agent-based model of colour changing agents who flip a biased coin to 
# determine if they are going to do one of two strategies:
#
# 1. Be (potentially) unique -- the agent chooses a random colour;
# 2. Take the most frequent colour from amongst their neighbours.

from celluloid import Camera
import matplotlib.pyplot as plt
import mesa
import numpy as np
import random


class ColourChangingAgent(mesa.Agent):
    """An agent that changes colour depending on its neighbours."""

    def __init__(self, unique_id: int, model: mesa.Model, num_colours: int, 
        p: float) -> None:

        super().__init__(unique_id, model)
        self.colour = random.randint(0, num_colours-1)
        self.p = p

    def step(self) -> None:

        # Get the neighbours
        neighbours = self.model.grid.get_neighbors(
            self.pos, 
            moore=True,
            include_center=False,
            radius=2)
        
        # Get the colours of the neighbours
        colours: list[int] = [n.colour for n in neighbours]

        if np.random.random() < self.p:
            self.colour = random.randint(0, num_colours-1)
        else:
            # Find the most frequent colour
            counts = np.bincount(colours)
            most_frequent = np.argmax(counts)
            self.colour = most_frequent


class ColourChangingModel(mesa.Model):
    """A model with colour changing agents."""

    def __init__(self, width:int, height: int, num_colours:int, p:float) -> None:
        self.num_colours = num_colours
        self.grid = mesa.space.SingleGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)

        # Create the agents
        agent_id = 0
        for i in range(width):
            for j in range(height):

                # Make the agent
                agent = ColourChangingAgent(agent_id, self, self.num_colours, p)
                self.schedule.add(agent)
                agent_id += 1

                # Set its position
                self.grid.place_agent(agent, (i,j))
        
    def step(self) -> None:
        """Advance the model by one step."""

        self.schedule.step()
    

if __name__ == '__main__':

    fig = plt.figure()
    ax = fig.subplots(1)
    camera = Camera(fig)

    num_colours = 10
    p_unique = 0.01
    model = ColourChangingModel(50, 50, num_colours, p_unique)
    for i in range(40):

        agent_colour = np.zeros((model.grid.width, model.grid.height))
        for cell in model.grid.coord_iter():
            agent, x, y = cell
            agent_colour[x][y] = agent.colour
        
        ax.imshow(agent_colour, interpolation="none", vmin=0, vmax=num_colours)
        ax.text(1, 2, f"Time step {i}", color="white")
        camera.snap()

        model.step()
    
    animation = camera.animate()
    plt.show()
