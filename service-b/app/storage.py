import json
import os

import redis

from schemas import IpToCoordinates

INDEX_KEY = "index:all_ips"

r = redis.Redis(
    host=os.getenv("REDIS_HOST", 'localhost'),
    port=os.getenv("REDIS_POTT", 6379),
    db=0,
    decode_responses=True)


def save_location(data: IpToCoordinates):
    try:
        key = f"geo:{data.ip}"
        json_value = data.model_dump_json(include={"coord"})
        pipe = r.pipeline()
        pipe.set(key, json_value)
        pipe.sadd(INDEX_KEY, str(data.ip))
        pipe.execute()
        return True
    except Exception as e:
        return False


def get_location_by_ip(ip_address: str) -> IpToCoordinates | None:
    key = f"geo:{ip_address}"
    raw_json = r.get(key)
    if not raw_json:
        return None
    try:
        data_dict = json.loads(raw_json)
        data_dict["ip"] = ip_address
        print(data_dict)
        obj = IpToCoordinates.model_validate(data_dict)
        return obj
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None


def get_all_locations() -> list[IpToCoordinates]:
    all_ips = r.smembers(INDEX_KEY)
    if not all_ips:
        return []
    keys = [f"geo:{ip}" for ip in all_ips]
    json_values = r.mget(keys)
    results = []
    for ip, raw_json in zip(all_ips, json_values):
        if raw_json:
            try:
                data_dict = json.loads(raw_json)
                data_dict["ip"] = ip
                obj = IpToCoordinates.model_validate(data_dict)
                results.append(obj)
            except Exception as e:
                print(f"Error parsing IP {ip}: {e}")
    return results
