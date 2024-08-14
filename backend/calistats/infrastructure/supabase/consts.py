import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

USERS_TABLE = "users"
STATS_TABLE = "stats"
STAT_TYPES_TABLE = "stat_types"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
