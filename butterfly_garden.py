from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
import math

#window size
WIDTH =900
HEIGHT = 650

# BUTTERFLY:X, Y , SPEED, COLOR, PHASE
butterflies = [
    [-0.8, 0.45, 0.008, (1.0, 0.35, 0.05), 0 ],
    [-0.3, 0.15, 0.006, (0.8, 0.1, 0.8), 1],
    [0.4, 0.4, 0.007, (1.0,0.2,0.5), 2]
]

#cloud positions
clouds = [-0.7, 0.1, 0.7 ]

def circle(x, y, r):
    glBegin(GL_POLYGON)

    for i in range(360):
        angle = math.radians(i)
        glVertex2f(
            x+r*math.cos(angle),
            y+r*math.sin(angle)
        )
    glEnd()

def ellipse(x, y , rx, ry):
    glPushMatrix()
    glTranslatef(x, y , 0)
    glScalef(rx, ry, 1)
    circle(0, 0 ,1)
    glPopMatrix()

def draw_cloud(x, y):
    glColor3f(1, 1, 1)
    circle(x, y, 0.07)
    circle(x+0.08, y+0.04, 0.09)
    circle(x+0.17, y, 0.07)
    circle(x+0.09, y- 0.02, 0.08)

def draw_sun():
    glColor3f(1.0, 0.85, 0.0)
    circle(0.78, 0.78, 0.13)

def draw_tree(x):
    #tree trunk
    glColor3f(0.4, 0.2, 0.05)

    glBegin(GL_QUADS)
    glVertex2f(x - 0.04, -0.65)
    glVertex2f(x + 0.04, -0.65)
    glVertex2f(x + 0.04, 0.05)
    glVertex2f(x - 0.04, 0.05)
    glEnd()

    #tree leaves
    glColor3f(0.0, 0.5, 0.1)

    circle(x, 0.12, 0.19)
    circle(x-0.12, 0.05, 0.15)
    circle(x+0.12, 0.05, 0.15)

#draw flower
def draw_flower(x, y, color):
    #stem
    glColor3f(0.0, 0.5, 0.0)

    glLineWidth(3)

    glBegin(GL_LINES)
    glVertex2f(x,y)
    glVertex2f(x, y - 0.18)
    glEnd()

    #petals
    glColor3f(*color)

    circle(x, y+0.05, 0.035)
    circle(x - 0.05, y, 0.035)
    circle(x + 0.05, y, 0.035)
    circle(x, y - 0.04, 0.035)

    #center
    glColor3f(1.0, 0.8, 0.0)
    circle(x, y, 0.025)

#draw butterfly
def draw_butterfly(x, y, color, phase):
    #wing movement
    wing = 0.4 + 0.6 * abs(math.sin(phase))

    glPushMatrix()
    glTranslatef(x, y, 0)

    #left wing
    glColor3f(*color)
    ellipse(-0.065, 0, 0.075 * wing, 0.10)

    #right wing
    ellipse(0.065, 0, 0.075*wing, 0.10)

    #butterfly body
    glColor3f(0.05, 0.05, 0.05)
    ellipse(0, 0, 0.018, 0.09)

    #head
    circle(0, 0.09, 0.025)

    #antennae
    glLineWidth(2)

    glBegin(GL_LINES)
    glVertex2f(-0.01, 0.10)
    glVertex2f(-0.04, 0.16)
    glVertex2f(0.01, 0.10)
    glVertex2f(0.04, 0.16)
    glEnd()

    glPopMatrix()

#display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    #sky
    glColor3f(0.3, 0.7, 1.0)

    glBegin(GL_QUADS)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    glVertex2f(1, 1)
    glVertex2f(-1, 1)
    glEnd()

    #sun
    draw_sun()

    #clouds
    for x in clouds:
        draw_cloud(x, 0.72)

    #green ground
    glColor3f(0.1, 0.55, 0.15)

    glBegin(GL_QUADS)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    glVertex2f(1, -0.65)
    glVertex2f(-1, -0.65)
    glEnd()

    #trees
    draw_tree(-0.82)
    draw_tree(0.85)

    #flowers
    draw_flower(-0.65, -0.72, (1.0, 0.2, 0.4) )
    draw_flower(-0.3, -0.75, (1.0, 0.8, 0.1) )
    draw_flower(0.1, -0.72, (0.9, 0.2, 0.8) )
    draw_flower(0.45, -0.75, (1.0, 0.3, 0.2) )
    draw_flower(0.75, -0.72, (1.0, 0.8, 0.2) )

    #butterflies
    for b in butterflies:
        draw_butterfly(b[0], b[1], b[3], b[4])

    glutSwapBuffers()

#animation function
def update(value):
    #move butterflies
    for b in butterflies:
        b[0] += b[2]
        b[4] += 0.2

        #up down movement
        b[1] = b[1] + 0.002 * math.sin(b[4])
        #retuen to position
        if b[0] > 1.2:
            b[0] = -1.2

    #move clouds
    for i in range(len(clouds)):
        clouds[i] += 0.002
        if clouds[i] > 1.2:
            clouds[i] = -1.2

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

#initialization
def init():
    glClearColor(0.3, 0.7, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)

#main function
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WIDTH, HEIGHT)
glutInitWindowPosition(100, 50)
glutCreateWindow(b"butterfly_garden")
init()
glutDisplayFunc(display)
glutTimerFunc(0, update, 0)
glutMainLoop()

