# beam-align

Code for the paper https://arxiv.org/abs/2206.13166.

There are four main scripts:

1. **simulate_opt_x.py**: this finds the optimal solution using the optimization problem provided in `new_optimization.py`. In `parameters.py` are given, and you can input certain scenario's (see below) for certain parameter settings.
2. **BEAM-ALIGN.py**: we devised a heuristic algorithm based on beam alignment between user and BS. This algorithm again takes as input all parameters given in `parameters.py` and outputs the heuristic user association.
3. **SNR_heuristic.py**: similar to BEAM-ALIGN, but this is a heuristic based on only highest received SNR.
4. **MCUA-PA heuristic.py**: this heuristic is based on Harris Hawkes Optimization and described in [1]. We implemented the algorithm of this paper in `MCUA-PA.py` and `MCUA-PA heuristic.py`

Next to that, there are some helper functions: `functions.py` is a collection of all functions relevant to the system model (based on 3GPP), such as the beamforming gain, path loss and interference. In `simulate_blockersj.py`, we implemented an algorithm to simulate blockers (rectangles with a certain angle, width and length) in a certain area. Lastly, `find_data.py` and `get_data.py` are scripts to rewrite the data in such a format that it can be used to make all figures.

### Scenario's
We defined different scenario's, based on different beamwidths, number of connections per user and whether we simulate a clustered user setting. 

[1] Jin, K., Cai, X., Du, J., Park, H., & Tang, Z. (2022). Toward energy efficient and balanced user associations and power allocations in multiconnectivity-enabled mmWave networks. IEEE Transactions on Green Communications and Networking, 6(4), 1917-1931.