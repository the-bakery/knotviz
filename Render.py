import pyglet
from pyglet.gl import *
from gletools import ShaderProgram, FragmentShader, VertexShader

from VQM import *


class Knot_Display(pyglet.window.Window):

    def __init__(self, **kwargs):
        super(Knot_Display, self).__init__(**kwargs)

        self.gridwidth = 100
        self.gridheight = 100

        def _create_grid(width, height):
            columns = [ float(x)/width for x in range(width) ]
            rows = [ float(y)/height for y in range(height) ]
            for r in rows:
                for c in columns:
                    yield r
                    yield c

        self.vertex_list = pyglet.graphics.vertex_list(self.gridwidth * self.gridheight, 'v2f')
        self.vertex_list.vertices = list(_create_grid(self.gridwidth, self.gridheight))


        self.t = 0.0
        self.orientation = Quat(1, Vec3(0,0,0))

        self.program = ShaderProgram(
            FragmentShader('''#version 130
                              out vec4 outputColor; void main() { outputColor = vec4(1,1,1,1); }'''),
            VertexShader('''#version 130
                            uniform float pi = 3.14159;
                            /* layout(location = 0) */ in vec2 param;
                            vec4 torus(float v25, float v26) { return vec4(((2.00000000000000 * cos((6.28318520000000 * v25))) + (-1.00000000000000 * cos((6.28318520000000 * v25)) * cos((6.28318520000000 * v26)))), ((2.00000000000000 * sin((6.28318520000000 * v25))) + (-1.00000000000000 * cos((6.28318520000000 * v26)) * sin((6.28318520000000 * v25)))), (1.00000000000000 * sin((6.28318520000000 * v26))), 1.0); }
                            void main() {
                                vec4 p = torus(param.x, param.y);
                                //vec4 p = vec4(sin(pos.x)*cos(pos.y), sin(pos.y), cos(pos.x)*cos(pos.y), 1/pos.x + 2*pi);
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
        return pyglet.event.EVENT_HANDLED

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # the rotation vector is the displacement vector rotated by 90 degrees
        v = Vec3(dy, -dx, 0).scale(0.002)
        # update the current orientation
        self.orientation = self.orientation * v.rotation()

    def on_draw(self):
        self.clear()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(0, 0, -7.0)

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
        with self.program:
            self.vertex_list.draw(GL_POINTS)
        glPopMatrix()


def main():



    config = pyglet.gl.Config(sample_buffers=1, samples=4)
    window = Knot_Display(caption='Knotviz in the house', resizable=True, vsync=True, config=config)


    pyglet.clock.schedule_interval(window.update, (1.0/60))
    pyglet.app.run()

if __name__ == '__main__': main()
