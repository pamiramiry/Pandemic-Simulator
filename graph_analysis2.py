import networkx as nx
import json
import random


# Gets the time and previous infection count
# Increments each one if within the time
def increment_infection(x, infection_count):
    if x < 1000:
        infection_count[3] += 1
    if x < 2000:
        infection_count[6] += 1
    if x < 3000:
        infection_count[9] += 1
    if x < 4000:
        infection_count[12] += 1
    if x < 5000:
        infection_count[15] += 1
    if x < 6000:
        infection_count[18] += 1
    if x < 7000:
        infection_count[21] += 1
    return infection_count


# Does the cascading
# infected nodes dict is the infected node and how long has it been alive
# Cured nodes are nodes that have been recently cured and cant catch covid again
# immune nodes are nodes that have lost some of there immunity
# Dead nodes are nodes that are dead and have been removed from the graph
def cascade(g):
    infected_nodes = {}
    cured_nodes = {}
    immune_nodes = {}
    dead_nodes = []
    total_infected = 0
    # Infect the first few edges
    zero_edges = [(a, b) for a, b, attrs in g.edges(data=True) if attrs["weight"] == 0]
    infection_count = {1: 0, 3: 0, 6: 0, 9: 0, 12: 0, 15: 0, 18: 0, 21: 0}
    start_infected = 0
    for tuple in zero_edges:
        infected_nodes[tuple[0]] = 0
        total_infected += 1
        infection_count = increment_infection(0, infection_count)
        start_infected += 1
        print(tuple[0])
        if start_infected > 4:
            break
    # Loops through the year
    for x in range(0, 4000):
        # If the edge Interaction took place at the current time look at the nodes
        current_edges = [(a, b) for a, b, attrs in g.edges(data=True) if attrs["weight"] == x]
        for tuple in current_edges:
            # Check if the first node is infected
            # If so the infection spreads and is kept track off
            if tuple[0] not in cured_nodes and tuple[1] not in cured_nodes:
                if tuple[0] in infected_nodes:
                    if tuple[1] not in infected_nodes and tuple[0] in immune_nodes:
                        chance_of_infection = random.randint(0, 100)
                        if chance_of_infection < 14:
                            infected_nodes[tuple[1]] = 0
                            total_infected += 1
                            infection_count = increment_infection(x, infection_count)
                    elif tuple[1] not in infected_nodes and tuple[1] not in immune_nodes and tuple[1] \
                            not in cured_nodes:
                        chance_of_infection = random.randint(0, 100)
                        if chance_of_infection < 28:
                            infected_nodes[tuple[1]] = 0
                            total_infected += 1
                            infection_count = increment_infection(x, infection_count)
                    elif tuple[1] not in infected_nodes and tuple[1] in immune_nodes:
                        chance_of_infection = random.randint(0, 100)
                        if chance_of_infection < 14:
                            infected_nodes[tuple[1]] = 0
                            total_infected += 1
                            infection_count = increment_infection(x, infection_count)
                # Check if the second node is infected
                # If so the infection spreads and is kept track off
                elif tuple[1] in infected_nodes:
                    if tuple[0] not in infected_nodes and tuple[1] in immune_nodes:
                        chance_of_infection = random.randint(0, 100)
                        if chance_of_infection < 14:
                            infected_nodes[tuple[0]] = 0
                            total_infected += 1
                            infection_count = increment_infection(x, infection_count)
                    elif tuple[0] not in infected_nodes and tuple[0] not in immune_nodes and tuple[0] not in \
                            cured_nodes:
                        chance_of_infection = random.randint(0, 100)
                        if chance_of_infection < 28:
                            infected_nodes[tuple[0]] = 0
                            total_infected += 1
                            infection_count = increment_infection(x, infection_count)
                    elif tuple[0] not in infected_nodes and tuple[0] in immune_nodes:
                        chance_of_infection = random.randint(0, 100)
                        if chance_of_infection < 14:
                            infected_nodes[tuple[0]] = 0
                            total_infected += 1
                            infection_count = increment_infection(x, infection_count)

        # People in cured nodes only have a limited amount of immunity for approximately 1 month
        # After that they move into immune nodes which has lost some immunity
        for person in list(cured_nodes):
            cured_nodes[person] += 1
            if cured_nodes[person] >= 360:
                del cured_nodes[person]
                immune_nodes[person] = 0

        # Check all of the infected nodes
        # if its been infected for 14 days time to die or live
        # if dead remove from graph
        # If alive remove infected list and put into cured nodes
        for person in list(infected_nodes):
            infected_nodes[person] += 1
            if infected_nodes[person] >= 336:
                del infected_nodes[person]
                chance_of_dying = random.randint(0, 10000)
                if chance_of_dying < 5:
                    dead_nodes.append(person)
                    print("Died at"+str(x)+": " + person)
                    g.remove_node(person)
                else:
                    cured_nodes[person] = 0

    print("total_dead: " + str(len(dead_nodes)))
    print("total infected: " + str(total_infected))
    print("Total infected 3 months: " + str(infection_count[3]))
    print("Total infected 6 months: " + str(infection_count[6]))
    print("Total infected 9 months: " + str(infection_count[9]))
    print("Total infected 12 months: " + str(infection_count[12]))
    print("Total infected 15 months: " + str(infection_count[15]))
    print("Total infected 18 months: " + str(infection_count[18]))
    print("Total infected 21 months: " + str(infection_count[21]))
    # print(len(cured_nodes))
    # print(len(immune_nodes))


# Remove the Person in the network with the highest Page Rank score
def remove_page_rank(g):
    with open("page_rank_scores.json", "r") as file:
        node_dict = json.load(file)
        ordered_node = sorted(node_dict.items(), key=lambda x: x[1], reverse=True)[:200]
        print(ordered_node)
        for node in ordered_node:
            g.remove_node(node[0])
        print(g.number_of_nodes())
    cascade(g)


# Calculates the Page rank for every time=0,1,2 in the graph
# Then puts it into json file to read later
# I put it in a json file because the graph remains the same
# and running it each time takes a long time
def pagerank_filter(g):
    print("WELCOME TO PAGERANK")
    total_page_score = {}
    for x in range(0, 4000):
        current_edges = [(a, b) for a, b, attrs in g.edges(data=True) if attrs["weight"] == x]
        subg = nx.empty_graph(create_using=nx.MultiGraph())
        subg.add_edges_from(current_edges)
        current_scores = nx.pagerank(subg)
        for node in current_scores:
            if node in total_page_score:
                total_page_score[node] += current_scores[node]
            elif node not in total_page_score:
                total_page_score[node] = current_scores[node]

    with open("page_rank_scores.json", "w") as file:
        json.dump(total_page_score, file)
    print("pr: " + str(sorted(total_page_score.items(), key=lambda x: x[1], reverse=True)[:50]))


# This removes random a nodes from the graph
# Null model
def remove_node_randomly(g):
    list_nodes = list(g.nodes())
    list_removal = random.sample(list_nodes, 100)
    for node in list_removal:
        g.remove_node(node)
    cascade(g)


# This removes random edges from the graph
# Null model
def remove_edge_randomly(g):
    list_edges = list(g.edges())
    list_removal = random.sample(list_edges, 10000)
    for e in list_removal:
        g.remove_edge(e[0], e[1])
    print(g.number_of_edges())
    cascade(g)


# calculates the edge betweeness scores for every hour
# Then removes the top one for each hour
def edge_b_remove(g):
    print("WELCOME TO edge betweeness filter")
    edge_scores = {}
    for x in range(0, 4000):
        current_edges = [(a, b) for a, b, attrs in g.edges(data=True) if attrs["weight"] == x]
        subg = nx.empty_graph(create_using=nx.MultiGraph())
        subg.add_edges_from(current_edges)
        current_scores = nx.edge_betweenness_centrality(subg)
        ordered = sorted(current_scores.items(), key=lambda x: x[1], reverse=True)[:10]
        #print(ordered)
        g.remove_edge(ordered[0][0][0], ordered[0][0][1])
        g.remove_edge(ordered[1][0][0], ordered[1][0][1])

    print(g.number_of_edges())


# Demo
# Don't worry about this
# DID not use
def edge_temporal_filter(g):
    print("WELCOME TO edge betweeness filteer")
    edge_scores = {}
    for x in range(0, 4000):
        current_edges = [(a, b) for a, b, attrs in g.edges(data=True) if attrs["weight"] == x]
        # g.remove_edge(current_edges[0][0], current_edges[0][1])
        # print("len of edges" + str(len(current_edges)))
        subg = nx.empty_graph(create_using=nx.MultiGraph())
        subg.add_edges_from(current_edges)
        # print("sub nodes:" + str(subg.number_of_nodes()))
        # print(nx.number_connected_components(subg))
        # print(nx.is_connected(subg))
        # current_scores = nx.pagerank(subg)
        current_scores = nx.edge_betweenness_centrality(subg)
        # print(current_scores)
        # print(current_scores)
        for edge in current_scores:
            if edge in edge_scores:
                edge_scores[edge] += current_scores[edge]
            elif edge not in edge_scores:
                edge_scores[edge] = current_scores[edge]

    with open("edge_scores.json", "w") as file:
        json.dump(edge_scores, file)

    print("pr: " + str(sorted(edge_scores.items(), key=lambda x: x[1], reverse=True)[:50]))
    print("DOOOOOOOOOOOOOOOOOONE")


# Create network
graph = nx.read_weighted_edgelist("edge_list_2year.txt", create_using=nx.MultiGraph())
# Random stats for testing purposes
# print(graph.number_of_nodes())
# print(nx.number_connected_components(graph))
# print(nx.is_connected(graph))
# print(graph.number_of_edges())


# Toggle the comments to run the desired cascade
cascade(graph)
# edge_b_remove(graph)
# edge_temporal_filter(graph)
# remove_edge_randomly(graph)
# pagerank_filter(graph)
# remove_page_rank(graph)
# remove_node_randomly(graph)
