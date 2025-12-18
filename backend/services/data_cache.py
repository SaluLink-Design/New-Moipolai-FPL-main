"""
Redis Cache Manager - Handles caching of FPL data
"""
import redis.asyncio as redis
import json
import logging
from typing import Optional, Any
from datetime import timedelta
from config import settings

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages Redis cache operations."""
    
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        
    async def connect(self):
        """Connect to Redis."""
        try:
            self.redis = await redis.from_url(
                f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
                password=settings.redis_password if settings.redis_password else None,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            # Continue without cache
            self.redis = None
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.redis:
            await self.redis.close()
            logger.info("Redis connection closed")
    
    async def ping(self) -> bool:
        """Check if Redis is available."""
        if not self.redis:
            return False
        try:
            await self.redis.ping()
            return True
        except Exception:
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if not self.redis:
            return None
        
        try:
            value = await self.redis.get(key)
            if value:
                logger.debug(f"Cache hit: {key}")
                return json.loads(value)
            logger.debug(f"Cache miss: {key}")
            return None
        except Exception as e:
            logger.error(f"Cache get error for {key}: {e}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (optional)
            
        Returns:
            True if successful
        """
        if not self.redis:
            return False
        
        try:
            serialized = json.dumps(value)
            if ttl:
                await self.redis.setex(key, ttl, serialized)
            else:
                await self.redis.set(key, serialized)
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set error for {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Delete value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        if not self.redis:
            return False
        
        try:
            await self.redis.delete(key)
            logger.debug(f"Cache delete: {key}")
            return True
        except Exception as e:
            logger.error(f"Cache delete error for {key}: {e}")
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching a pattern.
        
        Args:
            pattern: Key pattern (e.g., "fpl:*")
            
        Returns:
            Number of keys deleted
        """
        if not self.redis:
            return 0
        
        try:
            keys = []
            async for key in self.redis.scan_iter(match=pattern):
                keys.append(key)
            
            if keys:
                deleted = await self.redis.delete(*keys)
                logger.info(f"Cleared {deleted} keys matching pattern: {pattern}")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Cache clear pattern error for {pattern}: {e}")
            return 0
    
    async def get_or_set(
        self,
        key: str,
        factory,
        ttl: Optional[int] = None
    ) -> Any:
        """
        Get value from cache or compute and cache it.
        
        Args:
            key: Cache key
            factory: Async function to compute value if not cached
            ttl: Time to live in seconds
            
        Returns:
            Cached or computed value
        """
        # Try to get from cache
        value = await self.get(key)
        if value is not None:
            return value
        
        # Compute value
        value = await factory()
        
        # Cache it
        await self.set(key, value, ttl)
        
        return value


# Global cache manager instance
cache_manager = CacheManager()
