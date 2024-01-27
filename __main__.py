"""Init project file for the ELO rating system applied on custom scenarios"""
import os
from dotenv import load_dotenv

from services.game_service import GameService
from services.rank_service import RankService
from services.http_web_service import HttpWebService
from repositories.sqlite_repo import SQLiteRepository

print("Initializing application ELO Rating System")

# loading environment variables
load_dotenv()

rank_service = RankService(
  int(os.getenv("ELO_MULTIPLIER_FACTOR")),
  {
    'bonus': int(os.getenv("ELO_HUMILIATION_BONUS")),
    'malus': int(os.getenv("ELO_HUMILIATION_MALUS"))
  }
)

repo = SQLiteRepository({"DB_NAME": os.getenv("DB_NAME")})
repo.connect()

game_service = GameService(repo, rank_service)

http_service = HttpWebService(repo, game_service)
http_service.start(5000)
