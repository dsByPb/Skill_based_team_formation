

def tfs(l_graph, l_task, hops, lmbda):  # twice of average degree
    """
    return community based team formation using closest expert.
    :param l_graph:
    :param l_task:
    :return:
    """
    import random
    from Teamr import Teamr
    from tqdm import tqdm
    import utilities
    import networkx as nx
    avg_degree = (2 * l_graph.number_of_edges()) / float(l_graph.number_of_nodes())
    hc = sorted([n for n, d in l_graph.degree() if len(l_graph.nodes[n]) > 0 and
                 d >= lmbda * avg_degree and
                 len(set(l_graph.nodes[n]["skills"].split(",")).intersection(set(l_task))) > 0],
                reverse=True)
    best_team = Teamr()
    best_ldr_distance = 1000
    # expert_skills = utilities.get_expert_skills_dict(l_graph)
    skill_experts = utilities.get_skill_experts_dict(l_graph)
    # print(hc)
    for c_node in tqdm(hc, total=len(hc)):
        task_copy = set(l_task)
        # hops = 2
        random_experts = set()
        team = Teamr()
        # while hops < 3 and len(task_copy) > 0:
        team.clean_it()
        for skill in l_task:
            team.task.add(skill)
        task_copy.update(l_task)
        team.leader = c_node
        skill_cover = set(task_copy).intersection(
            set(l_graph.nodes[team.leader]["skills"].split(",")))  # expert skills matched with l_task
        team.experts.add(c_node)
        if len(skill_cover) > 0:
            if c_node in team.expert_skills:
                for skill in skill_cover:
                    team.expert_skills[c_node].append(skill)
            else:
                team.expert_skills[c_node] = list()
                for skill in skill_cover:
                    team.expert_skills[c_node].append(skill)
        task_copy.difference_update(skill_cover)
        hop_nodes = utilities.within_k_nbrs(l_graph, c_node, hops)
        nbrhd = []
        # team.clean_it()
        # for skill in l_task:
        #     team.task.add(skill)
        # task_copy.update(l_task)
        # team.leader = c_node
        for node in hop_nodes:
            if len(l_graph.nodes[node])>0:
                skills = set(l_graph.nodes[node]["skills"].split(",")).intersection(task_copy)
                if len(skills) > 0:
                    dis = nx.dijkstra_path_length(l_graph, c_node, node, weight="cc")
                    nbrhd.append([node, skills, dis])
                    # nbrhd.append([node, skills])
        nbrhd.sort(key=lambda elem: (-len(elem[1]), elem[2]))  # sort neighbor hood max skills and min distance
        for nbr in nbrhd:
            if len(nbr[1].intersection(task_copy)) > 0:
                team.experts.add(nbr[0])
                team.expert_skills[nbr[0]] = nbr[1].intersection(task_copy)
                task_copy.difference_update(nbr[1].intersection(task_copy))
        tsk_lst = list(task_copy)
        while len(tsk_lst) > 0:
            skl = random.choice(tsk_lst)
            min_dis = 100
            close_expert = ""
            for expert in skill_experts[skl]:
                if nx.has_path(l_graph, team.leader, expert):
                    dis = nx.dijkstra_path_length(l_graph, team.leader, expert, weight="cc")
                    if min_dis > dis:
                        min_dis = dis
                        close_expert = (expert + ".")[:-1]
            team.experts.add(close_expert)  # first element of neighbor hood
            if close_expert not in team.expert_skills:
                team.expert_skills[close_expert] = list()
                team.expert_skills[close_expert].append(skl)
            else:
                team.expert_skills[close_expert].append(skl)
            tsk_lst.remove(skl)
            random_experts.add(close_expert)
            team.random_experts = random_experts
        if team.is_formed():
            ld = team.leader_skill_distance(l_graph, l_task)
            if best_ldr_distance > ld:
                best_ldr_distance = ld
                best_team = team
    return best_team, best_ldr_distance

def tfr(l_graph, l_task, hops, lmbda):  # twice of average degree
    """
    return community based team formation using closest expert.
    :param l_graph:
    :param l_task:
    :return:
    """
    import random
    from Team import Team
    import utilities
    from tqdm import tqdm
    import networkx as nx
    avg_degree = (2 * l_graph.number_of_edges()) / float(l_graph.number_of_nodes())
    hc = sorted([n for n, d in l_graph.degree() if len(l_graph.nodes[n]) > 0 and
                 d >= lmbda * avg_degree and
                 len(set(l_graph.nodes[n]["skills"].split(",")).intersection(set(l_task))) > 0],
                reverse=True)
    best_team = Team()
    best_ldr_distance = 1000
    # expert_skills = utilities.get_expert_skills_dict(l_graph)
    skill_experts = utilities.get_skill_experts_dict(l_graph)
    # print(hc)
    for c_node in tqdm(hc, total=len(hc)):
        task_copy = set(l_task)
        # hops = 2
        random_experts = set()
        team = Team()
        # while hops < 3 and len(task_copy) > 0:
        team.clean_it()
        for skill in l_task:
            team.task.add(skill)
        task_copy.update(l_task)
        team.leader = c_node
        skill_cover = set(task_copy).intersection(
            set(l_graph.nodes[team.leader]["skills"].split(",")))  # expert skills matched with l_task
        team.experts.add(c_node)
        if len(skill_cover) > 0:
            if c_node in team.expert_skills:
                for skill in skill_cover:
                    team.expert_skills[c_node].append(skill)
            else:
                team.expert_skills[c_node] = list()
                for skill in skill_cover:
                    team.expert_skills[c_node].append(skill)
        task_copy.difference_update(skill_cover)
        hop_nodes = utilities.within_k_nbrs(l_graph, c_node, hops)
        nbrhd = []
        team.clean_it()
        for skill in l_task:
            team.task.add(skill)
        task_copy.update(l_task)
        team.leader = c_node
        for node in hop_nodes:
            if len(l_graph.nodes[node])>0:
                skills = set(l_graph.nodes[node]["skills"].split(",")).intersection(task_copy)
                if len(skills) > 0:
                    dis = nx.dijkstra_path_length(l_graph, c_node, node, weight="cc")
                    nbrhd.append([node, skills, dis])
                    # nbrhd.append([node, skills])
        nbrhd.sort(key=lambda elem: (-len(elem[1]), elem[2]))  # sort neighbor hood max skills and min distance
        for nbr in nbrhd:
            if len(nbr[1].intersection(task_copy)) > 0:
                team.experts.add(nbr[0])
                team.expert_skills[nbr[0]] = nbr[1].intersection(task_copy)
                task_copy.difference_update(nbr[1].intersection(task_copy))
        tsk_lst = list(task_copy)
        while len(tsk_lst) > 0:
            skl = random.choice(tsk_lst)
            random_expert = random.choice(skill_experts[skl])
            team.experts.add(random_expert)
            if random_expert not in team.expert_skills:
                team.expert_skills[random_expert] = list()
                team.expert_skills[random_expert].append(skl)
            else:
                team.expert_skills[random_expert].append(skl)
            tsk_lst.remove(skl)
            random_experts.add(random_expert)
            team.random_experts = random_experts
        if team.is_formed():
            ld = team.leader_skill_distance(l_graph, l_task)
            if best_ldr_distance > ld:
                best_ldr_distance = ld
                best_team = team
    return best_team


def best_leader_distance(l_graph, l_task):
    """
    returns team of experts with minimum leader distance
    :param l_graph:
    :param l_task:
    :return Team :
    """
    import utilities
    import networkx as nx
    from Team import Team
    from tqdm import tqdm
    l_skill_expert = utilities.get_skill_experts_dict(l_graph)
    ldr_distance = 1000
    best_team = Team()
    import math
    avg_degree = (2 * l_graph.number_of_edges()) / float(l_graph.number_of_nodes())
    hc = sorted([n for n, d in l_graph.degree() if len(l_graph.nodes[n]) > 0 and
                 d >= 1 * avg_degree and
                 len(set(l_graph.nodes[n]["skills"].split(",")).intersection(set(l_task))) > 0],
                reverse=True)
    for candidate in tqdm(hc, total=len(hc)):
        team = Team()
        for skill in l_task:
            team.task.add(skill)
        team.leader = candidate
        team.experts.add(candidate)
        skill_cover = set()
        if len(l_graph.nodes[team.leader])>0:
            skill_cover = set(l_task).intersection(
                set(l_graph.nodes[team.leader]["skills"].split(",")))  # expert skills matched with l_task
            for skill in skill_cover:
                if candidate in team.expert_skills:
                    team.expert_skills[candidate].append(skill)
                else:
                    team.expert_skills[candidate] = list()
                    team.expert_skills[candidate].append(skill)
        r_skills = set(l_task).difference(skill_cover)
        for skill in r_skills:
            min_dis = 100
            closest_expert = ""
            for expert in l_skill_expert[skill]:
                if nx.has_path(l_graph, candidate, expert):
                    dis = nx.dijkstra_path_length(l_graph, candidate, expert, weight="cc")
                    if min_dis > dis:
                        min_dis = dis
                        closest_expert = (expert + ".")[:-1]
            if len(closest_expert) > 0:
                team.experts.add(closest_expert)
                if closest_expert not in team.expert_skills:
                    team.expert_skills[closest_expert] = list()
                    team.expert_skills[closest_expert].append(skill)
                else:
                    team.expert_skills[closest_expert].append(skill)
        # print(team)
        if team.is_formed():
            cld = team.leader_skill_distance(l_graph, l_task)
            if ldr_distance > cld:
                ldr_distance = cld
                best_team = team
    return best_team
