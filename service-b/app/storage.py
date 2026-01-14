import json
import os

import redis.asyncio as redis

from shared.schemas import IpToCoordinates

INDEX_KEY = "index:all_ips"

r = redis.Redis(
    host=os.getenv("REDIS_HOST", 'localhost'),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)


async def save_location(data: IpToCoordinates):
    try:
        key = f"geo:{data.ip}"
        json_value = data.model_dump_json(include={"coord"})

        pipe = r.pipeline()
        await pipe.set(key, json_value)
        await pipe.sadd(INDEX_KEY, str(data.ip))
        await pipe.execute()
        return True
    except Exception as e:
        print(f"Error saving: {e}")
        return False


async def get_location_by_ip(ip_address: str) -> IpToCoordinates | None:
    key = f"geo:{ip_address}"
    try:
        raw_json = await r.get(key)
        if not raw_json:
            return None
        data_dict = json.loads(raw_json)
        if "ip" not in data_dict:
            data_dict["ip"] = ip_address
        return IpToCoordinates.model_validate(data_dict)
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None


async def get_all_locations() -> list[IpToCoordinates]:
    all_ips = await r.smembers(INDEX_KEY)
    if not all_ips:
        return []

    keys = [f"geo:{ip}" for ip in all_ips]
    json_values = await r.mget(keys)

    results = []
    for ip, raw_json in zip(all_ips, json_values):
        if raw_json:
            try:
                data_dict = json.loads(raw_json)
                data_dict["ip"] = ip
                obj = IpToCoordinates.model_validate(data_dict)
                results.append(obj)
            except Exception:
                continue
    return results
