from datetime import date
from redis import Redis
import json


class CacheService:
    def __init__(self, client: Redis):
        self.client = client

    def delete_posts_cache(self, key: str):
        self.client.delete(key)

    def cache_posts(self, posts, expire: int = 300):
        self.client.setex("posts", expire, json.dumps(posts))

    def get_cached_posts(self):
        cached = self.client.get("posts")
        return json.loads(cached) if cached else None

    def cache_post(self, post_id: int, post, expire: int = 300):
        self.client.setex(f"post:{post_id}", expire, json.dumps(post))

    def get_cached_post(self, post_id: int):
        cached = self.client.get(f"post:{post_id}")
        return json.loads(cached) if cached else None

    def increment_post_stat(self, key: str):
        today = date.today().isoformat()
        self.client.incr(f'{key}{today}')

    def get_post_stats(self):
        keys = self.client.keys("post_create:*")
        stats = {}
        for key in keys:
            count = int(self.client.get(key))
            day = key.split(":")[1]
            stats[day] = count
        return stats