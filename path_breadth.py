
def pathFindBreadth(start, goal, map):
    visited = {}
    visit = [(start,None)]

    while len(visit):
        s, p = visit.pop(0)
        if s[1]<0 or s[1]>=len(map) \
            or s[0]<0 or s[0]>=len(map[s[1]]) \
            or map[s[1]][s[0]] == 0:
            continue
        if visited.has_key(s):
            continue
        visited[s] = p
        if s == goal:
            break
        visit += (((s[0]-1,s[1]), s), ((s[0]+1,s[1]), s), \
                ((s[0],s[1]-1), s), ((s[0],s[1]+1), s))
    #endwhile
    p = goal
    path = []
    while p != start:
        path.insert(0, p)
        p = visited[p]
    return path
#enddef

data = [
    '    S #G             ',
    '      #              ',
    ' ################### ',
    ' #                 # ',
    ' ####  #########  ## ',
    '    #  #          #  ',
    ' ##    #  ## ####### ',
    ' ## ## # #         # ',
    ' #  ## #     ##### # ',
    ' # ##  #######   # # ',
    '       ##            '
];

map = []
start = (0,0)
goal = (0,0)
for y, ln in enumerate(data):
    row = []
    for x, ch in enumerate(ln):
        if ch == '#':
            row.append(0)
        else:
            row.append(1)
        if ch == 'S':
            start = (x,y)
        if ch == 'G':
            goal = (x,y)
    map.append(row)
#endfor

path = pathFindBreadth(start, goal, map)

for step, p in enumerate(path):
#    print step, p
    map[p[1]][p[0]] = step + 2

for row in map:
    for col in row:
        if col == 0:
            print '#',
        if col == 1:
            print ' ',
        if col >1:
            print (col-2) % 10,
    print
