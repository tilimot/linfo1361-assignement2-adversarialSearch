import random
import math
from fenix import *

class AgentMcts2:
    class Node:
        def __init__(self, parent_node, action_from_parent, state):
            self.parent_node = parent_node
            self.action_from_parent = action_from_parent
            self.state = state
            self.wins = 0
            self.visits = 0
            self.children = []

    def __init__(self, player, iterations=1000, search_parameter=math.sqrt(2)):
        self.player = player
        self.iterations = iterations
        self.search_parameter = search_parameter

    def mcts(self, state):
        if not state.actions():
            return random.choice(state.actions()) if state.actions() else None
        root = self.Node(None, None, state)
        for _ in range(self.iterations):
            leaf = self.select(root)
            child = self.expand(leaf)
            result = self.simulate(child)
            self.backpropagate(child, result)
        if not root.children:
            return random.choice(state.actions()) if state.actions() else None
        return max(root.children, key=lambda node: node.visits + self.strategic_bonus(node)).action_from_parent

    def UCB1(self, node):
        if node.visits == 0:
            return float('inf')
        
        win_by_visits = node.wins / node.visits
        
        C = self.search_parameter
        explore = C * math.sqrt(math.log(node.parent_node.visits + 1) / (node.visits + 1))
        strategic_bonus = self.strategic_bonus(node)
        
        return win_by_visits + explore + strategic_bonus
    
    def strategic_bonus(self, node):
        if not node.action_from_parent:
            return 0
            
        bonus = 0
        action = node.action_from_parent
        state = node.state
        
        # Block adversary
        adversary = -state.current_player
        for direction_i, direction_j in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            potential_pos = (action.end[0] + direction_i, action.end[1] + direction_j)
            if self._is_inside(state, potential_pos) and state.pieces.get(potential_pos, 0) == adversary:
                bonus += 10
                break
            
        if len(action.removed) > 0:
            bonus += 8
            
        if any(abs(state.pieces.get(piece, 0)) == 2 for piece in action.removed):
            bonus += 15
            
        for direction_i, direction_j in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            potential_pos = (action.end[0] + direction_i, action.end[1] + direction_j)
            if self._is_inside(state, potential_pos) and state.pieces.get(potential_pos, 0) == adversary:
                bonus += 20
                break
                
        return bonus

    def _is_inside(self, state, position):
        return 0 <= position[0] < state.dim[0] and 0 <= position[1] < state.dim[1]

    def select(self, node):
        while node.children and node.state and not node.state.is_terminal():
            node = max((child for child in node.children if not child.state.is_terminal()), key=self.UCB1, default=None)
            if not node:
                break
        return node

    def expand(self, node):
        if node.state.is_terminal() or node.children:
            return node
        for action in node.state.actions():
            action_res = node.state.result(action)
            if not action_res.is_terminal():
                new_node_child = self.Node(node, action, action_res)
                node.children.append(new_node_child)
        if node.children:
            return node.children[0]
        return node

    def simulate(self, node):
        actual_state = node.state
        if actual_state.is_terminal():
            return actual_state.utility(-node.state.to_move())
        
        while not actual_state.is_terminal():
            possible_actions = actual_state.actions()
            if not possible_actions:
                break
            
            best_action = None
            max_bonus = -float('inf')
            
            for action in possible_actions:
                bonus = self.strategic_bonus(node)
                if bonus > max_bonus:
                    max_bonus = bonus
                    best_action = action
            

            actual_state = actual_state.result(best_action)            
        return actual_state.utility(-node.state.to_move()) if actual_state.is_terminal() else 0


    def backpropagate(self, node, result):
        node.visits += 1
        if result == 1: 
            node.wins += 1
        if node.parent_node is not None:
            self.backpropagate(node.parent_node, -result)

    def act(self, state, remaining_time):
        action = self.mcts(state)
        return action
    
    def get_action(self, state, remaining_time):
        return self.act(state, remaining_time)