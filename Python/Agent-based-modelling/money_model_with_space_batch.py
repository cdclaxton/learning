# Batch run
# Agents exist on a grid and walk about at random
# They pass money to an agent sharing the same cell

import matplotlib.pyplot as plt
import mesa
import pandas as pd


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
        self.running = True

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

    params = {"width": 10, "height": 10, "N": range(10, 500, 50)}

    results = mesa.batch_run(
        MoneyModel,                # Model class to run
        parameters=params,         # Dict of all parameters of model class
        iterations=5,              # Number of iterations per parameter setting
        max_steps=100,             # Number of steps after which model halts
        number_processes=1,        # Number of processes (multiprocessing)
        data_collection_period=1,  # Number of steps before data collected
        display_progress=True      # Display batch run progress 
    )

    # Convert results to a dataframe
    results_df = pd.DataFrame(results)

    # ['RunId', 'iteration', 'Step', 'width', 'height', 'N', 'Gini', 'AgentID',
    #  'Wealth']
    print(results_df.keys())

    results_filtered = results_df[(results_df.AgentID == 0) & (results_df.Step == 100)]
    N_values = results_filtered.N.values
    gini_values = results_filtered.Gini.values

    plt.scatter(N_values, gini_values)
    plt.show()
