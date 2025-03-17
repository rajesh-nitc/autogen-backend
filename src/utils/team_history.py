import json
import os
from typing import Any

import aiofiles

history_path = "team_history.json"


async def get_history() -> list[dict[str, Any]]:
    """Get chat history.

    :return: list[dict[str, Any]]
    """
    if not os.path.exists(history_path):
        return []
    async with aiofiles.open(history_path) as file:
        return json.loads(await file.read())
