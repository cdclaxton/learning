# Agents exist on a grid and walk about at random
# They pass money to an agent sharing the same cell

import matplotlib.pyplot as plt
import mesa
import numpy as np


def compute_gini(model: mesa.Model) -> float:
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi*(N-i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1/N) - 2*B


class MoneyAgent(mesa.Agent):
    """An agent with a fixed initial wealth."""

    def __init__(self, unique_id: int, model: mesa.Model) -> None:
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self) -> None:
        self.move()
        if self.wealth > 0:
            self.give_money()
        
    def move(self) -> None:
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore = True,
            include_center = False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    
    def give_money(self) -> None:
        cell_mates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cell_mates) > 1:
            other = self.random.choice(cell_mates)
            other.wealth += 1
            self.wealth -= 1


class MoneyModel(mesa.Model):
    """A model with a given number of agents."""

    def __init__(self, N: int, width: int, height: int) -> None:
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)

        # Create the agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x,y))
    
        # Setup the data collector
        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": "wealth"}
        )

    def step(self) -> None:
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()
    

if __name__ == '__main__':

    model = MoneyModel(50, 10, 10)
    for i in range(100):
        model.step()
    
    agent_counts = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        agent_counts[x][y] = len(cell_content)

    fig, ax = plt.subplots(2, 2)

    im1 = ax[0, 0].imshow(agent_counts, interpolation="nearest")

    # Get the model-level Gini coefficient as a Pandas dataframe
    gini = model.datacollector.get_model_vars_dataframe()
    gini.plot(ax=ax[0,1])

    agent_wealth = model.datacollector.get_agent_vars_dataframe()
    
    end_wealth = agent_wealth.xs(99, level="Step")["Wealth"]
    end_wealth.hist(ax=ax[1,0], bins=range(agent_wealth.Wealth.max() + 1))

    # Wealth of a single agent
    one_agent_wealth = agent_wealth.xs(14, level="AgentID")
    one_agent_wealth.plot(ax=ax[1,1])

    plt.show()
    