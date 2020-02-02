def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    start = problem.getStartState()
    allNode = []
    allNode.append(node(start, [], 0, heuristic(start, problem)))
    start = allNode[0]
    marked_ = []

    def cur_aStarSearch(point, cost, marked_):
        pos = point.state
        marked_.append(pos)#marked
        
        if problem.isGoalState(pos):           
            return point.res
        print(pos)
        suc = problem.getSuccessors(pos)
        for sta in suc:
            pos_ = sta[0]
            cost_ = sta[2] + cost  # total cost
            if pos_ not in marked_:
                res_ = []
                res_ = list(point.res)
                res_.append(sta[1])
                point_ = node(pos_, res_, cost_,
                            cost_ + heuristic(pos_, problem))
                existed = False
                for m in allNode:
                    if point_.state == m.state:
                        existed = True
                        if point_.f < m.f:
                            m.res = list(point_.res)
                            m.cost = point_.cost
                            m.f = point_.f
                if not existed:
                    allNode.append(point_)


        min = 10000
        next_node = []
        end = True
        for m in allNode:
            position = m.state
            if position not in marked_:
                if m.f < min:
                    end = False
                    min = m.f
                    next_node = node(m.state, m.res, m.cost, m.f)
        if not end:
            return cur_aStarSearch(next_node, next_node.cost, marked_)#can not pass res
    all_res = []
    all_res = list(cur_aStarSearch(start, 0, marked_))
    print(all_res)
    return all_res
    util.raiseNotDefined()