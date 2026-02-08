import json
import traceback


def serialize_json(record):
    payload = {
        "time": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "name": record["name"],
    }
    exception = record["exception"]
    if exception:
        payload["error"] = "".join(
            traceback.format_exception(
                exception.type, exception.value, exception.traceback
            )
        )

    return f"{{{json.dumps(payload, ensure_ascii=False)}}}\n"
