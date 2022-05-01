def lru_cache(maxsize=100, get_space=lambda obj:1):
    assert maxsize > 0

    def decorating_function(user_function):
        cache = dict()
        cache_get = cache.get  # bound method to lookup key or return None
        _get_space = get_space  # make it local
        total_space = [0]
        root = []  # root of the circular doubly linked list
        nonlocal_root = [root]  # make updateable non-locally
        root[:] = [root, root, None, None, 0]  # initialize by pointing to self
        PREV, NEXT = 0, 1  # names for the link fields

        def wrapper(*args):
            # size limited caching that tracks accesses by recency
            key = tuple(args)
            link = cache_get(key)
            if link is not None:
                # record recent use of the key by moving it to the front of the list
                # HIT
                root, = nonlocal_root
                link_prev, link_next, key, result, _space = link
                link_prev[NEXT] = link_next
                link_next[PREV] = link_prev
                last = root[PREV]
                last[NEXT] = root[PREV] = link
                link[PREV] = last
                link[NEXT] = root
                return result

            # MISS
            result = user_function(*args)
            space = _get_space(result)
            total_space[0] += space

            root = nonlocal_root[0]

            last = root[PREV]
            link = [last, root, key, result, space]
            cache[key] = last[NEXT] = root[PREV] = link

            while total_space[0] > maxsize:
                # purge least recently used cache entry
                _old_prev, old_next, old_key, _old_result, space = root[NEXT]
                total_space[0] -= space
                root[NEXT] = old_next
                old_next[PREV] = root
                del cache[old_key]

            return result

        def cache_clear():
            """Clear the cache and cache statistics"""
            total_space = [0]
            cache.clear()
            root = nonlocal_root[0]
            root[:] = [root, root, None, None, 0]

        wrapper.__wrapped__ = user_function
        wrapper.cache_clear = cache_clear
        return update_wrapper(wrapper, user_function)

    return decorating_function