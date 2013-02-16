import pyglet
from pyglet.gl import *
from gletools import ShaderProgram, FragmentShader, VertexShader


class Knot_Display(pyglet.window.Window):

    def __init__(self, **kwargs):
        super(Knot_Display, self).__init__(**kwargs)

        self.t = 0.0

        self.program = ShaderProgram(
            FragmentShader('out vec4 outputColor; void main() { outputColor = vec4(1,1,1,1); }'),
            VertexShader('''layout(location = 0) in vec2 position;
                          void main() { 
                              vec4 p = vec4(position.x, position.y, cos(position.x*10)*cos(position.y*10) * 0.2, 1);
                              gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * p; 
                          }''')
        )

    def init_grid(self, points):
        point_data = [ coord for point in points for coord in point ]

        num_coords = len(point_data)
        pointsGl = (GLfloat * num_coords)(*point_data)
        self.vbo = pyglet.graphics.vertexbuffer.create_buffer(
            num_coords*4, GL_ARRAY_BUFFER, GL_STATIC_DRAW)
        self.vbo.set_data(pointsGl)

    def update(self, dt):
        self.t += dt

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(50, width / float(height), .01, 100)
        glMatrixMode(GL_MODELVIEW)
        return pyglet.event.EVENT_HANDLED

    def on_draw(self):
        self.clear()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(0, 0, -2.0)
        glRotatef(self.t*40, 0.0, 1.0, 0.0)
        glTranslatef(-0.5, -0.5, 0)
        glPointSize(2)
        with self.program:
            self.vbo.bind()
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0)
            glDrawArrays(GL_POINTS, 0, 10000)
            glDisableVertexAttribArray(0)
            self.vbo.unbind()
        glPopMatrix()


def main():

    def _create_grid(width, height):
        grid = []
        columns = [ float(x)/width for x in range(width) ]
        rows = [ float(y)/height for y in range(height) ]
        for r in rows:
            for c in columns:
                grid.append((r,c))
        return grid


    config = pyglet.gl.Config(sample_buffers=1, samples=4)
    window = Knot_Display(caption='Knotviz in the house', resizable=True, vsync=True, config=config)

    points = _create_grid(100, 100)
    window.init_grid(points)

    pyglet.clock.schedule_interval(window.update, (1.0/60))
    pyglet.app.run()

if __name__ == '__main__': main()
