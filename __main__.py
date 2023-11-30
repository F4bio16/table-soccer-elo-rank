"""Init project file for the ELO rating system applied on custom scenarios"""
import os
from dotenv import load_dotenv

from services.game_service import GameService
from services.rank_service import RankService
from repositories.sqlite_repo import SQLiteRepository
from models.player import Teams

print("Initializing application ELO Rating System")

# loading environment variables
load_dotenv()

rank_service = RankService(int(os.getenv("ELO_MULTIPLIER_FACTOR")))
repo = SQLiteRepository({"DB_NAME": os.getenv("DB_NAME")})
repo.connect()

game_service = GameService(repo, rank_service)

players = [
  repo.get_player(1, Teams.RED.value),
  repo.get_player(2, Teams.RED.value),
  repo.get_player(5, Teams.BLUE.value),
  repo.get_player(6, Teams.BLUE.value)
]

match = game_service.game_start(players)
print(f"""
  Created game ID {match.game_id}
  {" --- ".join([f"ID#{player.id} {player.name} {player.rank_score} {player.team}" for player in players])}

  Expected result:
    RED wins for {match.get_expected_score(Teams.RED.value) * 100} % ({match.get_team_points(Teams.RED.value)} points)
    BLUE wins for {match.get_expected_score(Teams.BLUE.value) * 100} % ({match.get_team_points(Teams.BLUE.value)} points)
  """)

updated_players = game_service.game_end(match, 6, 0)

print(f"Game {match.game_id} ended")
for player in updated_players:
    print(f"  - Player #{player.id} Score: {player.rank_score}")
