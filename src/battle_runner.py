import run_webdriver

class BattleResult:
  def __init__(self, level, victory=False, fled=False, defeat=False):
    self.victory = victory
    self.fled = fled
    self.defeat = defeat
    self.level = level

def run_battle(d):
  if d.is_battle_start_screen():
    d.battle_start()
  enemy_level = d.battle_enemy_level()
  
  while True:
    if d.is_battle_victory_screen():
      d.battle_victory_resolve()
      return BattleResult(enemy_level, victory=True)
    if d.is_battle_defeat_screen():
      d.battle_defeat_resolve()
      return BattleResult(enemy_level, defeat=True)
    d.battle_action_attack()
