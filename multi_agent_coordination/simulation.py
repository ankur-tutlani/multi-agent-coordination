
import numpy as np   
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import datetime
import random
import string



# 1.iteration_name: iteration name. String
# 2.path_to_save_output: path to save output files. String 
# 3.num_neighbors: number of neighbours. Integer
# 4.num_agents: number of agents. Integer
# 5.prob_edge_rewire: small world network parameter. Probability of rewiring each edge. Float
# 6.grid_network_m:  2-dimensional grid network parameter. Number of nodes. Integer
# 7.grid_network_n:  2-dimensional grid network parameter. Number of nodes. Integer
# 8.name_len: length of random keywords created by the game. Integer
# 9.num_of_trials: number of trials. Integer    
# 10.perturb_ratio: probability of agents taking action randomly. Float
# 11.fixed_agents: agents assumed as fixed. List
# 12.prob_new_name: probability of agent suggesting new name. Float
# 13.network_name: specify one of these values [small_world1,small_world2,small_world3,complete,random,grid2d]. String
# 14.random_seed: random seed value. Integer 
# 15.function_to_use: specify one of these values [perturbed_response1,perturbed_response2,perturbed_response3,perturbed_response4]. String  
# 16.norm_agents_frequency: norm condition. Minimum percentage of agents require to propose same name. Specify number from 0 to 1. Float
# 17.norm_time_frequency: norm condition. Minimum percentage of times agents require to propose same name. Specify number from 0 to 1. Float     

# function_to_use
# perturbed_response1: Agent selects the best response (1-perturb_ratio)*100% times among the strategies which are most frequently used. Agents selects random strategy (perturb_ratio)*100% times from which are not most frequently used. Agents propose new name at any point during the game with probability of prob_new_name.
# perturbed_response2: Agent selects strategy according to the % share in which it has been used by opponents in the past.Agents propose new name at any point during the game with probability of prob_new_name.
# perturbed_response3: This is same as perturbed_response1 function except agent selects random strategy (perturb_ratio)*100% times from all the strategies. Agents propose new name at any point during the game with probability of prob_new_name.
# perturbed_response4: Agent selects the best response 100% times among the strategies which are most frequently used. There is no perturbation element.Agents propose new name at any point during the game with probability of prob_new_name.
    
 
# Note there may be instances wherein more than 1 strategy has been used by opponent agents more frequently.
# E.g. if an agent comes across s1 and s2 strategy used by their opponent agents most frequently during any history and both s1 and s2
# have been used equally in the past, in that case agent deciding to take action will select randomly from s1 and s2.


# network_name
# small_world1: Returns a Watts–Strogatz small-world graph. Here number of edges remained constant once we increase the prob_edge_rewire value.Shortcut edges if added would replace the existing ones. But total count of edges remained constant.
# small_world2: Returns a Newman–Watts–Strogatz small-world graph. Here number of edges increased once we increase the prob_edge_rewire value. Would add more shortcut edges in addition to what already exist.
# small_world3: Returns a connected Watts–Strogatz small-world graph.
# complete: Returns the complete graph.
# random: Compute a random graph by swapping edges of a given graph.
# grid2d: Return the 2d grid graph of mxn nodes, each connected to its nearest neighbors.




def perturbed_response1(AGENT_NO,data_to_look,perturb_ratio,name_len,prob_new_name):

    try:
        count_pd = data_to_look.loc[data_to_look["agent"]==AGENT_NO]["name_offered_by_opponent"].value_counts().reset_index()
        count_pd["tot_sum"] = count_pd["name_offered_by_opponent"] / sum(count_pd["name_offered_by_opponent"])
        best_response = count_pd.loc[count_pd["tot_sum"] == max(count_pd["tot_sum"])]['index'].tolist()
        draw1= random.choices(population=best_response,k=1)

        Nonbest_response = count_pd.loc[count_pd["tot_sum"] != max(count_pd["tot_sum"])]['index'].tolist()
        if len(Nonbest_response) > 0:
            draw2= random.choices(population=Nonbest_response,k=1)
            best_response = random.choices(population=[draw1[0],draw2[0]],weights=[1-perturb_ratio,perturb_ratio],k=1)
            best_response = best_response[0]
        else:
            best_response = draw1[0]


    except:
        best_response = [''.join(random.choices(string.ascii_uppercase+string.digits,k=name_len))]
        best_response = best_response[0]


    best_response2 = [''.join(random.choices(string.ascii_uppercase+string.digits,k=name_len))]
    best_response2 = best_response2[0]

    best_response3 = random.choices(population=[best_response,best_response2],weights=[1-prob_new_name,prob_new_name],k=1)[0]

    return best_response3




def perturbed_response2(AGENT_NO,data_to_look,name_len,prob_new_name):
    try:
        count_pd = data_to_look.loc[data_to_look["agent"]==AGENT_NO]["name_offered_by_opponent"].value_counts().reset_index()
        count_pd["tot_sum"] = count_pd["name_offered_by_opponent"] / sum(count_pd["name_offered_by_opponent"])
        names_list = count_pd['index'].tolist()
        share_list = count_pd['tot_sum'].tolist()
        draw1= random.choices(population=names_list,weights=share_list,k=1)
        best_response = draw1[0]


    except:
        best_response = [''.join(random.choices(string.ascii_uppercase+string.digits,k=name_len))]
        best_response = best_response[0]

    best_response2 = [''.join(random.choices(string.ascii_uppercase+string.digits,k=name_len))]
    best_response2 = best_response2[0]

    best_response3 = random.choices(population=[best_response,best_response2],weights=[1-prob_new_name,prob_new_name],k=1)[0]


    return best_response3




def perturbed_response3(AGENT_NO,data_to_look,perturb_ratio,name_len,prob_new_name):
    try:
        count_pd = data_to_look.loc[data_to_look["agent"]==AGENT_NO]["name_offered_by_opponent"].value_counts().reset_index()
        count_pd["tot_sum"] = count_pd["name_offered_by_opponent"] / sum(count_pd["name_offered_by_opponent"])
        best_response = count_pd.loc[count_pd["tot_sum"] == max(count_pd["tot_sum"])]['index'].tolist()
        draw1= random.choices(population=best_response,k=1)

        Nonbest_response = count_pd['index'].tolist()
        draw2= random.choices(population=Nonbest_response,k=1)
        best_response = random.choices(population=[draw1[0],draw2[0]],weights=[1-perturb_ratio,perturb_ratio],k=1)
        best_response = best_response[0]

    except:
        best_response = [''.join(random.choices(string.ascii_uppercase+string.digits,k=name_len))]
        best_response = best_response[0]

    best_response2 = [''.join(random.choices(string.ascii_uppercase+string.digits,k=name_len))]
    best_response2 = best_response2[0]

    best_response3 = random.choices(population=[best_response,best_response2],weights=[1-prob_new_name,prob_new_name],k=1)[0]

    return best_response3




def perturbed_response4(AGENT_NO,data_to_look,name_len,prob_new_name):
    try:
        count_pd = data_to_look.loc[data_to_look["agent"]==AGENT_NO]["name_offered_by_opponent"].value_counts().reset_index()
        count_pd["tot_sum"] = count_pd["name_offered_by_opponent"] / sum(count_pd["name_offered_by_opponent"])
        best_response = count_pd.loc[count_pd["tot_sum"] == max(count_pd["tot_sum"])]['index'].tolist()
        draw1= random.choices(population=best_response,k=1)
        best_response = draw1[0]

    except:
        best_response = [''.join(random.choices(string.ascii_uppercase+string.digits,k=name_len))]
        best_response = best_response[0]

    best_response2 = [''.join(random.choices(string.ascii_uppercase+string.digits,k=name_len))]
    best_response2 = best_response2[0]

    best_response3 = random.choices(population=[best_response,best_response2],weights=[1-prob_new_name,prob_new_name],k=1)[0]

    return best_response3




def network_simulations(iteration_name,
                        path_to_save_output,
                        num_neighbors,
                        num_agents,
                        prob_edge_rewire,
                        grid_network_m,
                        grid_network_n,
                        name_len,
                        num_of_trials,
                        perturb_ratio,
                        fixed_agents,
                        prob_new_name,
                        network_name,
                        random_seed,
                        function_to_use,
                        norms_agents_frequency,
                        norms_time_frequency
                        
                       ):
    
    
    iteration_name = iteration_name
    today = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    path_to_save_output = path_to_save_output
    num_neighbors = num_neighbors
    num_agents= num_agents
    prob_edge_rewire = prob_edge_rewire
    grid_network_m=grid_network_m
    grid_network_n=grid_network_n
    name_len = name_len
    num_of_trials =  num_of_trials
    perturb_ratio = perturb_ratio
    fixed_agents = fixed_agents
    prob_new_name=prob_new_name
    network_name = network_name
    random_seed = random_seed
    function_to_use =  function_to_use
    norms_agents_frequency = norms_agents_frequency
    norms_time_frequency = norms_time_frequency

    random.seed(random_seed)
    
    if network_name == 'small_world1': 
        G = nx.watts_strogatz_graph(num_agents,num_neighbors,prob_edge_rewire)
    if network_name == 'small_world2': 
        G = nx.newman_watts_strogatz_graph(n=num_agents,k=num_neighbors,p=prob_edge_rewire,seed=random_seed)
    if network_name == 'small_world3':
        G = nx.connected_watts_strogatz_graph(n=num_agents,k=num_neighbors,p=prob_edge_rewire,seed=random_seed)
    if network_name == 'complete':
        G = nx.complete_graph(num_agents)
    if network_name == 'random':
        G = nx.watts_strogatz_graph(num_agents,num_neighbors,prob_edge_rewire)
        G = nx.random_reference(G, niter=5, connectivity=True, seed=random_seed)
    if network_name == 'grid2d':
        G = nx.grid_2d_graph(m=grid_network_m,n=grid_network_n)
        mapping = dict(zip(G, range(len(G))))
        G = nx.relabel_nodes(G, mapping)
        
        
    nx.draw(G,with_labels=True)
    plt.savefig(path_to_save_output+"input_network_"+iteration_name+"_"+today+".png")
    plt.clf()
    
    potential_edges = list(G.edges)
    
    empty_df_to_fill_trial = pd.DataFrame()
    empty_df_to_fill_trial["agent"] = -1
    empty_df_to_fill_trial["name_offered"] = ''
    empty_df_to_fill_trial["opponentagent"] = -1
    empty_df_to_fill_trial["name_offered_by_opponent"] = ''
    empty_df_to_fill_trial["pair"] = ""
    empty_df_to_fill_trial["timeperiod"] = -1

    
    fixed_values_to_use = dict()
    num_of_rounds = len(potential_edges)
    norms_db_to_fill = pd.DataFrame()
    norms_db_to_fill['name'] = ''
    norms_db_to_fill['percent_count'] = ''
    norms_db_to_fill['timeperiod'] = ''
    
    
    for timeperiod in range(1,num_of_trials+1):
        empty_df_to_fill_temp = empty_df_to_fill_trial[0:0]
        for v in range(num_of_rounds):
            vcheck = potential_edges[v]
            agent1 = vcheck[0]
            agent2 = vcheck[1]

            if function_to_use == 'perturbed_response1':
                if len(empty_df_to_fill_temp) > len(empty_df_to_fill_trial):

                    name_to_fill1 = perturbed_response1(AGENT_NO = agent1,data_to_look = empty_df_to_fill_temp,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)
                    name_to_fill2 = perturbed_response1(AGENT_NO = agent2,data_to_look = empty_df_to_fill_temp,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)
                else:
                    name_to_fill1 = perturbed_response1(AGENT_NO = agent1,data_to_look = empty_df_to_fill_trial,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)
                    name_to_fill2 = perturbed_response1(AGENT_NO = agent2,data_to_look = empty_df_to_fill_trial,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)

            elif function_to_use == 'perturbed_response2':
                if len(empty_df_to_fill_temp) > len(empty_df_to_fill_trial):

                    name_to_fill1 = perturbed_response1(AGENT_NO = agent1,data_to_look = empty_df_to_fill_temp,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)
                    name_to_fill2 = perturbed_response1(AGENT_NO = agent2,data_to_look = empty_df_to_fill_temp,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)
                else:
                    name_to_fill1 = perturbed_response1(AGENT_NO = agent1,data_to_look = empty_df_to_fill_trial,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)
                    name_to_fill2 = perturbed_response1(AGENT_NO = agent2,data_to_look = empty_df_to_fill_trial,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)



            elif function_to_use == 'perturbed_response3':
                if len(empty_df_to_fill_temp) > len(empty_df_to_fill_trial):

                    name_to_fill1 = perturbed_response1(AGENT_NO = agent1,data_to_look = empty_df_to_fill_temp,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)
                    name_to_fill2 = perturbed_response1(AGENT_NO = agent2,data_to_look = empty_df_to_fill_temp,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)
                else:
                    name_to_fill1 = perturbed_response1(AGENT_NO = agent1,data_to_look = empty_df_to_fill_trial,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)
                    name_to_fill2 = perturbed_response1(AGENT_NO = agent2,data_to_look = empty_df_to_fill_trial,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)



            elif function_to_use == 'perturbed_response4':
                if len(empty_df_to_fill_temp) > len(empty_df_to_fill_trial):

                    name_to_fill1 = perturbed_response1(AGENT_NO = agent1,data_to_look = empty_df_to_fill_temp,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)
                    name_to_fill2 = perturbed_response1(AGENT_NO = agent2,data_to_look = empty_df_to_fill_temp,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)
                else:
                    name_to_fill1 = perturbed_response1(AGENT_NO = agent1,data_to_look = empty_df_to_fill_trial,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)
                    name_to_fill2 = perturbed_response1(AGENT_NO = agent2,data_to_look = empty_df_to_fill_trial,perturb_ratio=perturb_ratio,name_len=name_len,prob_new_name=prob_new_name)



            if (agent1 in fixed_agents or agent2 in fixed_agents) and len(fixed_values_to_use) < len(fixed_agents):
                for jj in fixed_agents:
                    if jj not in list(fixed_values_to_use.keys()):
                        xx = empty_df_to_fill_temp.loc[empty_df_to_fill_temp["agent"]==jj].sort_values(["timeperiod"],ascending=True).head(1)
                        if len(xx) > 0:
                            fixed_values_to_use[xx["agent"].values[0]]=xx["name_offered"].values[0]

            if agent1 in fixed_agents:
                try:
                    name_offered = fixed_values_to_use[agent1]
                except:
                    name_offered = name_to_fill1
            else:
                name_offered = name_to_fill1


            if agent2 in fixed_agents:
                try:
                    name_offered_by_opponent = fixed_values_to_use[agent2]
                except:
                    name_offered_by_opponent = name_to_fill2
            else:
                name_offered_by_opponent = name_to_fill2


            data_to_append = pd.DataFrame({'agent':agent1,
                                               'name_offered':name_offered,
                                               'name_offered_by_opponent':name_offered_by_opponent,
                                               'opponentagent':agent2,
                                               'pair':str(vcheck), 
                                               'timeperiod':timeperiod
                                               },index=[0])

            data_to_append2 = pd.DataFrame({'agent':agent2,
                                               'name_offered':name_offered_by_opponent,
                                               'name_offered_by_opponent':name_offered,
                                               'opponentagent':agent1,
                                               'pair':str(vcheck), 
                                               'timeperiod':timeperiod
                                               },index=[0])


            empty_df_to_fill_temp = pd.concat([empty_df_to_fill_temp,data_to_append,data_to_append2],ignore_index=True,sort=False)


        empty_df_to_fill_trial = pd.concat([empty_df_to_fill_trial,empty_df_to_fill_temp],ignore_index=True,sort=False)
        footemp = empty_df_to_fill_temp['name_offered'].value_counts(normalize=True).to_frame()
        footemp.columns = ['percent_count']
        footemp['name'] = footemp.index.values
        footemp=footemp[['name','percent_count']].reset_index(drop=True)
        footemp['timeperiod'] = timeperiod

        norms_db_to_fill = pd.concat([norms_db_to_fill,footemp],ignore_index=True,sort=False)
        
        
    norms_candidates = norms_db_to_fill.loc[norms_db_to_fill['percent_count']>=norms_agents_frequency]
    norms_to_store = []
    percent_time_frequency = []
    if len(norms_candidates) > 0:
        potential_norms_candidate = np.unique(norms_candidates['name']).tolist()
        for k in potential_norms_candidate:
            norms_candidates2 = norms_candidates.loc[norms_candidates['name']==k]
            distinct_timeperiod = len(np.unique(norms_candidates2['timeperiod']))
            norms_candidates2 = round(distinct_timeperiod/len(np.unique(norms_db_to_fill['timeperiod'])),2)
            if norms_candidates2 >= norms_time_frequency:
                norms_to_store.append(k)
                percent_time_frequency.append(norms_candidates2)
                
    
    try:
        norms_candidates2 = pd.DataFrame()
        norms_candidates2["percent_count"] = percent_time_frequency
        norms_candidates2["name"] = norms_to_store
        if len(norms_candidates2) > 0:
            norms_candidates2.to_excel(path_to_save_output+"normcandidates_"+iteration_name+"_"+today+".xlsx",index=None)
    except:
        pass
    
    
    
    
    db_to_fill2 = pd.DataFrame()
    db_to_fill2["timeperiod"] = -1
    db_to_fill2["name_offered"] = -1

    if len(norms_to_store) > 0:
        for j in norms_to_store:
            foocheck = norms_candidates.loc[norms_candidates["name"]==j]
            foocheck = foocheck.sort_values(["timeperiod"])
            foocheck["count_names_offered"] = (foocheck["name"]==j).cumsum()
            foocheck["cum_perc"] = foocheck["count_names_offered"]/len(np.unique(norms_db_to_fill['timeperiod'])) ## divide by total timeperiod.
            xxxx= foocheck.loc[foocheck["cum_perc"]>=norms_time_frequency][["timeperiod"]].head(1)
            if xxxx.shape[0] > 0:
                timev = foocheck.loc[foocheck["cum_perc"]>=norms_time_frequency][["timeperiod"]].head(1)["timeperiod"].values[0]
                foodb = pd.DataFrame({"timeperiod":[timev],"name_offered":[j]})
                db_to_fill2 = pd.concat([db_to_fill2,foodb],ignore_index=True,sort=False)
                
    
    try:
        if len(db_to_fill2) > 0:
            db_to_fill2.to_excel(path_to_save_output+"time_when_reached_norm_"+iteration_name+"_"+today+".xlsx",index=None)
    except:
        pass
    
    
    
    empty_df_to_fill_trial = empty_df_to_fill_trial.sort_values(["timeperiod"])
    agent_no_to_fill = []
    if len(norms_to_store) > 0:
        for j in norms_to_store:
            xx = empty_df_to_fill_trial.loc[empty_df_to_fill_trial["name_offered"]==j].head(1)["agent"].values[0]
            agent_no_to_fill.append(xx)
            
    
    data1_to_save = pd.DataFrame({'first_agent_propose_the_name':agent_no_to_fill,'name_proposed':norms_to_store})
    try:
        if len(data1_to_save) > 0:
            data1_to_save.to_excel(path_to_save_output+"first_agent_proposed_norm_"+iteration_name+"_"+today+".xlsx",index=None)
    except:
        pass
    
    
    if len(fixed_agents) > 0:
        fixed_agents_data =empty_df_to_fill_trial.loc[empty_df_to_fill_trial["agent"].isin(fixed_agents)][["agent","name_offered","timeperiod"]]
        fixed_agents_data=fixed_agents_data.sort_values(["agent","timeperiod"])
        fixed_agents_data = fixed_agents_data.groupby("agent").first().reset_index()
        fixed_agents_data.to_excel(path_to_save_output+"fixed_agent_name_proposed_"+iteration_name+"_"+today+".xlsx",index=None)

    
    list_to_fill_for_labels_2 = []
    for i in range(len(G)):
        perct_share = empty_df_to_fill_trial.loc[empty_df_to_fill_trial["agent"]==i]["name_offered"].value_counts(normalize=True).to_frame()
        perct_share["name_index"] = perct_share.index.tolist()
        xx = perct_share.head(1)["name_index"][0]
        list_to_fill_for_labels_2.append(xx)
        
    
    selected_norms = list(set(list_to_fill_for_labels_2))
    
    fig,ax = plt.subplots()
    data_for_trend_plot = norms_db_to_fill.loc[norms_db_to_fill['name'].isin(selected_norms)]
    data_for_trend_plot = data_for_trend_plot.reset_index(drop=True)
    for label,grp in data_for_trend_plot.groupby('name'):
        grp.plot(x='timeperiod',y='percent_count',ax=ax,label=label)
    ax.set_xlabel('Timeperiod')
    ax.set_ylabel('Count %')
    # plt.show()
    plt.savefig(path_to_save_output+"top_names_"+iteration_name+"_"+today+".png")
    plt.clf()
    
    names_to_check = list(np.unique(empty_df_to_fill_trial['name_offered']))
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF),range(n)))
    list_of_colors = get_colors(len(names_to_check))
    
    perct_share_temp=empty_df_to_fill_trial.copy()
    list_to_fill_for_labels = []
    for i in range(len(G)):
        perct_share = perct_share_temp.loc[perct_share_temp["agent"]==i]["name_offered"].value_counts(normalize=True).to_frame()
        perct_share["name_index"] = perct_share.index.tolist()
        xx = perct_share.head(1)["name_index"][0]
        list_to_fill_for_labels.append(xx)
      
    
    color_map = []
    for j in range(len(list_to_fill_for_labels)):
        for i in range(len(names_to_check)):
            if list_to_fill_for_labels[j] == names_to_check[i]:
                color_map.append(list_of_colors[i])
                
    
    nx.draw(G,with_labels=True,node_color=color_map)
    l,r = plt.xlim()
    plt.xlim(l-0.05,r+0.05)
    plt.savefig(path_to_save_output+"network_after_"+str(num_of_trials)+'_timeperiods_'+iteration_name+"_"+today+".png")
    plt.clf()
    
    empty_df_to_fill_trial.to_excel(path_to_save_output+"aggregate_data_detailed_agent_"+iteration_name+"_"+today+".xlsx",index=None)
    
    parameters_pd = pd.DataFrame([{'iteration_name':iteration_name,'path_to_save_output':path_to_save_output,
                  'datetime':today,'num_neighbors':num_neighbors,'num_agents':num_agents,
                  'prob_edge_rewire':prob_edge_rewire,'grid_network_m':grid_network_m,
                  'grid_network_n':grid_network_n,'name_len':name_len,
                  'num_of_trials':num_of_trials,'fixed_agents':str(fixed_agents),'prob_new_name':prob_new_name,
                   'perturb_ratio':perturb_ratio,'network_name':network_name,'random_seed':random_seed,
                  'function_to_use':function_to_use,'norms_agents_frequency':norms_agents_frequency,
                   'norms_time_frequency':norms_time_frequency}]).T
    parameters_pd.columns=["parameter_values"]
    parameters_pd["parameter"]=parameters_pd.index
    parameters_pd[["parameter","parameter_values"]].to_excel(path_to_save_output+"parameters_"+iteration_name+"_"+today+".xlsx",index=None)


    return(print("done"))