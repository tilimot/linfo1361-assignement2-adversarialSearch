class Agent:
    def __init__(self, player):
        self.player = player
    
    def alpha_beta_search(self, state, depth):
        _, action = self.max_value(state, -float('inf'), float('inf'), depth)
        return action
    
    def max_value(self, state, alpha, beta, depth):
        if state.is_terminal() or depth == 0:
            return state.utility(self.player), None

        value = -float('inf')
        action = None
        
        for a in state.actions():
            v, _ = self.min_value(state.result(a), alpha, beta, depth - 1)
            if v > value:
                value = v
                action = a
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Coupure alpha-beta

        return value, action
    
    def min_value(self, state, alpha, beta, depth):
        if state.is_terminal() or depth == 0:
            return state.utility(self.player), None

        value = float('inf')
        action = None
        
        for a in state.actions():
            v, _ = self.max_value(state.result(a), alpha, beta, depth - 1)
            if v < value:
                value = v
                action = a
            beta = min(beta, value)
            if alpha >= beta:
                break  # Coupure alpha-beta

        return value, action
    
    def act(self, state, remaining_time):
        action = self.alpha_beta_search(state, depth=3)
        return action
