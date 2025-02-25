import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

w_width, w_height = 1000, 1000
display = (w_width, w_height)

pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

vertex_shader_txt = """#version 330 core
in vec3 vertex_position;
out vec2 fragCoord;
void main()
{
    gl_Position = vec4(vertex_position, 1.0);
    fragCoord = vertex_position.xy;
}
"""

fragment_shader_txt = """#version 330 core
#define MAX_STEPS 100
#define MAX_DIST 1000.
#define SURF_DIST .01

uniform float iTime;
uniform vec3 iResolution;
uniform vec3 cpos;
uniform vec2 mo;

in vec2 fragCoord;
out vec4 fragColor;

mat3 setCamera( in vec3 ro, in vec3 ta, float cr )
{
	vec3 cw = normalize(ta-ro);
	vec3 cp = vec3(sin(cr), cos(cr),0.0);
	vec3 cu = normalize( cross(cw,cp) );
	vec3 cv =          ( cross(cu,cw) );
    return mat3( cu, cv, cw );
}

float distance_from_sphere(in vec3 point, in vec3 center, float radius)
{
    return length(point - center) - radius;
}

float map(in vec3 point)
{
    return distance_from_sphere(point, vec3(0.0, 0.0, 0.0), 0.2);
}
vec3 calculate_normal(in vec3 pos)
{
#if 0
    vec2 e = vec2(1.0,-1.0)*0.5773*0.0005;
    return normalize( e.xyy*map( pos + e.xyy ) + 
					  e.yyx*map( pos + e.yyx ) + 
					  e.yxy*map( pos + e.yxy ) + 
					  e.xxx*map( pos + e.xxx ) );
#else
    // inspired by tdhooper and klems - a way to prevent the compiler from inlining map() 4 times
    vec3 n = vec3(0.0);
    for( int i=0; i<4; i++ )
    {
        vec3 e = 0.5773*(2.0*vec3((((i+3)>>1)&1),((i>>1)&1),(i&1))-1.0);
        n += e*map(pos+0.0005*e);
      //if( n.x+n.y+n.z>100.0 ) break;
    }
    return normalize(n);
#endif  
}
float get_light(in vec3 pos, in vec3 light_pos)
{
    vec3 to_light = pos - light_pos;
    vec3 norm = calculate_normal(pos);
    float brightness = dot(normalize(to_light), norm);
    return 5. * brightness/dot(to_light, to_light);
}
vec3 raymarch(in vec3 ray_origin, in vec3 ray_direction)
{
    float total_distance_travelled = 0.0;
    const int NUMBER_OF_STEPS = 32;
    const float MINIMUM_HIT_DISTANCE = 0.001;
    const float MAXIMUM_TRACE_DISTANCE = 1000.0;
    
    for (int i = 0; i < NUMBER_OF_STEPS; i++) 
    {
        vec3 current_position = ray_origin + total_distance_travelled * ray_direction;
        float closest_distance = map(current_position);
        if(closest_distance < MINIMUM_HIT_DISTANCE) 
        {
            //hit!
            return vec3(1.) * get_light(current_position, vec3(2.0, 3.0, 1.0));
        }
        
        if (total_distance_travelled > MAXIMUM_TRACE_DISTANCE) 
        {
            break;
        }
        
        total_distance_travelled += closest_distance;
    }
    //miss...
    return vec3(0.);
}
void main()
{
    vec3 camera_position = vec3(0.0, 0.0, -5.0);
    vec3 ta = vec3(0.25, -0.75, -0.75 );
    vec3 ro = ta - cpos + vec3(4.5*cos(7.0*mo.x), 0, 4.5*sin(7.0*mo.x));
    mat3 ca = setCamera( ro, ta, 0.0 );
    
    vec3 rd = ca * normalize( vec3(fragCoord, 2.5) );
    fragColor = vec4(raymarch(ro, rd), 1.0);
}
"""
program = glCreateProgram()
vertex = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)

glShaderSource(vertex, vertex_shader_txt)
glCompileShader(vertex)

log = glGetShaderInfoLog(vertex)
if isinstance(log, bytes):
    log = log.decode()
for line in log.split("\n"):
    print(line)

glAttachShader(program, vertex)
glShaderSource(fragment, fragment_shader_txt)
glCompileShader(fragment)

log = glGetShaderInfoLog(fragment)
if isinstance(log, bytes):
    log = log.decode()
for line in log.split("\n"):
    print(line)

glAttachShader(program, fragment)
glValidateProgram(program)
glLinkProgram(program)
log = glGetProgramInfoLog(program)
if isinstance(log, bytes):
    log = log.decode()
for line in log.split("\n"):
    print(line)


glUseProgram(program)

#gluPerspective(45.0, (w_width/float(w_height)), 0.1, 50.0)
#glTranslatef(0.0, 0.0, -10)

#texture = glGenTextures(1)
#image = pygame.image.load('../../resources/test/718smiley.png')
#img_raw = pygame.image.tostring(image, 'RGBA', 1)
#i_width, i_height = image.get_width(), image.get_height()

glClearColor(1, 0, 0, 0)

#glBindTexture(GL_TEXTURE_2D, texture)
#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, i_width, i_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_raw)
i_time = 0.0
i_resolution = display
x_pos = 0.0
y_pos = 0.0
z_pos = 0.0
mouse_pos = (0, 0)

res_loc = glGetUniformLocation(program, "iResolution")
time_loc = glGetUniformLocation(program, "iTime")
cpos_loc = glGetUniformLocation(program, "cpos")
mouse_loc = glGetUniformLocation(program, "mo")
speed = 0.2
while True:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                quit()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_a:
                        x_pos += speed
                    case pygame.K_e:
                        y_pos += speed
                    case pygame.K_s:
                        z_pos += speed
                    case pygame.K_d:
                        x_pos -= speed
                    case pygame.K_q:
                        y_pos -= speed
                    case pygame.K_w:
                        z_pos -= speed
            case pygame.MOUSEMOTION:
                (x, y) = pygame.mouse.get_pos()
                mouse_pos = ((2 * x / float(i_resolution[0]) - 0.5), (2 * y / float(i_resolution[1]) - 0.5))



    glUniform3f(res_loc, i_resolution[0], i_resolution[1], 0.0)
    glUniform1f(time_loc, 0.0)
    glUniform3f(cpos_loc, x_pos, y_pos, z_pos)
    glUniform2f(mouse_loc, mouse_pos[0], mouse_pos[1])
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_QUADS)
    glVertex3f(-1, -1, 0)
    glVertex3f(1, -1, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(-1, 1, 0)
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)