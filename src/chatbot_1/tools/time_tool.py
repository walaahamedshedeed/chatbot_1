from datetime import datetime
from typing import Dict, Any
from crewai.tools import BaseTool

class TimeTool(BaseTool):
    name: str = "Time Tool"
    description: str = "Get the current date and time"

    def _run(self, args: Dict[str, Any] = None) -> str:
        current_time = datetime.now()
        return current_time.strftime("%Y-%m-%d %H:%M:%S")