This folder contains some RL algorithms to solve Mountain Car problem.

The Mountain_car enviroment is refered to gym library, OpenAI.

All algorithms are implemented from " Reinforcement Learning:
An Introduction",Richard S. Sutton and Andrew G. Barto, prof. David Silver and prof. Jun Pyo Hong courses

# Mountain Car Problem:
- A car is started at the bottom of valley.
- For any given state, the agent may choose to accelerate to the left, right or cease any acceleration.
- Observation:
         Index             Observation                  Min        Max
         0                 Car position(x-axis)         -1.2       0.6
         1                 Car Velocity                 -0.07      0.07
- Actions: 
         Index                  Action
         0                      Accelerate to the left
         1                      Do not accelerate
         2                      Accelerate to the right
- Episode termination:
    The car position is more than 0.5 or episode length is greater than 1000 steps
