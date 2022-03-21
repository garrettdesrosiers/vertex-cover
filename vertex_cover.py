#Name: Garrett DesRosiers
#Description: Produces three vertex covers using different algorithms
#Class: CSC 349
#Programming Assignment #4 

import sys

def get_edge_list(filename):
   fp = open(filename, 'r')
   edge_list = fp.read().split('\n')
   edge_list = edge_list[:-1]
   new_list = []
   for edge in edge_list:
      edge = edge.split(' ')
      new_list.append([int(edge[0]), int(edge[1])])
   return new_list

def get_degree(node):
   return len(node[1])

def get_label(node):
   return node[0]

def build_empty_adj_list(edge_list):
   maximum = 0   
   for i in range(len(edge_list)):
      for j in range(2):
         if edge_list[i][j] > maximum:
            maximum = edge_list[i][j]
   empty_adj_list = []
   for k in range(maximum + 1):
      empty_adj_list.append([k, []])
   return empty_adj_list

def build_adj_list(edge_list, empty_adj_list):
   for edge in edge_list:
      empty_adj_list[edge[0]][1].append(edge[1])
      empty_adj_list[edge[1]][1].append(edge[0])
   return empty_adj_list

def sort_neighbors(adj_list):
   for v in adj_list:
      v[1].sort()
   return adj_list

def smart_greedy(graph):
   vertex_cover = ['log-Approximation:']
   for v in graph:
      if len(v[1]) > 0:
         vertex_cover.append(str(v[0]))
         graph = sorted(graph, key=get_label)
         for neighbor in graph[v[0]][1]:
            graph[neighbor][1].remove(v[0])
         graph[v[0]][1] = []
         graph = sorted(graph, key=get_degree, reverse=True)
   return ' '.join(vertex_cover)

def basic_greedy(graph):
   vertex_cover = ['2-Approximation:']
   for v in graph:
      if len(v[1]) > 0:
         v1 = v[0]
         v2 = v[1][0]
         vertex_cover.append(str(v1))
         vertex_cover.append(str(v2))
         for neighbor1 in graph[v1][1]:
            graph[neighbor1][1].remove(v1)
         for neighbor2 in graph[v2][1]:
            graph[neighbor2][1].remove(v2)
         graph[v1][1] = []
         graph[v2][1] = []
   return ' '.join(vertex_cover) 


def create_permutations(vertices):
   val = 1
   permutations = []
   while val < (2 ** len(vertices)):
      temp_list = []
      for v in vertices:
         if val & (2 ** v[0]) != 0:
            temp_list.append(v)
      permutations.append(temp_list)
      val += 1
   return permutations

def is_vertex_cover(vertices, edge_list):
   copy = edge_list.copy()
   for vertex in vertices:
      for neighbor in vertex[1]:
         edge1 = [vertex[0], neighbor]
         edge2 = [neighbor, vertex[0]]
         if edge1 in copy:
            copy.remove(edge1)
         if edge2 in copy:
            copy.remove(edge2)
   if len(copy) == 0:
      return True
   return False

def exact(graph, edge_list):
   permutations = create_permutations(graph)
   vc = [str(x[0]) for x in graph]
   minimum = len(graph)
   for vertex_set in permutations:
      if is_vertex_cover(vertex_set, edge_list) and len(vertex_set) < minimum:
         minimum = len(vertex_set)
         vc = [str(y[0]) for y in vertex_set]
   return 'Exact Solution: ' + ' '.join(vc)


def main(argv):
   edge_list = get_edge_list(argv[1])
   empty_adj_list = build_empty_adj_list(edge_list)
   adj_list = build_adj_list(edge_list, empty_adj_list)
   adj_list = sort_neighbors(adj_list)
   smart_graph = sorted(adj_list, key=get_degree, reverse=True)
   print(smart_greedy(smart_graph))
   adj_list = build_adj_list(edge_list, empty_adj_list)
   adj_list = sort_neighbors(adj_list)
   basic_graph = sorted(adj_list, key=get_label)
   print(basic_greedy(basic_graph))
   adj_list = build_adj_list(edge_list, empty_adj_list)
   adj_list = sort_neighbors(adj_list)
   exact_graph = sorted(adj_list, key=get_label)
   print(exact(exact_graph, edge_list))

if __name__ == "__main__":
   main(sys.argv)
