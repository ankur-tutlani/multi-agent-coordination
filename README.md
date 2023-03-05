
# Evolution of Strategic Choices under Coordination and Social Networks

This library is used to understand how specific actions or choices can evolve as the dominant choices when agents donot have any specific choices to begin with and they form their opinions based upon their interactions with other agents repeatedly. Agents have incentives to coordinate with other agents and are connected with each other through a specific social network. The strategies or actions which satisfy the norm criteria are potential candidates for setting the norm. In simple terms, norm is something which is played by more number of agents and for a longer periods of time.

## How to use it?


```bash
  # Install
  pip install multi-agent-coordination
  
  # Import
  from multi_agent_coordination import simulation

  # Execute 
  simulation.network_simulations(iteration_name = "test",
                        path_to_save_output = "C:\\Users\\Downloads\\",
                        num_neighbors = 2,
                        num_agents = 20,
                        prob_edge_rewire = 0.5,
                        grid_network_m = 5,
                        grid_network_n = 4,
                        name_len = 4,
                        num_of_trials = 20,
                        perturb_ratio = 0.05,
                        fixed_agents=[],
                        prob_new_name = 0,
                        network_name = "complete",
                        random_seed = 96852,
                        function_to_use = "perturbed_response1",
                        norms_agents_frequency = 0.7,
                        norms_time_frequency = 0.5
                        
                       )


```
    
## Function parameters
Following are the parameters which are required to be specified. At the end in the parenthesis, it shows the data type of the parameter which is required or the possible values which is required to be used. In following we will use agents' strategies, actions, choices, responses, names proposed interchangeably. These all represent same intent and meaning in our context.

1. iteration_name: Iteration name. (String)
2. path_to_save_output: Path to save output files. (String)
3. num_neighbors: Number of neighbours. (Integer)
4. num_agents: Number of agents. (Integer)
5. prob_edge_rewire: Small world network parameter. Probability of rewiring existing edges or adding new edges. (Float)
6. grid_network_m:  2-dimensional grid network parameter. Number of nodes. (Integer)
7. grid_network_n:  2-dimensional grid network parameter. Number of nodes. (Integer)
8. name_len: Length of random keywords created by the game. (Integer)
9. num_of_trials: Number of trials, how long the game should run. (Integer)
10. perturb_ratio: Probability of agents taking action randomly. (Float)
11. fixed_agents: Agents assumed as fixed. e.g. [2,3] shows we want agents 2 and 3 to be fixed. (List)
12. prob_new_name: Probability of agent suggesting new name at any time during the game. (Float)
13. network_name: Specify one of these values. A detailed explanation is provided below. ["small_world1","small_world2","small_world3","complete","random","grid2d"]. (String)
14. random_seed: Random seed value to reproduce results. (Integer)
15. function_to_use: Specify one of these values. A detailed explanation is provided below. ["perturbed_response1","perturbed_response2","perturbed_response3","perturbed_response4"]. (String)
16. norm_agents_frequency: Norm condition. Minimum percentage of agents require to propose same name at any given time. Specify number from 0 (0% agents) to 1(100% agents). (Float)
17. norm_time_frequency: Norm condition. Minimum percentage of times agents require to propose same name. Specify number from 0 (no time period) to 1 (all time periods). (Float)

<br />

In the "function_to_use" parameter above, below is the explanation for what these different values mean inside the list specified above.

1. perturbed_response1: Agents select the best response (1-"perturb_ratio")*100% times among the strategies which are most frequently used. If there is more than one such strategy, then agents select any one strategy randomly. Agents select random strategy ("perturb_ratio")*100% times among the strategies which are not most frequently used. Here also, if there is more than one such strategy, then agents select any one strategy randomly out of these.
2. perturbed_response2: Agent selects strategy randomly according to the relative weightage of different strategies. These relative weights are the % of times the respective strategy has been used by opponents in the past. 
3. perturbed_response3: This is same as "perturbed_response1" function except agent selects random strategy ("perturb_ratio")*100% times from all the possible strategies and not only from the ones which were not used most frequently by their opponents.
4. perturbed_response4: Agent selects the best response 100% of times among the strategies which are most frequently used. If there is more than one such strategy, then agents select any one strategy randomly. There is no perturbation element ("perturb_ratio" is considered as zero).

In all the four different response functions, agents propose new name at any point during the game with probability of "prob_new_name".


<br/>

In the "network_name" parameter above, below is the explanation for what these different values mean inside the list specified above.
1. small_world1: Returns a Watts Strogatz small-world graph. Here number of edges remained constant once we increase the "prob_edge_rewire" value. Shortcut edges if added would replace the existing ones. But total count of edges remained constant.
2. small_world2: Returns a Newman Watts Strogatz small-world graph. Here number of edges increased once we increase the "prob_edge_rewire" value. It would add more shortcut edges in addition to what already exist.
3. small_world3: Returns a connected Watts Strogatz small-world graph. Rest of the explanation remains as small_world1.
4. complete: Returns the complete graph.
5. random: Compute a random graph by swapping edges of a given graph. The given graph used is Watts Strogatz small-world graph (the one produced by "small_world1").
6. grid2d: Return the 2d grid graph of mxn nodes, each connected to its nearest neighbors.

We have used the networkx python library to populate these graphs. For more information around these graphs and how these are produced please refer to the link in the reference section.



## Function explanation
Here we explain the underlying functioning of this library with the help of an example. But the logic can be replicated to any coordination game where there is a positive reward if agents follow the same strategy as their neighbour/opponent, and zero/negative reward if agents follow different strategy.

We assume agents play naming game as defined in Young (2015). Naming game is a coordination game wherein two agents are shown a picture of a face and they simultaneously and independently suggest names for it. If agents provide same name, they earn a positive reward and if they provide different names, they pay a small penalty (negative reward). There is no restriction on the names that agents can provide, this is left to their imagination. Agents do not know with whom they are paired or their identities. Agents can recollect the names provided by their partners in previous rounds.

We assume there are 20 ("num_agents") agents and are connected with 2 ("num_neighbors") other agents in their neighbourhood. We assume that the positive reward and negative reward are constant values. If we assume agents are connected via ring network structure, the network looks like as in below figure. For instance, agent 0 relates to 2 agents, agent 1 and 19. Similarly, agent 5 is connected with agents 4 and 6. We assume the network to be undirected.


![](https://github.com/ankur-tutlani/multi-agent-coordination/raw/main/input_network.png)



We start the game with one edge of the network is selected at any given point. Edge of the network is represented as (0,1), (5,4) etc, implying agents 0 and 1 are connected with each other, agents 5 and 4 are connected with each other. During each time period, all edges are selected sequentially and the agents associated with those edges play the game.

To begin with, agents do not have history to look back into, hence agents propose names randomly. Agents do not know the identity of the other agents with whom they are being paired. At the end of a given time period, agents do know the names proposed by other agents. Once agents have history of names proposed by other agents, they take into consideration the names proposed by their opponents in the next successive plays. This way agents get to know the names which are popular among the agents.

We assume name to be any string of length "name_len", a combination of alpha and numeric characters generated randomly. Agents keep track of names proposed by other agents and accordingly update their actions in the successive rounds of play. We assume agents have bounded rationality and engaged in limited calculations to decide upon what action to take.

We have considered different combinations of approaches or methods that agents can adopt while taking actions. We assume that agents use perturbed best response implying agents can take action randomly with a certain probability (Young, 2015). At each time when agents require to take action, they consider the names proposed in the past by their opponents and decide what name to propose in the current period. We have tested four different ways which agents can use to decide what action to take. The "function_to_use" parameter provides details about these and how these are different to each other.

When the simulations are run for "num_of_trials" timeperiod, we get the percentage distribution of different names (strategies) which agents proposed. The names which satisfy the two conditions for norm specified by "norms_agents_frequency" and "norms_time_frequency" are considered as norm. We have looked at two dimensions of norms, number of agents following the norm and for how long it has been followed. We can see the output like below. In below graph, X-axis shows the timeperiod, and Y-axis shows the % of agents who proposed the respective name. Y-axis values are in ratio format (range from 0 - 1), so would need to multiply by 100 to get this in percentage format.



![](https://github.com/ankur-tutlani/multi-agent-coordination/raw/main/top_names.png)



In above figure, name "1E1C" satisfies the norm criteria, when we assume "norms_agents_frequency" as 0.7 and "norms_time_frequency" as 0.5. This implies at least 70% of agents following "1E1C" for at least 50% of times. The network structure looks like below by the end of "num_of_trials" timeperiods. Agents who proposed same name majority of times during the run are colored in same colour. Color itself has no significance here, it is just used to denote agents proposing same name. Same color agents taking same action majority of the times.


![](https://github.com/ankur-tutlani/multi-agent-coordination/raw/main/network_after_50_timeperiods.png)


The detailed explanation of the output generated is provided in the next section.


## How to interpret output?
There are total 9 files generated in the output when there is at least 1 name which satisfies the norm criteria.

    input_network_complete_2023-02-01-15-24-22.png
    network_after_50_timeperiods_complete_2023-02-01-15-24-22.png
	top_names_complete_2023-02-01-15-24-22.png
    parameters_complete_2023-02-01-15-24-22.xlsx
    aggregate_data_detailed_agent_complete_2023-02-01-15-24-22.xlsx
	normcandidates_complete_2023-02-01-15-24-22.xlsx
    time_when_reached_norm_complete_2023-02-01-15-24-22.xlsx
    first_agent_proposed_norm_complete_2023-02-01-15-24-22.xlsx
	fixed_agent_name_proposed_smallworld_10_2023-02-01-17-16-19.xlsx
    


The image files (.png) show the network graphs and the strategy trend graph for the simulation. The "input_network_.." file is the input network with which the game is started. The "network_after_..." file is the network state at the end of game. Agents following the same strategy most frequently, they would be coloured in the same colour in this file. The "top_names_.." png file shows the percent of times specific name is proposed over a period of time.

Parameters file "parameters_.." lists all the parameters which have been specified in the function call. File "aggregate_data_detailed_.." has the information on names proposed by each agents at all time periods. 

Norm file "normcandidates_..." shows names that satisfy the norm criteria laid out. File "time_when_reached_norm_..." shows the time period number when the name met the norm criteria. "first_agent_proposed_norm_" file shows the agent information who proposed that name first during the simulation run. These 3 files are generated only when at least one name satisfies the norm criteria. 

When there is at least one fixed agent specified, we will see "fixed_agent_name_proposed_.." file also gets generated. This file shows the names proposed by fixed agents.

All the file names end with date and time stamp when the function was executed. It also contains information on network structure used like "complete" or "smallworld" network etc.


## References
1. Young, H.P. "The evolution of social norms" Annual Review of Economics. 2015 (7),pp.359-387
2. https://pypi.org/project/networkx/ 

