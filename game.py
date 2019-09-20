import  curses
from curses import textpad

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

def update_player_position(d, p):
    if d == curses.KEY_RIGHT:
        p[0] += 3
    elif d == curses.KEY_LEFT:
        p[0] -= 3 
    elif d == curses.KEY_DOWN:
        p[1] += 1
    elif d == curses.KEY_UP:
        p[1] -= 1
     
    return p 


def main(stdscr):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    box = [[3,3], [sh-3, sw-3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    ppos = [sw//2, sh//2]
    pdir = curses.KEY_RIGHT
    papp = ".o."
    ptra = "..."
    stdscr.addstr(ppos[1], ppos[0], papp)
    
    while 1:
        key = stdscr.getch()
        
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            pdir = key
            stdscr.addstr(ppos[1], ppos[0], ptra)
            papp = update_player_appearance(pdir)
            ppos = update_player_position(pdir, ppos)
            stdscr.addstr(ppos[1], ppos[0], papp)
        if key == curses.KEY_BACKSPACE:
            if ptra == "...":
                ptra = "~~~"
            else:
                ptra = "..."
    stdscr.refresh()


curses.wrapper(main)
