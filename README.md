# RedisProxy

# Architecture

The redis proxy is implemented with python flask. There are three major compoents: Proxy, Cache, and RedisFence. Their relationships are illustrated by this chart.
![image](https://user-images.githubusercontent.com/54859268/167300943-27da467f-7283-4888-a5ab-3e1749a42439.png)

# How The Code Works

When a request get to the proxy, it first tries to fetch from the cache. If it does not exists in the cache or the cache entry has expired, then it will incur a redis operation to fetch from the backing redis server. Once the record is succesfully fetched from redis, it stores that record to the cache. If the cache reaches the capacity, it removes the least recent used cache entry implemented using double linked link.

# Cache Runtime Complexity

This is implemented using a double linked list.
get -> O(1) set -> O(1)

# How To Run The Proxy Service

All the configuration is in config.py. Once you are happy with the config, you can start the proxy service by running:

```
make run
```

# Time Spent

Create python flask framework - 1 hour.  
Implement LRU cache - 1 hour.  
Implement proxy logic - 1 hour.  
Implement Redis get with retry - 2 hours.  
Unit tests and integration tests - 2 hours.  

# Unsatisfied Requirement

Bonus Redis Client Protocol - cannot find more time
