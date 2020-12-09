from graphics import *
from itertools import chain, count
from copy import deepcopy
from math import ceil
from time import time, sleep
from random import randint
import os


class Piece:

    def __init__(self, pos, side, isKing=False):
        self.pos = pos
        self.side = side
        self.isKing = isKing

    def isSafe(self, grid):
        restricted = [(0, 0), (0, 10), (10, 0), (10, 10), (5, 5)]
        up = False
        down = False
        left = False
        right = False
        numDefenders = len(getDefenders(grid))

        # up
        if self.pos[1] == 0:
            up = self.isKing and numDefenders == 1
        else:
            p = grid[self.pos[1] - 1][self.pos[0]]
            if p == None:
                up = (self.pos[0], self.pos[1] - 1) in restricted
            else:
                up = p.side != self.side

        # down
        if self.pos[1] == 10:
            down = self.isKing and numDefenders == 1
        else:
            p = grid[self.pos[1] + 1][self.pos[0]]
            if p == None:
                down = (self.pos[0], self.pos[1] + 1) in restricted
            else:
                down = p.side != self.side

        # left
        if self.pos[0] == 0:
            left = self.isKing and numDefenders == 1
        else:
            p = grid[self.pos[1]][self.pos[0] - 1]
            if p == None:
                left = (self.pos[0] - 1, self.pos[1]) in restricted
            else:
                left = p.side != self.side

        # right
        if self.pos[0] == 10:
            right = self.isKing and numDefenders == 1
        else:
            p = grid[self.pos[1]][self.pos[0] + 1]
            if p == None:
                right = (self.pos[0] + 1, self.pos[1]) in restricted
            else:
                right = p.side != self.side

        if self.isKing:
            return not all([up, down, left, right])
        else:
            return not ((up and down) or (left and right))


class BoardSelection:

    def __init__(self, pos, fname):
        self.pos = pos
        self.fname = fname
        self.grid = [x.strip().split(",") for x in open(fname, "r").readlines()]

    def draw(self, win, s):
        createRectangle(win, Point(self.pos[0], self.pos[1] + s), Point(self.pos[0] + 170, self.pos[1] + 182 + s),
                        "yellow", "black", 3)
        createText(win, (self.pos[0] + 85, self.pos[1] + 12 + s), self.fname.replace(".txt", ""), size=16,
                   style="italic")
        createRectangle(win, Point(self.pos[0] + 10, self.pos[1] + 25 + s),
                        Point(self.pos[0] + 160, self.pos[1] + 175 + s), color_rgb(222, 184, 135),
                        color_rgb(222, 184, 135), 3)
        x = self.pos[0] + 11 + 13
        while x < self.pos[0] + 158:
            createLine(win, Point(x, self.pos[1] + 26 + s), Point(x, self.pos[1] + 174 + s))
            x += 13.4
        y = self.pos[1] + 26 + 13
        while y < self.pos[1] + 174:
            createLine(win, Point(self.pos[0] + 11, y + s), Point(self.pos[0] + 159, y + s))
            y += 13.4

        createRectangle(win, Point(self.pos[0] + 12, self.pos[1] + 27 + s),
                        Point(self.pos[0] + 23, self.pos[1] + 38 + s), color_rgb(139, 69, 19), color_rgb(139, 69, 19))
        createRectangle(win, Point(self.pos[0] + 146, self.pos[1] + 27 + s),
                        Point(self.pos[0] + 158, self.pos[1] + 38 + s), color_rgb(139, 69, 19), color_rgb(139, 69, 19))
        createRectangle(win, Point(self.pos[0] + 12, self.pos[1] + 161 + s),
                        Point(self.pos[0] + 23, self.pos[1] + 172 + s), color_rgb(139, 69, 19), color_rgb(139, 69, 19))
        createRectangle(win, Point(self.pos[0] + 146, self.pos[1] + 161 + s),
                        Point(self.pos[0] + 158, self.pos[1] + 172 + s), color_rgb(139, 69, 19), color_rgb(139, 69, 19))
        createRectangle(win, Point(self.pos[0] + 79, self.pos[1] + 94 + s),
                        Point(self.pos[0] + 90, self.pos[1] + 105 + s), color_rgb(139, 69, 19), color_rgb(139, 69, 19))
        createRectangle(win, Point(self.pos[0] + 10, self.pos[1] + 25 + s),
                        Point(self.pos[0] + 160, self.pos[1] + 175 + s), None, "black", 4)
        for i in range(11):
            for j in range(11):
                p = self.grid[i][j]
                if p != "e":
                    createCircle(win, (self.pos[0] + (13.4 * j) + 17, self.pos[1] + (13.4 * i) + 32 + s), 4.5,
                                 "white" if p == "d" or p == "k" else "black",
                                 "white" if p == "d" or p == "k" else "black")
                    if p == "k":
                        createLine(win, Point(self.pos[0] + (13.4 * j) + 18, self.pos[1] + (13.4 * i) + 28 + s),
                                   Point(self.pos[0] + (13.4 * j) + 18, self.pos[1] + (13.4 * i) + 38 + s), width=2)
                        createLine(win, Point(self.pos[0] + (13.4 * j) + 12, self.pos[1] + (13.4 * i) + 33 + s),
                                   Point(self.pos[0] + (13.4 * j) + 23, self.pos[1] + (13.4 * i) + 33 + s), width=2)


wSize = (552, 552)
mousePos = (0, 0)
scrollCount = 0
aCollected = 0
dCollected = 0


def createText(win, pos, string, color="black", face="helvetica", size=12, style="normal"):
    t = Text(Point(pos[0], pos[1]), string)
    t.setFace(face)
    t.setSize(size)
    t.setStyle(style)
    t.setTextColor(color)
    t.draw(win)


def createRectangle(win, p1, p2, fcolor="", ocolor="black", width=1):
    r = Rectangle(p1, p2)
    r.setFill(fcolor)
    r.setOutline(ocolor)
    r.setWidth(width)
    r.draw(win)


def createLine(win, p1, p2, color="black", width=1, arrow="none"):
    l = Line(p1, p2)
    l.setOutline(color)
    l.setWidth(width)
    l.setArrow(arrow)
    l.draw(win)


def createCircle(win, pos, r, fcolor="", ocolor="black", width=1):
    c = Circle(Point(pos[0], pos[1]), r)
    c.setFill(fcolor)
    c.setOutline(ocolor)
    c.setWidth(width)
    c.draw(win)


def drawBoard(win, grid, doUpdate=True, ex=[], side=None):
    clear(win, ex)

    createRectangle(win, Point(49, 49), Point(wSize[0] - 50, wSize[1] - 50), color_rgb(210, 105, 30), "black")
    createRectangle(win, Point(51, 51), Point(91, 91), color_rgb(139, 69, 19), color_rgb(139, 69, 19))
    createRectangle(win, Point(wSize[0] - 91, 51), Point(wSize[0] - 51, 91), color_rgb(139, 69, 19),
                    color_rgb(139, 69, 19))
    createRectangle(win, Point(51, wSize[1] - 91), Point(91, wSize[1] - 51), color_rgb(139, 69, 19),
                    color_rgb(139, 69, 19))
    createRectangle(win, Point(wSize[0] - 91, wSize[1] - 91), Point(wSize[0] - 51, wSize[1] - 51),
                    color_rgb(139, 69, 19), color_rgb(139, 69, 19))
    createRectangle(win, Point(256, 256), Point(296, 296), color_rgb(139, 69, 19), color_rgb(139, 69, 19))
    # grid is 11 x 11
    for x in range(50, wSize[0] - 50, 41):
        createLine(win, Point(x, 50), Point(x, wSize[1] - 51), color="black")
        createLine(win, Point(50, x), Point(wSize[0] - 51, x), color="black")

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if isinstance(grid[i][j], Piece):
                p = grid[i][j]
                createCircle(win, (71 + 41 * j, 71 + 41 * i), 15, "white" if p.side == "Defender" else "black",
                             "white" if p.side == "Defender" else "black")
                if p.isKing == True:
                    l1 = Line(Point(71 + 41 * j, 56 + 41 * i), Point(71 + 41 * j, 87 + 41 * i))
                    l2 = Line(Point(56 + 41 * j, 71 + 41 * i), Point(87 + 41 * j, 71 + 41 * i))
                    l1.setWidth(3)
                    l2.setWidth(3)
                    l1.draw(win)
                    l2.draw(win)

    if side != None:
        createText(window, (276, 527), side, size=18, style="italic")
        if side == "Attacker":
            createRectangle(win, Point(229, 514), Point(324, 540), None, "black", 3)
            createCircle(win, (215, 525), 10, "black", "black")
            createCircle(win, (338, 525), 10, "black", "black")
        else:
            createRectangle(win, Point(226, 510), Point(330, 540), None, "black", 3)
            createCircle(win, (210, 525), 10, "white", "black")
            createCircle(win, (343, 525), 10, "white", "black")

    global aCollected
    global dCollected
    displayCollected(win, aCollected, dCollected, doUpdate)

    if doUpdate:
        update(60)


def clear(win, ex=[]):
    for item in win.items[:]:
        if str(item.__class__.__name__) not in ex:
            item.undraw()


def loadBoard(grid, fname):
    lst = [x.strip().split(",") for x in open(fname + ".txt", "r").readlines()]
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            c = lst[i][j]

            if c == "k":
                grid[i][j] = Piece((j, i), "Defender", True)
            elif c == "d":
                grid[i][j] = Piece((j, i), "Defender")
            elif c == "a":
                grid[i][j] = Piece((j, i), "Attacker")


def getPosFromClick(pos):
    x = pos.getX()
    y = pos.getY()
    gx = (x - 50) // 41 if 50 < x < wSize[0] - 51 else -1
    gy = (y - 50) // 41 if 50 < y < wSize[1] - 51 else -1
    return (int(gx), int(gy))


def showMoves(win, p, grid, doShow=True):
    drawBoard(win, grid, False)
    px = p.pos[0]

    py = p.pos[1]

    if doShow:
        createRectangle(win, Point(50 + px * 41, 50 + py * 41), Point(91 + px * 41, 91 + py * 41), width=3)
    lst = []
    restricted = [(0, 0), (0, 10), (10, 0), (10, 10)]
    # up
    if py > 0:
        for x in range(py - 1, -1, -1):
            if isinstance(grid[x][px], Piece):
                break
            else:
                if (px, x) == (5, 5):
                    if p.isKing:
                        lst.append((px, x))
                elif (px, x) in restricted:
                    if p.isKing:
                        lst.append((px, x))
                    else:
                        break
                else:
                    lst.append((px, x))

    # down
    if py < 10:
        for x in range(py + 1, 11):
            if isinstance(grid[x][px], Piece):
                break
            else:
                if (px, x) == (5, 5):
                    if p.isKing:
                        lst.append((px, x))
                elif (px, x) in restricted:
                    if p.isKing:
                        lst.append((px, x))
                    else:
                        break
                else:
                    lst.append((px, x))

    # left
    if px > 0:
        for x in range(px - 1, -1, -1):
            if isinstance(grid[py][x], Piece):
                break
            else:
                if (x, py) == (5, 5):
                    if p.isKing:
                        lst.append((x, py))
                elif (x, py) in restricted:
                    if p.isKing:
                        lst.append((x, py))
                    else:
                        break
                else:
                    lst.append((x, py))

    # right
    if px < 11:
        for x in range(px + 1, 11):
            if isinstance(grid[py][x], Piece):
                break
            else:
                if (x, py) == (5, 5):
                    if p.isKing:
                        lst.append((x, py))
                elif (x, py) in restricted:
                    if p.isKing:
                        lst.append((x, py))
                    else:
                        break
                else:
                    lst.append((x, py))

    if doShow:
        for pos in lst:
            createRectangle(win, Point(53 + pos[0] * 41, 53 + pos[1] * 41), Point(88 + pos[0] * 41, 88 + pos[1] * 41),
                            color_rgb(153, 31, 0), color_rgb(153, 31, 0))

    update(60)
    return lst


def updatePieces(grid, p):
    global aCollected
    global dCollected
    # done twice to allow calculating 'checkmate' after a piece might be captured
    b = True
    for k in range(2):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] != None:
                    if not grid[i][j].isSafe(grid):
                        if i == p[1] and j == p[0] and b:
                            # gives the moved piece priority in capturing
                            b = False
                        else:
                            if grid[i][j].side == "Attacker":
                                aCollected += 1
                            elif grid[i][j].side == "Defender":
                                dCollected += 1
                            grid[i][j] = None


def animateMove(win, grid, p1, p2):
    prevp = p1
    while p1 != p2:
        if p1[0] == p2[0]:  # horizontal
            if p1[1] < p2[1]:
                p1 = (p1[0], p1[1] + 1)
            else:
                p1 = (p1[0], p1[1] - 1)
        elif p1[1] == p2[1]:  # vertical
            if p1[0] < p2[0]:
                p1 = (p1[0] + 1, p1[1])
            else:
                p1 = (p1[0] - 1, p1[1])

        grid[p1[1]][p1[0]] = grid[prevp[1]][prevp[0]]
        grid[p1[1]][p1[0]].pos = p1
        grid[prevp[1]][prevp[0]] = None
        prevp = p1

        drawBoard(win, grid)


def getPieces(grid):
    return list(filter(lambda x: x != None, chain.from_iterable(grid)))


def getKing(grid):
    return list(filter(lambda x: x.isKing, filter(lambda x: x != None, chain.from_iterable(grid))))


def getDefenders(grid):
    return list(filter(lambda x: x.side == "Defender", filter(lambda x: x != None, chain.from_iterable(grid))))


def getAttackers(grid):
    return list(filter(lambda x: x.side == "Attacker", filter(lambda x: x != None, chain.from_iterable(grid))))


def convertGrid(grid):
    g = deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            n = grid[i][j]
            g[i][j] = None if n == 0 else Piece((j, i), "Attacker") if n == 1 else Piece((j, i),
                                                                                         "Defender") if n == 2 else Piece(
                (j, i), "Defender", True)
    return g


def drawCreatorGUI(win):
    createRectangle(win, Point(400, 510), Point(500, 544), "red", "black", 3)
    createText(win, (450, 527), "Save", size=22, color="white")
    createText(win, (35, 527), "File Name:", size=9, color="black")
    createText(win, (275, 35), "Click on a square to toggle its state, and input a file name and save when finished",
               size=10, color="black")
    createLine(win, Point(7, 12), Point(43, 12), color="black", width=5, arrow="first")
    if "Entry" not in [str(x.__class__.__name__) for x in win.items]:
        fileNameEntry = Entry(Point(225, 527), 35)
        fileNameEntry.setFill(color_rgb(255, 255, 240))
        fileNameEntry.setText("-")
        fileNameEntry.draw(win)
    update(60)


def rectContains(r1, r2, p):
    return r1[0] < p[0] < r2[0] and r1[1] < p[1] < r2[1]


def validateBoard(grid):
    g = convertGrid(grid)
    # attackers have 2x more pieces then defenders
    nd = len(getDefenders(g))
    na = len(getAttackers(g))
    v1 = (nd - 1) * 2 == na and nd != 0 and na != 0
    # no pieces in a 'captured' position
    v2 = all(x.isSafe(g) for x in getPieces(g))
    return (v1, v2)


def saveGrid(grid, fname):
    with open(fname + ".txt", "w") as f:
        f.write("\n".join(
            ",".join(map(lambda p: "e" if p == 0 else "a" if p == 1 else "d" if p == 2 else "k", x)) for x in grid))
        f.close()


def createBackgroundSquare(win, pos):
    square = Rectangle(Point(pos[0], pos[1]), Point(pos[0] + 46, pos[1] + 46))
    square.setFill(color_rgb(222, 184, 135))
    square.setOutline(color_rgb(222, 184, 135))
    square.draw(win)
    return square


def motion(e):
    global mousePos
    mousePos = (e.x, e.y)


def mouse_wheel(e):
    global scrollCount

    scrollCount += e.delta
    n = ceil(len(getBoards()) / 3)

    if scrollCount < -192 * (n - 3) - 10 * n:
        scrollCount = -192 * (n - 3) - 10 * n
    if scrollCount > 0:
        scrollCount = 0


def animateBackground(win, squares):
    clear(win, ["Rectangle"])
    for s in squares:
        s.move(1, -1)
        if s.getP1().getX() > 552 or s.getP2().getY() < 0:
            s.move(-598, 598)


def createMenuGUI(win):
    createText(win, (125, 175), "One Player", face="arial", size=20, style="bold",
               color=color_rgb(200, 0, 40) if rectContains((40, 160), (210, 185),
                                                           (mousePos[0], mousePos[1])) else "black")
    createText(win, (125, 225), "Two Player", face="arial", size=20, style="bold",
               color=color_rgb(200, 0, 40) if rectContains((40, 215), (210, 235),
                                                           (mousePos[0], mousePos[1])) else "black")
    createText(win, (145, 275), "Board Creator", face="arial", size=20, style="bold",
               color=color_rgb(200, 0, 40) if rectContains((40, 260), (230, 285),
                                                           (mousePos[0], mousePos[1])) else "black")
    createText(win, (88, 325), "Rules", face="arial", size=20, style="bold",
               color=color_rgb(200, 0, 40) if rectContains((40, 315), (125, 335),
                                                           (mousePos[0], mousePos[1])) else "black")

    try:
        titleImage = Image(Point(276, 75), "title.png")
        titleImage.draw(win)
    except:
        pass


def createRulesGUI(win):
    createLine(win, Point(7, 12), Point(43, 12), width=5, arrow="first")
    createText(win, (58, 50), "Pieces:", size=18, style="bold italic")
    createCircle(win, (35, 85), 10, "black", "black")

    createCircle(win, (35, 115), 10, "white", "black")
    createCircle(win, (35, 145), 10, "white", "black")
    createLine(win, Point(35, 135), Point(35, 155), color="black", width=3)
    createLine(win, Point(25, 145), Point(45, 145), color="black", width=3)
    createText(win, (221, 85), "The Attacker's goal is to capture the King and its Defenders", size=9)
    createText(win, (243, 115), "The Defender's goal is to protect the King and capture the Attackers", size=9)
    createText(win, (190, 145), "The King's goal is to reach a corner of the board", size=9)
    createText(win, (74, 175), "Movement:", size=18, style="bold italic")
    createText(win, (190, 195), "All pieces can move along a straight line up, down, left, or right", size=9)
    createText(win, (283, 208),
               "All pieces can occupy any square, except the Restricted Squares, which only the King can occupy",
               size=9)
    createText(win, (181, 221), "Upon selecting a piece, possible moves will be highlighted", size=9)
    createText(win, (239, 234), "Only one piece can be moved on each turn, after which the other player will move",
               size=9)
    createText(win, (123, 255), "Restricted Squares:", size=18, style="bold italic")
    createText(win, (285, 275),
               "The squares at the corners of the board plus the middle square are known as Restricted Squares", size=9)
    createText(win, (231, 288), "Any piece can move through these squares, but only the King can stop on one", size=9)
    createText(win, (74, 310), "Capturing:", size=18, style="bold italic")
    createText(win, (252, 330), "To capture a Defender or Attacker, surround them on opposite sides with Hostile tiles",
               size=9)
    createText(win, (234, 345), "A Hostile tile can be either a piece from the other player, or a Restricted Square",
               size=9)
    createText(win, (216, 360), "To capture the King, it must be surrounded on all 4 sides by Hostile tiles", size=9)
    createText(win, (247, 375), "The King can also be captured on the side of the board if there are no Defenders left",
               size=9)
    createLine(win, Point(30, 425), Point(55, 395), color="green", width=3)
    createLine(win, Point(30, 425), Point(22, 410), color="green", width=3)
    createLine(win, Point(22, 480), Point(52, 510), color="red", width=3)
    createLine(win, Point(52, 480), Point(22, 510), color="red", width=3)

    def createGrid(pos, grid):
        for i in range(3):
            for j in range(3):
                c = grid[i][j]
                createLine(win, Point(pos[0] + 21 * j + 11, pos[1] + 21 * i),
                           Point(pos[0] + 21 * j + 11, pos[1] + 21 * i + 21), color=color_rgb(210, 105, 30), width=20)
                if c == "a":
                    createCircle(win, (pos[0] + 21 * j + 11, pos[1] + 21 * i + 11), 6, "black", "black")
                elif c == "d":
                    createCircle(win, (pos[0] + 21 * j + 11, pos[1] + 21 * i + 11), 6, "white", "black")
                elif c == "k":
                    createCircle(win, (pos[0] + 21 * j + 11, pos[1] + 21 * i + 11), 6, "white", "black")
                    createLine(win, Point(pos[0] + 21 * j + 11, pos[1] + 21 * i + 5),
                               Point(pos[0] + 21 * j + 11, pos[1] + 21 * i + 16), width=1)
                    createLine(win, Point(pos[0] + 21 * j + 5, pos[1] + 21 * i + 11),
                               Point(pos[0] + 21 * j + 16, pos[1] + 21 * i + 11), width=1)
                elif c == "r":
                    createLine(win, Point(pos[0] + 21 * j + 11, pos[1] + 21 * i),
                               Point(pos[0] + 21 * j + 11, pos[1] + 21 * i + 21), color=color_rgb(139, 69, 19),
                               width=20)
        createLine(win, Point(pos[0], pos[1]), Point(pos[0] + 64, pos[1]), width=3)
        createLine(win, Point(pos[0] + 64, pos[1]), Point(pos[0] + 64, pos[1] + 64), width=3)
        createLine(win, Point(pos[0] + 64, pos[1] + 64), Point(pos[0], pos[1] + 64), width=3)
        createLine(win, Point(pos[0], pos[1] + 64), Point(pos[0], pos[1]), width=3)
        createLine(win, Point(pos[0] + 21, pos[1]), Point(pos[0] + 21, pos[1] + 64), width=1)
        createLine(win, Point(pos[0] + 42, pos[1]), Point(pos[0] + 42, pos[1] + 64), width=1)
        createLine(win, Point(pos[0], pos[1] + 21), Point(pos[0] + 64, pos[1] + 21), width=1)
        createLine(win, Point(pos[0], pos[1] + 42), Point(pos[0] + 64, pos[1] + 42), width=1)

    createGrid((80, 390), [["e", "e", "e"], ["a", "d", "a"], ["e", "e", "e"]])
    createGrid((160, 390), [["e", "d", "e"], ["e", "a", "e"], ["e", "d", "e"]])
    createGrid((240, 390), [["e", "e", "e"], ["e", "a", "e"], ["a", "k", "a"]])
    createGrid((320, 390), [["e", "a", "e"], ["a", "k", "a"], ["e", "a", "e"]])
    createGrid((400, 390), [["r", "a", "d"], ["e", "e", "e"], ["e", "e", "e"]])
    createGrid((80, 465), [["e", "a", "e"], ["a", "d", "e"], ["e", "e", "e"]])
    createGrid((160, 465), [["e", "e", "e"], ["a", "k", "a"], ["e", "e", "e"]])
    createGrid((240, 465), [["d", "e", "e"], ["e", "a", "e"], ["a", "k", "a"]])
    createGrid((320, 465), [["r", "k", "a"], ["e", "a", "e"], ["e", "e", "e"]])


def displayCollected(win, na, nd, doUpdate=True):
    x = 15

    y = 60
    for i in range(na):
        createCircle(win, (x, y), 6, "black", "black")
        if i % 2 != 0:
            x = 15
            y += 20
        else:
            x += 20

    x = 517
    y = 60
    for i in range(nd):
        createCircle(win, (x, y), 6, "white", "black", 2)
        if i % 2 != 0:
            x = 517
            y += 20
        else:
            x += 20

    if doUpdate:
        update(60)


def getBoards():
    return sorted([f for f in os.listdir() if f.endswith(".txt")])[::-1]


def drawBoardSelect(win, lst, s):
    createRectangle(win, Point(0, 0 + s), Point(552, 552), color_rgb(222, 184, 135), color_rgb(222, 184, 135))
    for b in lst:
        b.draw(win, s)
    createRectangle(win, Point(0, 0 + s), Point(552, 552), None, "black", 5)
    update(60)


def generateBoardSelections(files):
    lst = []

    for y in count(10, 192):
        for x in [10, 191, 371]:
            lst.append(BoardSelection((x, y), files.pop()))
            if len(files) == 0:
                return lst


def drawEndScreen(win, w, t, m):
    switch = 1
    for i in range(0, 552, 24):
        for j in range(0, 552, 24):
            if switch == 1:
                s = int((((276 - i) ** 2 + (276 - j) ** 2) ** .5) / 6)
                createRectangle(win, Point(i, j), Point(i + 24, j + 24), color_rgb(222 - s, 184 - s, 135 - s),
                                color_rgb(222 - s, 184 - s, 135 - s))
            else:
                s = int((((276 - i) ** 2 + (276 - j) ** 2) ** .5) / 5)
                createRectangle(win, Point(i, j), Point(i + 24, j + 24), color_rgb(s, s, s), color_rgb(s, s, s))
            switch *= -1
    update(60)
    sleep(1)

    createText(win, (276, 50), "{} Wins!".format(w), color="white", size=30, style="bold")
    update(60)
    sleep(1)
    createText(win, (276, 150), "Time: {}".format(formatTime(t)), color="white", size=25, style="bold")
    update(60)
    sleep(1)
    createText(win, (276, 250), "Moves: {}".format(m), color="white", size=25, style="bold")
    update(60)


def formatTime(t):
    t = int(round(t))
    return str(int(t // 60)) + ":" + str(t % 60).zfill(2)


def drawSideSelect(win):
    global mousePos

    createRectangle(win, Point(0, 0), Point(552, 552), color_rgb(222, 184, 135), color_rgb(222, 184, 135))

    createText(win, (276, 60), "Pick", size=30, style="bold")
    createText(win, (276, 110), "a", size=30, style="bold")
    createText(win, (276, 160), "Side", size=30, style="bold")

    createCircle(win, (145, 400), 120, "black", "black")
    createCircle(win, (407, 400), 120, "white", "white")

    if inCircle(mousePos, (145, 400), 120):
        createText(win, (145, 400), "Attacker", color="white", size=20, style="bold")

    if inCircle(mousePos, (407, 400), 120):
        createText(win, (407, 400), "Defender", color="black", size=20, style="bold")

    update(60)


def inCircle(p, c, r):
    return ((p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2) ** .5 <= r


def defenderAI(win, grid):
    moves = []
    cache = {}

    for p in getDefenders(grid):
        arr = showMoves(win, p, grid, False)
        for move in arr:
            # determine value of the move
            total = 0
            if (move[0], move[1]) in cache and not p.isKing:
                total = cache[(move[0], move[1])]
            else:
                # +50 if moves king to corner               Done
                # +9 if moves king out of 3 pieces          Done
                # +4 if captures a piece                    Done
                # +~ if moves king closer to corner         Done
                # -5 if move gets piece captured            Done
                # -9 if moves king into 3 enemies           Done

                dis = lambda p1, p2: abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
                if p.isKing:
                    if move in [(0, 0), (0, 10), (10, 0), (10, 10)]:
                        total += 50

                    if getNumAdjacent(grid, p.pos, "Attacker") == 3:
                        total += 9

                    if getNumAdjacent(grid, move, "Attacker") == 3:
                        total -= 9

                    mMove = min([dis((0, 0), move), dis((0, 10), move), dis((10, 0), move), dis((10, 10), move)])
                    mPos = min([dis((0, 0), p.pos), dis((0, 10), p.pos), dis((10, 0), p.pos), dis((10, 10), p.pos)])
                    if mMove <= mPos:
                        total += 10 - mMove
                else:
                    g = deepcopy(grid)
                    g[move[1]][move[0]] = g[p.pos[1]][p.pos[0]]
                    g[move[1]][move[0]].pos = move
                    g[p.pos[1]][p.pos[0]] = None

                    lst = list(filter(lambda x: dis(x.pos, move) == 1, getAttackers(grid)))

                    canCapture = False
                    if not all([x.isSafe(g) for x in lst]):
                        total += 4
                        canCapture = True

                    newP = deepcopy(p)
                    newP.pos = move
                    if not newP.isSafe(g) and not canCapture:
                        total -= 7

                    cache[(move[0], move[1])] = total
            moves.append((p.pos, move, total))
    m = max(moves, key=lambda x: x[2])[2]
    moves = list(filter(lambda x: x[2] == m, moves))

    # pick a random move
    choice = moves[randint(0, len(moves) - 1)]
    animateMove(window, grid, choice[0], choice[1])
    updatePieces(grid, choice[1])


def attackerAI(win, grid):
    moves = []
    cache = {}

    k = getKing(grid)[0]
    kMoves = showMoves(win, k, grid, False)

    for p in getAttackers(grid):
        arr = showMoves(win, p, grid, False)
        for move in arr:
            # determine value of the move
            total = 0
            dis = lambda p1, p2: abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

            if (move[0], move[1]) in cache:
                total = cache[(move[0], move[1])]
            else:
                # +2,3,7,50 if moves next to king         Done
                # +4 if move in king's line of movement   Done
                # +1 if on side of board               Done
                # +4 if move captures a piece             Done
                # +1 if piece is near enemy (not king)    Done
                # -1 if move is near enemy (not king)     Done
                # -7 if piece is near king already        Done
                # -9 if move gets piece captured          Done

                g = deepcopy(grid)
                g[move[1]][move[0]] = g[p.pos[1]][p.pos[0]]
                g[move[1]][move[0]].pos = move
                g[p.pos[1]][p.pos[0]] = None

                lst = list(filter(lambda x: dis(x.pos, move) == 1, getDefenders(grid)))

                canCapture = False
                if not all([x.isSafe(g) for x in lst]):
                    total += 4
                    canCapture = True

                newP = deepcopy(p)
                newP.pos = move
                if not newP.isSafe(g) and not canCapture:
                    total -= 9

                if len([x for x in getAdjacent(grid, p.pos) if
                        x != None and x.side == "Defender" and not x.isKing]) >= 1:
                    total += 1

                if len([x for x in getAdjacent(grid, move) if
                        x != None and x.side == "Defender" and not x.isKing]) >= 1:
                    total -= 1

                if dis(k.pos, p.pos) == 1:
                    total -= 7

                if dis(k.pos, move) == 1:
                    n = getNumAdjacent(g, k.pos, "Attacker")
                    total += 2 if n == 1 else 3 if n == 2 else 7 if n == 3 else 50
                else:
                    if (move[0], move[1]) in kMoves:
                        total += 4 + (min(
                            [dis((0, 0), move), dis((10, 0), move), dis((0, 10), move), dis((10, 10), move)]) / 10)
                        if any([x in move for x in [0, 1, 9, 10]]):
                            total += 1

            cache[(move[0], move[1])] = total
            moves.append((p.pos, move, total))
    m = max(moves, key=lambda x: x[2])[2]
    moves = list(filter(lambda x: x[2] == m, moves))

    # pick a random move
    choice = moves[randint(0, len(moves) - 1)]
    animateMove(window, grid, choice[0], choice[1])
    updatePieces(grid, choice[1])


def getAdjacent(grid, p):
    up = None
    down = None
    left = None
    right = None

    if p[1] < 10:
        up = grid[p[1] + 1][p[0]]
    if p[1] > 0:
        down = grid[p[1] - 1][p[0]]
    if p[0] > 0:
        left = grid[p[1]][p[0] - 1]
    if p[0] < 10:
        right = grid[p[1]][p[0] + 1]

    return [up, down, left, right]


def getNumAdjacent(grid, p, side):
    return len([x for x in getAdjacent(grid, p) if x != None and x.side == side])


def close():
    pass


window = GraphWin("Hnefatafl", wSize[0], wSize[1], autoflush=False)
window.setBackground("white")
window.bind("<Motion>", motion)
window.bind("<MouseWheel>", mouse_wheel)

state = "Menu"
menuState = "Menu"
board = ""
winner = None

gameMode = 2
sideChoice = "Attacker"
startTime = 0
endTime = 0
numMoves = 0
while True:
    if state == "Menu":
        clear(window)

        squares = []
        switch = 1
        for y in range(0, 1104, 46):
            switch *= -1
            for x in range(-552, 552, 46):
                if switch == 1:
                    squares.append(createBackgroundSquare(window, (x, y)))
                switch *= -1

        while True:
            animateBackground(window, squares)
            if menuState == "Menu":
                createMenuGUI(window)
            else:
                createRulesGUI(window)

            update(60)
            click = window.checkMouse()
            if click != None:
                click = (click.getX(), click.getY())
                if menuState == "Menu":
                    if rectContains((40, 160), (210, 185), click):
                        gameMode = 1
                        state = "Board Select"
                        break
                    if rectContains((40, 215), (210, 235), click):
                        gameMode = 2
                        state = "Board Select"
                        break
                    if rectContains((40, 260), (230, 285), click):
                        state = "Creator"
                        break
                    if rectContains((40, 315), (125, 335), click):
                        menuState = "Rules"
                        clear(window, ["Rectangle"])
                        break
                else:
                    if rectContains((0, 0), (50, 24), click):
                        menuState = "Menu"
                        break
    elif state == "Game":
        clear(window)
        turn = "Attacker"
        startTime = time()
        grid = [[None for i in range(11)] for j in range(11)]
        loadBoard(grid, board)
        while True:
            drawBoard(window, grid, side=turn)

            if gameMode == 2 or turn == sideChoice:
                click1 = getPosFromClick(window.getMouse())
                if -1 not in click1:
                    p = grid[click1[1]][click1[0]]
                    if p != None:
                        if p.side == turn:
                            moves = showMoves(window, p, grid)
                            click2 = getPosFromClick(window.getMouse())
                            if click2 in moves:
                                animateMove(window, grid, click1, click2)
                                updatePieces(grid, click2)
                                numMoves += 1
                                turn = "Defender" if turn == "Attacker" else "Attacker"
            else:
                if sideChoice == "Attacker":
                    defenderAI(window, grid)
                else:
                    attackerAI(window, grid)
                numMoves += 1
                turn = "Defender" if turn == "Attacker" else "Attacker"

            lst = getKing(grid)
            numAttackers = len(getAttackers(grid))
            # end conditions
            if len(lst) == 0:
                drawBoard(window, grid)
                winner = "Attacker"
                state = "End"
                break
            elif lst[0].pos in [(0, 0), (0, 10), (10, 0), (10, 10)] or numAttackers == 0:
                drawBoard(window, grid)
                winner = "Defender"
                state = "End"
                break
    elif state == "Creator":
        clear(window)
        grid = [[0 for i in range(11)] for j in range(11)]
        grid[5][5] = 3
        while True:
            drawBoard(window, convertGrid(grid), False, ["Entry"])
            drawCreatorGUI(window)
            click = window.getMouse()
            if rectContains((0, 0), (50, 24), (click.getX(), click.getY())):
                state = "Menu"
                break
            pos = getPosFromClick(click)
            if -1 not in pos and pos not in [(0, 0), (0, 10), (10, 0), (10, 10), (5, 5)]:
                grid[pos[1]][pos[0]] = (grid[pos[1]][pos[0]] + 1) % 3
            if rectContains((400, 510), (500, 544), (click.getX(), click.getY())):
                result = validateBoard(grid)
                entry = list(filter(lambda x: str(x.__class__.__name__) == "Entry", window.items[:]))[0]
                if all(result) and 0 < len(entry.getText()) <= 12 and entry.getText()[0] != "-":
                    fname = entry.getText()
                    entry.setText("-saved")
                    saveGrid(grid, fname)
                else:
                    error = ""
                    if not result[0]:
                        error = "-Need 2 times more attackers then defenders"
                    elif not result[1]:
                        error = "-Captured piece positions detected"
                    elif len(entry.getText()) == 0 or entry.getText()[0] == "-":
                        error = "-Please enter a file name"
                    elif len(entry.getText()) > 12:
                        error = "-File name cannot exceed 12 characters"
                    else:
                        error = "-Unknown Error"
                    entry.setText(error)
    elif state == "Board Select":
        scrollCount = 0
        lst = generateBoardSelections(getBoards())
        br = True
        while br:
            clear(window)
            drawBoardSelect(window, lst, scrollCount)
            click = window.checkMouse()
            if click != None:
                for b in lst:
                    if rectContains((b.pos[0], b.pos[1]), (b.pos[0] + 170, b.pos[1] + 182),
                                    (click.getX(), click.getY())):
                        state = "Game" if gameMode == 2 else "Side Select"
                        board = b.fname.replace(".txt", "")
                        br = False
                        break
    elif state == "Side Select":
        while True:
            clear(window)
            drawSideSelect(window)
            click = window.checkMouse()

            if click != None:
                if inCircle((click.getX(), click.getY()), (145, 400), 120):
                    sideChoice = "Attacker"
                    state = "Game"
                    break
                if inCircle((click.getX(), click.getY()), (407, 400), 120):
                    sideChoice = "Defender"
                    state = "Game"
                    break

    elif state == "End":
        sleep(1)

        clear(window)
        drawEndScreen(window, winner, time() - startTime, numMoves)
        sleep(5)

        state = "Menu"
        numMoves = 0
        dCollected = 0
        aCollected = 0

        clear(window)