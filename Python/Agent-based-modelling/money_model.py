# Simulated agent-based economy
#
# Rules:
# 1. Some number of agents;
# 2. All agents start with 1 unit of money; and
# 3. At every time step, an agent gives 1 unit of money
#    if they have it to another agent

import matplotlib.pyplot as plt
import mesa

class MoneyAgent(mesa.Agent):
    """An agent with a fixed initial wealth."""

    def __init__(self, unique_id: int, model: mesa.Model) -> None:
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self) -> None:
        if self.wealth == 0:
            return
        
        other_agent = self.random.choice(self.model.schedule.agents)
        other_agent.wealth += 1
        self.wealth -= 1


class MoneyModel(mesa.Model):
    """A model with a given number of agents."""

    def __init__(self, N: int) -> None:
        self.num_agents = N
        self.schedule = mesa.time.RandomActivation(self)

        # Create the agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
    
    def step(self) -> None:
        """Advance the model by one step."""
        self.schedule.step()
    

if __name__ == '__main__':
    
    all_wealth = []

    for j in range(100):

        # Run the model
        model = MoneyModel(10)
        for i in range(10):
            model.step()

        # Store the results
        for agent in model.schedule.agents:
            all_wealth.append(agent.wealth)

    plt.hist(all_wealth, bins=range(max(all_wealth) + 1))
    plt.show()
