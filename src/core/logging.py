import json
import logging
from datetime import datetime

from rich.logging import RichHandler


# Custom formatter to handle JSON messages
class CustomRichFormatter(logging.Formatter):
    def format(self, record):
        try:
            # Attempt to parse the message as JSON
            message = record.getMessage()
            if isinstance(message, str):
                try:
                    message = json.loads(message)  # Try parsing if it's a JSON string
                except json.JSONDecodeError:
                    pass

            # If message is a dict and has a 'payload' field that’s also JSON, parse it
            if isinstance(message, dict) and "payload" in message:
                try:
                    message["payload"] = json.loads(message["payload"])
                except (json.JSONDecodeError, TypeError):
                    pass

            if isinstance(message, (dict, list)):
                pretty_message = json.dumps(message, indent=4)  # Format JSON nicely
            else:
                pretty_message = str(message)

        except Exception as e:
            pretty_message = f"Error formatting log: {e}"

        record.pretty_message = pretty_message
        record.asctime = datetime.fromtimestamp(record.created).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        record.filename = record.pathname.split("/")[-1]

        return f"[{record.asctime}] {record.filename}:{record.funcName}:{record.lineno} - {pretty_message}"


# Function to set up logging
def setup_logging(level=logging.INFO):
    rich_handler = RichHandler(show_time=False, show_path=False, rich_tracebacks=False)
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[rich_handler],
    )
    formatter = CustomRichFormatter()

    # Apply RichHandler to all loggers
    for logger_name in logging.root.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        logger.handlers = [rich_handler]
        logger.handlers[0].setFormatter(formatter)
        logger.propagate = False
