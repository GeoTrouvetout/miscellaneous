import  curses
from curses import textpad
import numpy as np

def update_player_appearance(d):
    if d == curses.KEY_RIGHT:
        p = ">o>"
    elif d == curses.KEY_LEFT:
        p = "<o<"
    elif d == curses.KEY_DOWN:
        p = "/o\\"
    elif d == curses.KEY_UP:
        p = "\o/"
    else: 
        p = ".o."
    return p 

def update_player_position(d, a, p, w):
    
    if d == curses.KEY_RIGHT:
        if p[0]+1 < len(w[0])  :
            if w[p[1]][p[0]+1] == " ":
                p[0] += 1
    elif d == curses.KEY_LEFT:
        if p[0]-1 > 0:
            if w[p[1]][p[0]-1] == " ":
                p[0] -= 1 
    elif d == curses.KEY_DOWN:
        if p[1]+1 < len(w[1]):
            if w[p[1]+1][p[0]] == " ":
                p[1] += 1
    elif d == curses.KEY_UP:
        if p[1]-1 > 0:
            if w[p[1]-1][p[0]] == " ":
                p[1] -= 1 
    return p 

def update_player_position3(d, a, p, w):
    sx = int(np.round(np.sin(a)))
    sy = int(np.round(np.cos(a)))
    if d == curses.KEY_UP:
        if 0 < p[1]-sy < len(w) and 0 < p[0]-sx < len(w[0]):
            if w[p[1]-sy][p[0]-sx] == " ":
                p[1] -= sy
                p[0] -= sx
    elif d == curses.KEY_DOWN:
        if 0 < p[1]+sy < len(w) and 0 < p[0]+sx < len(w[0]):
            if w[p[1]+sy][p[0]+sx] == " ":
                p[1] += sy
                p[0] += sx
    if d == curses.KEY_RIGHT:
        #if p[0]+1 < len(w[0])  :
        if 0 < p[1]-sx < len(w) and 0 < p[0]+sy < len(w[0]):
            #if w[p[1]][p[0]+1] == " ":
            if w[p[1]-sx][p[0]+sy] == " ":
                #p[0] += 1
                p[1] -= sx
                p[0] += sy
    elif d == curses.KEY_LEFT:
        #if p[0]-1 > 0:
        if 0 < p[1]+sx < len(w) and 0 < p[0]-sy < len(w[0]):
            #if w[p[1]-1][p[0]] == " ":
            if w[p[1]+sx][p[0]-sy] == " ":
                #p[0] -= 1 
                p[1] += sx
                p[0] -= sy
    return p

def get_distance(p, a,  w):
    bound = False
    dx = np.sin(a)
    dy = np.cos(a)
    r = [0, 0]
    i = 0
    while(not bound and i < 100):
        r[0] -= dx
        r[1] -= dy
        e = [ int(np.round(p[0]+r[0])), int(np.round(p[1]+r[1])) ]
        if 0 < e[1] < len(w) and 0 < e[0] < len(w[0]):
            if not w[e[1]][e[0]] == " ":
                bound=True
        else:
            bound = True
        i += 1
    #return dist
    return np.sqrt(np.sum(np.power(r,2)))




def get_worldmap():
    worldmap = []
    worldmap+=["                          "] 
    worldmap+=["                          "] 
    worldmap+=["    ▓▓▓▓            ▓     "] 
    worldmap+=["                     ▓    "] 
    worldmap+=["                     ▓    "] 
    worldmap+=["                     ▓    "] 
    worldmap+=["         ▓▓▓▓             "] 
    worldmap+=["                          "] 
    worldmap+=["                          "] 
    worldmap+=["                          "] 
    worldmap+=["                          "] 
    worldmap+=["                          "] 
    return worldmap

def draw_map(stdscr, f, offset):
    for i in range(len(f)):
        for j in range(len(f[i])):
            if not f[i][j] == " ":
                stdscr.addstr(i+offset[0], j+offset[1], f[i][j])
    textpad.rectangle(stdscr, offset[0], offset[1], len(f)+offset[0], len(f[1])+offset[1])
    
def draw_frame( stdscr, box, distances ):
    minheight, maxheight = 4, 20
    mindistance, maxdistance = 2, 10
    d = -(maxheight - minheight) / (maxdistance-mindistance)
    listchar = ["#", ""]
    for i in range(len(distances)):
        height = int(np.round(np.clip(distances[i]*d + maxheight, 4, 20)))
        if distances[i] <= 2:
            char = "█"
        elif distances[i] <= 4:
            char = "▓"
        elif distances[i] <= 6:
            char = "▒"
        elif distances[i] <= 8:
            char = "░"
        else:
            char = " "
            height = 0
        
        for j in np.arange(box[0][0], (box[1][0] - height ) // 2 ):
            stdscr.addstr( j, len(distances)-i+3, "▥")
        for j in np.arange( (box[1][0]- height)//2 + height, box[1][0]):
            stdscr.addstr( j, len(distances)-i+3, " ")
        for j in np.arange((box[1][0] - height)//2, (box[1][0]-height)//2 + height):
            stdscr.addstr( j, len(distances)-i+3, char)
         
     
def compute_fov(pos, angle, fov, ncolumn, worldmap):
    startangle, endangle = angle-(fov/2), angle+ (fov/2)
    tabdist = []
    for i in np.arange(startangle, endangle+((endangle-startangle)/ncolumn), (endangle-startangle)/ncolumn):
        tabdist.append(get_distance(pos, i , worldmap))
    
    return(tabdist)

def main(stdscr):

       
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    box = [[3,3], [sh-3, sw-3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
    worldmap = get_worldmap()
    offset =  (4, 4)
    draw_map(stdscr, worldmap, offset)
    
     
    ppos = [8, 8]
    pdir = curses.KEY_RIGHT
    pang = 0.0
    anglestep = 0.25*np.pi
    pfov = (1/4)*np.pi
    papp = "⏺"
    ptra = " "
    stdscr.addstr(ppos[1]+offset[1], ppos[0]+offset[0], papp)
    
    while 1:
        key = stdscr.getch()
        
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            pdir = key
            stdscr.addstr(ppos[1]+offset[1], ppos[0]+offset[0], " ")
            ppos = update_player_position3( pdir, pang, ppos, worldmap )
            stdscr.addstr(ppos[1]+offset[1], ppos[0]+offset[0], papp)
       
        if key == 113:
            pang += anglestep
            pang = pang%(2*np.pi)
        if key == 115:
            pang -= anglestep
            pang = pang%(2*np.pi)
        
        dis_ray =  get_distance(ppos, pang, worldmap)
        r = [ppos[1],ppos[0]]
        r[0] = np.sin(pang)
        r[1] = np.cos(pang)
        stdscr.addstr(0,0, "                                      ")
        stdscr.addstr(0,0, str(int(ppos[0])) + " " +str(int(ppos[1])))
        stdscr.addstr(20,0, "   ")
        stdscr.addstr(20,0, str(int((pang*180/np.pi)%360))+ " " + str(pang) )
        stdscr.addstr(20,40, str(r) )
        stdscr.addstr(0,50, "                                      " )
        stdscr.addstr(0,50, str(dis_ray) )
        
        fovdist = compute_fov(ppos, pang, pfov, sw-6, worldmap)
        stdscr.addstr(10,50,  str(min(fovdist)) +" "+ str(max(fovdist)))
        draw_frame(stdscr, box, fovdist)         
        
        if key == curses.KEY_BACKSPACE:
            if ptra == "   ":
                ptra = " # "
            else :
                ptra = "   "
        stdscr.refresh()


curses.wrapper(main)
