import os
from dotenv import load_dotenv

load_dotenv()

QUERY_BALANCER_HOST = os.getenv("QUERY_BALANCER_HOST")
ACTIVE_REPLICATOR_HOST = os.getenv("ACTIVE_REPLICATOR_HOST")
