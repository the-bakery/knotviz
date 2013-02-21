import pyglet
from pyglet.gl import *
from gletools import ShaderProgram, FragmentShader, VertexShader

from VQM import *
from Grid import *


class Knot_Display(pyglet.window.Window):

    def __init__(self, **kwargs):
        super(Knot_Display, self).__init__(**kwargs)
        self.t = 0.0
        self.orientation = Quat(1, Vec3(0,0,0))
        self.zoom = 1.0

        self.grid = Grid(100, 100)


        self.program = ShaderProgram(
            FragmentShader('''#version 130
                              uniform float pi;
                              varying vec2 uv;
                              float tf(float f) { return 0.5*sin(20*pi*f) + 0.5; }
                              out vec4 outputColor; void main() {
                                outputColor = true /* gl_FrontFacing */ ?
                                  vec4(tf(uv.x), tf(uv.y), 0, 1) :
                                  vec4(1, 1 - tf(uv.x), 1 - tf(uv.y), 1); }'''),
            VertexShader('''#version 130
                            uniform float pi = 3.14159;
                            /* layout(location = 0) */ in vec2 param;
                            varying vec2 uv;
                            vec4 torus(float v25, float v26) { return vec4(((2.00000000000000 * cos((6.28318520000000 * v25))) + (-1.00000000000000 * cos((6.28318520000000 * v25)) * cos((6.28318520000000 * v26)))), ((2.00000000000000 * sin((6.28318520000000 * v25))) + (-1.00000000000000 * cos((6.28318520000000 * v26)) * sin((6.28318520000000 * v25)))), (1.00000000000000 * sin((6.28318520000000 * v26))), 1.0); }
                            //vec4 knot(float v15, float v16) { return vec4(((-1.00000000000000 * cos((18.8495556000000 * v15)) * cos((12.5663704000000 * v15))) + (2.00000000000000 * cos((12.5663704000000 * v15)))), ((2.00000000000000 * sin((12.5663704000000 * v15))) + (-1.00000000000000 * cos((18.8495556000000 * v15)) * sin((12.5663704000000 * v15)))), (1.00000000000000 * sin((18.8495556000000 * v15))), 1.0); }
                            void main() {
                                vec4 p = torus(param.x, param.y);
                                //vec4 p = knot(param.x, param.y);
                                //vec4 p = vec4(param.x, param.y, 0, 1);
                                uv = param.xy;
                                gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * p;
                            }''')
        )

    def update(self, dt):
        self.t += dt

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(50, width / float(height), .01, 100)
        glMatrixMode(GL_MODELVIEW)

        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        return pyglet.event.EVENT_HANDLED

    def on_mouse_press(self, x, y, button, modifiers):
        # self.set_exclusive_mouse()
        return

    def on_mouse_release(self, x, y, button, modifiers):
        # self.set_exclusive_mouse(exclusive=False)
        return


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # rotate on left-drag
        if buttons & 1:
            # the rotation vector is the displacement vector rotated by 90 degrees
            v = Vec3(dy, -dx, 0).scale(0.002)
            # update the current orientation
            self.orientation = self.orientation * v.rotation()
        # zoom on right-drag
        if buttons & 4:
            self.zoom += self.zoom * dy*0.01

    def on_draw(self):
        self.clear()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(0, 0, -7.0)
        glScalef(self.zoom, self.zoom, self.zoom)

        r = self.orientation.conj().matrix()
        # column-major order
        m = [r.X.x, r.X.y, r.X.z, 0,
             r.Y.x, r.Y.y, r.Y.z, 0,
             r.Z.x, r.Z.y, r.Z.z, 0,
                 0,     0,     0, 1,]
        array = (GLfloat * len(m))()
        for index, value in enumerate(m):
            array[index] = value
        glMultMatrixf(array);

        glPointSize(1.8)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        with self.program:
            self.grid.draw_triangles()
        glPopMatrix()


def main():

    config = pyglet.gl.Config(sample_buffers=1, samples=4)
    window = Knot_Display(caption='Knotviz in the house', resizable=True, vsync=True, config=config)

    pyglet.clock.schedule_interval(window.update, (1.0/60))
    pyglet.app.run()

if __name__ == '__main__': main()
