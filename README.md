# _Evacuation Simulation_
A discrete agentic automation simulation of pedestrian evacuation dynamic implemented in Python using Pygame. It is based on the research paper published about floor field models introduced by Burstedde et al. (2001).

Agents navigate a room toward a single exit using static floor field computed by Dijkstra's algorithm which assigns every cell a cose base on its distance to the exit. Agents choose their next cell stochastically using transition probability formula from the paper:

`p_ij = N * exp(βJs * △s(i,j)) * (1 - n_ij) * d_ij`


Where △s(i,j) is the difference in static field between the neighbor and current cell, (1 - n_ij) blocks occupied cells, and d_ij blocks walls. Conflict resolution is handled by randomly selecting one winner when multiple agents compete for the same cell.

The simulation is designed to demonstrate the faster-is-slower effect the counterintuitive phenomenon where increasing agent urgency (via KD) leads to jamming near the exit and slower overall evacuation times.

Built with: Python, Pygame, NumPy

## Set up the virtual environment
Make sure Python is installed and in the PATH
Run command to create venv:
`python -m venv .venv`
### Windows (activate venv)
`.venv\Scripts\activate`
### Linux
`source .venv/bin/activate`

Use requirements.txt to get the dependencies
  - After activating virtual env, run:
    
    `pip install -r requirements.txt`

## To change the experiment outcomes
Go to `config.py`:
- make changes to the room dimension
- change the `KD` which in turn changes the urgency of each agent
