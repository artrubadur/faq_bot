from yandex_cloud_ml_sdk import AsyncYCloudML

from app.core.config import config

sdk = AsyncYCloudML(
    folder_id=config.yc_folder_id,
    auth=config.yc_api_key,
)
