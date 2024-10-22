import logging
import time
from typing import Optional, Any
import requests
import runpod
from src.base.constants import XTTS_CONFIG_FILE
from src.filesystem.filesystem_manager import FilesystemManager
logger = logging.getLogger(__name__)


class RequestsManager:

    def __init__(self, filesystem_manager: Optional[FilesystemManager] = None,
                 max_retries: int = 5, retry_delay: float = 2.0):
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._xtts_data = (self._filesystem_manager.
                           load_existing_or_new_json_file(XTTS_CONFIG_FILE))

    def _get_pod_url(self) -> Optional[str]:
        runpod.api_key = self._filesystem_manager.load_runpod_secret_key()
        try:
            pods = runpod.get_pods()
        except Exception as e:
            logger.error(f'Failed to fetch pods: {e}')
            return None
        if not pods:
            return None
        for pod in pods:
            pod_id = pod.get('id')
            desired_status = pod.get('desiredStatus', '').lower()
            if pod_id and desired_status == 'running':
                endpoint_url = f'https://{pod_id}-8020.proxy.runpod.net'
                return endpoint_url
            else:
                logger.warning(f'Pod {pod_id} is not running: {pod}')
        logger.warning('No running pods found.')
        return None

    def _is_pod_ready(self) -> bool:
        pod_url = self._get_pod_url()
        if not pod_url:
            return False
        xtts_set_tts_settings = f'{pod_url}/set_tts_settings'
        try:
            response = requests.post(xtts_set_tts_settings, json=self.
                                     _xtts_data)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            logger.error("Couldn't set TTS settings. %s", err)
            if 'Connection aborted' in err.__str__():
                return False
        return True

    def _wait_for_pod_ready(self) -> bool:
        for attempt in range(1, self.max_retries + 1):
            if self._is_pod_ready():
                return True
            logger.info(
                f'Retrying health check ({attempt}/{self.max_retries}) after {self.retry_delay} seconds...'
            )
            time.sleep(self.retry_delay)
        logger.error('Pod did not become ready in time.')
        return False

    def get_available_speakers(self) -> dict[str, Any]:
        try:
            if not self._wait_for_pod_ready():
                logger.error('Pod is not ready to handle requests.')
                return {}
            speakers_endpoint = f'{self._get_pod_url()}/speakers_list'
            response_speakers = requests.get(speakers_endpoint)
            if response_speakers.status_code == 200:
                all_speakers = response_speakers.json()
                current_language_speakers = all_speakers.get('en', {}).get(
                    'speakers', [])
                return current_language_speakers
            else:
                logger.warning(
                    f'Failed to fetch speakers list. Status code: {response_speakers.status_code}'
                )
                return {}
        except requests.exceptions.ConnectionError as e:
            logger.warning(f'Connection error while fetching speakers: {e}')
            return {}
        except Exception as e:
            logger.error(f'Unexpected error in get_available_speakers: {e}')
            return {}

    def get_xtts_endpoint(self) -> Optional[str]:
        try:
            if not self._wait_for_pod_ready():
                logger.error('Pod is not ready to handle TTS requests.')
                return None
            tts_endpoint = f'{self._get_pod_url()}/tts_to_audio/'
            logger.info(f'TTS endpoint is ready: {tts_endpoint}')
            return tts_endpoint
        except Exception as e:
            logger.error(f'Unexpected error in get_xtts_endpoint: {e}')
            return None
