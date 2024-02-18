from BFS_DFS import bfs
from BFS_DFS import dfs

graph = {
  '5' : ['3','7'],
  '3' : ['2', '4'],
  '7' : ['8'],
  '2' : [],
  '4' : [],
  '8' : []
}

# Driver Code
print("Following is the Breadth-First Search")
bfs(graph, '5')    # function calling


print("Following is the Depth-First Search")
dfs(graph,'5')