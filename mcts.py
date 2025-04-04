class UCT:

    class Node:
        def __init__(self, parent_node, action_from_parent, state):
            self.parent_node = parent_node
            self.action_from_parent = action_from_parent
            self.state = state
            self.wins = 0
            self.visits = 0
            self.children = []

    def __init__(self, player, iterations=1000):
        self.player = player
        self.iterations = iterations

    def mcts(self, state):
        root = self.Node(None, None, state)
        for _ in range(self.iterations):
            leaf = self.select(root)
            child = self.expand(leaf)
            result = self.simulate(child)
            self.backpropagate(child, result)
        return max(root.children, key=lambda node: node.visits).action_from_parent

    def UCB1(self, node):
        if node.visits == 0:
            return float('inf')
        #win ratio by number of visits (formule).
        win_by_visits = node.wins / node.visits
        explore = math.sqrt(2 * math.log(node.parent_node.visits) / node.visits)
        return win_by_visits + explore


    def select(self, node):
        #last node
        if node.state.is_terminal() or not node.children:
            return node
        
        #select recursive child with best val
        best_child = max(node.children, key=lambda child: self.UCB1(child))
        return self.select(best_child)


    def expand(self, node):
        #last node
        if node.state.is_terminal() or node.children:
            return node
        #create all childs
        for action in node.state.actions():
            action_res = node.state.result(action)
            new_node_child = self.Node(node, action, action_res)
            node.children.append(new_node_child)
        #return new child (first).
        if node.children:
            return node.children[0]
        else:
        #no childs
            return node


    def simulate(self, node):
        actual_state = node.state
        #last node
        if actual_state.is_terminal():
            return actual_state.utility(-node.state.to_move())
        
        #random simu
        while not actual_state.is_terminal():
            action = random.choice(actual_state.actions())
            actual_state = actual_state.result(action)
        
        #result for parent
        return actual_state.utility(-node.state.to_move())


    def backpropagate(self, node, result):
        node.visits += 1
        if result == 1: node.wins += 1
        if node.parent_node != None:
            self.backpropagate(node.parent_node, -result)