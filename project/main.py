from util.base import DungeonMaster, Player

def main():
  dm = DungeonMaster()
  player = Player("Max")
  player.connect()
  dm.start_server()

  print("Connecting player...")/quit
  
if __name__ == "__main__":
  main()