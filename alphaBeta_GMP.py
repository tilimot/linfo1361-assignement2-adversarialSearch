from fenix import *

class Alpha_Beta_GMP:
    def __init__(self, player,depth = 1):
        self.player = player
        self.depth=depth
    
    def evaluate(self, state: FenixState, player: int) -> float:
        """
        Évalue un état de jeu du point de vue du joueur donné.

        Args:
            state (FenixState): L'état du jeu.
            player (int): Le joueur évalué (1 ou -1).

        Returns:
            float: Le score de l'état .
            
        This ef push Agent to prefer states where it has the most pieces in the game.
        """
        score = 0
        
        for pos, piece in state.pieces.items():
            # Count each Player piece and sum their value, count each adversary piece and substract their value. 
            if piece * player > 0:
                score += abs(piece)  # 1, 2 ou 3
            elif piece * player < 0:
                score -= abs(piece)

        return score

    
    def alpha_beta_search(self, state:FenixState):
        _, action = self.max_value(state, -float('inf'), float('inf'), self.depth)
        return action
    
    def max_value(self, state, alpha, beta, depth):
        if state.is_terminal():
            return state.utility(self.player)*1000, None
        elif depth == 0:
            return self.evaluate(state,self.player), None

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
        if state.is_terminal():
            return state.utility(self.player)*1000, None
        elif depth == 0:
            return self.evaluate(state,self.player), None

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
        action = self.alpha_beta_search(state)
        return action
