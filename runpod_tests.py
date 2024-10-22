import runpod
from src.filesystem.filesystem_manager import FilesystemManager
from src.requests.requests_manager import RequestsManager
key = FilesystemManager().load_runpod_secret_key()
runpod.api_key = key
pods = runpod.get_pods()
print(RequestsManager().get_xtts_endpoint())
