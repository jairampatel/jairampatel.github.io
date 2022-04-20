import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
# plt.style.use('seaborn-paper')

MAX_MOVIES = 128
M = 3
MOVIE_COUNT = 1024

X_VALUES = "xvalues"
Y_VALUES = "yvalues"
LABEL = "label"

MERGE_SORT = "mergeSort"
# TOP_M1 = "topM1"
TOP_M2 = "topM2"
TOP_M3 = "topM3"
TOP_M4 = "topM4"
# TOP_M8 = "topM8"
# TOP_M16 = "topM16"
# TOP_M32 = "topM32"

TIER_LIST2 = "tierList2"
TIER_LIST3 = "tierList3"
TIER_LIST4 = "tierList4"
TIER_LIST8 = "tierList8"
TIER_LIST16 = "tierList16"
TIER_LIST32 = "tierList32"

TOPM_ARRAY = {}
TOPM_ARRAY[2] = []
TOPM_ARRAY[3] = []
TOPM_ARRAY[4] = []
TIER_ARRAY = {}
TIER_ARRAY[2] = []
TIER_ARRAY[3] = []
TIER_ARRAY[4] = []
TIER_ARRAY[8] = []
TIER_ARRAY[16] = []
TIER_ARRAY[32] = []

def createGraph(graphs):
    sns.set_theme()

    # plt.title("Comparisons to get top M Disney movies")
    plt.title("Total number of comparisons for 1024 movies for N queries")
    plt.xlabel("Number of queries")
    # plt.xlabel("Number of movies")
    plt.ylabel("Number of comparisons")
    for i, graph in graphs.items():
        x=graph[X_VALUES]
        y=graph[Y_VALUES]
        plt.plot(x,y, label=graph[LABEL])
    plt.legend()
    plt.show()

def mergeInsertionSort(n):
    # return (MOVIE_COUNT * math.log(MOVIE_COUNT,2)) - MOVIE_COUNT
    return (MOVIE_COUNT * math.log(MOVIE_COUNT,2)) - MOVIE_COUNT
    # return (n * math.log(n,2)) - n

def topM(n, m):
    # if m == 1:
    #     return n - 1
    # # return n * math.log(m,2)
    # newN = n - m
    # # if newN <= 0:
    # #     return 0
    # return n * math.log(m,2)
    
    # print("n/size: " + str(n) + " / " + str(len(TOPM_ARRAY)))

    # QUERIES
    if n == 1:
        TOPM_ARRAY[m].append(MOVIE_COUNT * math.log(m,2))
        return TOPM_ARRAY[m][0]
    else:
        total = TOPM_ARRAY[m][n - 2]
        result = (MOVIE_COUNT - (m * n)) * math.log(m,2)
        TOPM_ARRAY[m].append(total + result)
        return TOPM_ARRAY[m][n - 1]

def tierList(n, b, m):
    # newN = (n/b)
    # if newN <= 0:
    #     return 0
    # return newN + ((newN / b)* math.log(m,2))
    # return n + ((n / b)* math.log(m,2))

    # QUERIES
    itemPerBucket = MOVIE_COUNT / b
    if n == 1:
        result = (MOVIE_COUNT + (itemPerBucket * math.log(m,2)))
        TIER_ARRAY[b].append(result)
        return result
    else:
        total = TIER_ARRAY[b][n - 2]
        result = itemPerBucket * math.log(m,2)
        TIER_ARRAY[b].append(total + result)
        return TIER_ARRAY[b][n - 1]


def initGraph(graphs, type, label):
    graphs[type] = {}
    graphs[type][X_VALUES] = []
    graphs[type][Y_VALUES] = []
    graphs[type][LABEL] = label

graphs = {}
initGraph(graphs, MERGE_SORT, "Merge-Insertion Sort")
# initGraph(graphs, TOP_M1, "Top M (1) Buffer")
initGraph(graphs, TOP_M2, "Top M (2) Buffer")
initGraph(graphs, TOP_M3, "Top M (3) Buffer")
initGraph(graphs, TOP_M4, "Top M (4) Buffer")
# initGraph(graphs, TOP_M8, "Top M (8) Buffer")
# initGraph(graphs, TOP_M16, "Top M (16) Buffer")
# initGraph(graphs, TOP_M32, "Top M (32) Buffer")
initGraph(graphs, TIER_LIST2, "Tier List (2)")
initGraph(graphs, TIER_LIST3, "Tier List (3)")
initGraph(graphs, TIER_LIST4, "Tier List (4)")
initGraph(graphs, TIER_LIST8, "Tier List (8)")
initGraph(graphs, TIER_LIST16, "Tier List (16)")
initGraph(graphs, TIER_LIST32, "Tier List (32)")

i = 1
while i < 200:
    graphs[MERGE_SORT][X_VALUES].append(i)
    # graphs[TOP_M1][X_VALUES].append(i)
    graphs[TOP_M2][X_VALUES].append(i)
    graphs[TOP_M3][X_VALUES].append(i)
    graphs[TOP_M4][X_VALUES].append(i)
    # graphs[TOP_M8][X_VALUES].append(i)
    # graphs[TOP_M16][X_VALUES].append(i)
    # graphs[TOP_M32][X_VALUES].append(i)
    graphs[TIER_LIST2][X_VALUES].append(i)
    graphs[TIER_LIST3][X_VALUES].append(i)
    graphs[TIER_LIST4][X_VALUES].append(i)
    graphs[TIER_LIST8][X_VALUES].append(i)
    graphs[TIER_LIST16][X_VALUES].append(i)
    graphs[TIER_LIST32][X_VALUES].append(i)

    graphs[MERGE_SORT][Y_VALUES].append(mergeInsertionSort(i))
    # graphs[TOP_M1][Y_VALUES].append(topM(i, 1))
    graphs[TOP_M2][Y_VALUES].append(topM(i, 2))
    graphs[TOP_M3][Y_VALUES].append(topM(i, 3))
    graphs[TOP_M4][Y_VALUES].append(topM(i, 4))
    # graphs[TOP_M8][Y_VALUES].append(topM(i, 8))
    # graphs[TOP_M16][Y_VALUES].append(topM(i, 16))
    # graphs[TOP_M32][Y_VALUES].append(topM(i, 32))
    graphs[TIER_LIST2][Y_VALUES].append(tierList(i,2,3))
    graphs[TIER_LIST3][Y_VALUES].append(tierList(i,3,3))
    graphs[TIER_LIST4][Y_VALUES].append(tierList(i,4,3))
    graphs[TIER_LIST8][Y_VALUES].append(tierList(i,8,3))
    graphs[TIER_LIST16][Y_VALUES].append(tierList(i,16,3))
    graphs[TIER_LIST32][Y_VALUES].append(tierList(i,32,3))
    i = i + 1



createGraph(graphs)
