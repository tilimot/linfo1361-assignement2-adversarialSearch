from visual_game_manager import *

#agent = Agent()
red = Agent(1)
black = RandomAgent(-1)
vg = VisualGameManager(red_agent=red,black_agent=black)
vg.play()