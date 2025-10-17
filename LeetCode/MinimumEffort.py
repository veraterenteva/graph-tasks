import heapq
from typing import List


class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        rows = len(heights)
        cols = len(heights[0])
        efforts = [[float('inf')] * cols for i in range(rows)]
        efforts[0][0] = 0

        # Min-heap effort row, col
        heap = [(0, 0, 0)]

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while heap:
            effort, r, c = heapq.heappop(heap)

            if r == rows - 1 and c == cols - 1:
                return effort

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    new_effort = max(effort, abs(heights[nr][nc] - heights[r][c]))
                    if new_effort < efforts[nr][nc]:
                        efforts[nr][nc] = new_effort
                        heapq.heappush(heap, (new_effort, nr, nc))

        return 0

# Time: O(m * n * log(m * n))
# Idea: Dijkstra’s algorithm but instead of summing weights we track the maximum weight at the moment with each path