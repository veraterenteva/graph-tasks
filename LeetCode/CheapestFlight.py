class Solution(object):
    def findCheapestPrice(self, n, flights, src, dst, k):
        """
        :type n: int
        :type flights: List[List[int]]
        :type src: int
        :type dst: int
        :type k: int
        :rtype: int
        """
        prev = [float('inf')] * n
        prev[src] = 0

        for i in range(k + 1):
            curr = prev[:]
            for u, v, w in flights:
                if prev[u] + w < curr[v]:
                    curr[v] = prev[u] + w
            prev = curr  # move to next

        return -1 if prev[dst] == float('inf') else prev[dst]

# Time: O((k+1) * N) where N = num of flights
# Idea: modified Bellman–Ford algorithm which relaxes edges up to k+1 times, otherwise we are done with that