import { useState, useEffect } from 'react';

interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl: number; // Time to live in milliseconds
}

class SimpleCache {
  private cache: Map<string, CacheEntry<any>> = new Map();

  get<T>(key: string): T | null {
    const entry = this.cache.get(key);
    if (!entry) {
      return null;
    }

    // Check if entry has expired
    if (Date.now() - entry.timestamp > entry.ttl) {
      this.cache.delete(key);
      return null;
    }

    return entry.data;
  }

  set<T>(key: string, data: T, ttl: number = 5 * 60 * 1000): void { // Default TTL: 5 minutes
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl
    });
  }

  remove(key: string): void {
    this.cache.delete(key);
  }

  clear(): void {
    this.cache.clear();
  }
}

const cache = new SimpleCache();

export const useCache = <T>(key: string, initialValue: T | null = null, ttl: number = 5 * 60 * 1000) => {
  const [cachedValue, setCachedValue] = useState<T | null>(() => {
    return cache.get<T>(key) ?? initialValue;
  });

  const [hasValue, setHasValue] = useState(() => {
    return cache.get<T>(key) !== null;
  });

  const setValue = (value: T) => {
    cache.set(key, value, ttl);
    setCachedValue(value);
    setHasValue(true);
  };

  const removeValue = () => {
    cache.remove(key);
    setCachedValue(initialValue);
    setHasValue(false);
  };

  const refreshValue = () => {
    const value = cache.get<T>(key);
    if (value !== null) {
      setCachedValue(value);
      setHasValue(true);
    } else {
      setCachedValue(initialValue);
      setHasValue(false);
    }
  };

  return {
    value: cachedValue,
    hasValue,
    setValue,
    removeValue,
    refreshValue
  };
};

// Additional hook for caching API responses
export const useApiCache = <T>(key: string, apiCall: () => Promise<T>, ttl: number = 5 * 60 * 1000) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const { value: cachedData, hasValue, setValue: setCacheValue, refreshValue } = useCache<T>(key, null, ttl);

  useEffect(() => {
    const fetchData = async () => {
      if (hasValue && cachedData) {
        // Use cached data
        setData(cachedData);
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const result = await apiCall();
        setData(result);
        setCacheValue(result); // Store in cache
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [key]); // Only run once when key changes

  const refresh = async () => {
    try {
      setLoading(true);
      const result = await apiCall();
      setData(result);
      setCacheValue(result); // Update cache
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  return {
    data,
    loading,
    error,
    refresh,
    isCached: hasValue
  };
};