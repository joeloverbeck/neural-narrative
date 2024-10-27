import runpod

from src.filesystem.config_loader import ConfigLoader
from src.requests.requests_manager import RequestsManager

key = ConfigLoader().load_runpod_secret_key()
runpod.api_key = key
pods = runpod.get_pods()
print(RequestsManager().get_xtts_endpoint())
