#Andres Emilio Quinto Villagran
#Carne 18288

import struct

def char(myChar):
		return struct.pack('=c', myChar.encode('ascii'))

def word(myChar):
	return struct.pack('=h', myChar)
	
def dword(myChar):
	return struct.pack('=l', myChar)

def normalizeColorArray(colors_array):
    return [round(i*255) for i in colors_array]

def color(r,g,b):
	return bytes([b, g, r])

Dark = color(0,0,0)

class Render(object):
    
    def __init__(self):
        self.framebuffer = []
        self.width = 500
        self.height = 500
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = 500
        self.viewport_height = 500
        # Para el poligono actual
        self.polygon_coords = []

        self.glClear()

    # Colocar el pixel en la coordenada proporcionada
    def point(self, x, y):
        self.framebuffer[y][x] = self.color

    
    def glCreateWindow(self, width, height):
        self.height = height
        self.width = width

    
    def glViewport(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_height = height
        self.viewport_width = width

    def glClear(self):
        self.framebuffer = [
            [Dark for x in range(self.width)] for y in range(self.height)
        ]

    
    def glClearColor(self, r=1, g=1, b=1):
        normalized = normalizeColorArray([r,g,b])
        clearColor = color(normalized[0], normalized[1], normalized[2])

        self.framebuffer = [
            [clearColor for x in range(self.width)] for y in range(self.height)
        ]

    def glVertex(self, x, y):
        final_x = round((x+1) * (self.viewport_width/2) + self.viewport_x)
        final_y = round((y+1) * (self.viewport_height/2) + self.viewport_y)
        self.point(final_x, final_y)


    def glColor(self, r=0, g=0, b=0):
        normalized = normalizeColorArray([r,g,b])
        self.color = color(normalized[0], normalized[1], normalized[2])

    def glCoordinate(self, value, is_vertical):
        real_coordinate = ((value+1) * (self.viewport_height/2) + self.viewport_y) if is_vertical else ((value+1) * (self.viewport_width/2) + self.viewport_x)
        return round(real_coordinate)

    # Dibujamos el pligono en una linea de vertices
    def glDrawPolygon(self, vertices):
        self.polygon_coords = vertices
        vcount = len(vertices)

        for limit in range(vcount):
            v1 = vertices[limit]
            v2 = vertices[(limit + 1) % vcount]
            self.glLine(v1[0], v1[1], v2[0], v2[1])

    # Codigo que optimiza el relleno de los poligonos referencia de la clase.
    def calculateVertices(self, poly_x_coords, poly_y_coords): 
        constants = []
        multipliers = []

        count_vertices = len(self.polygon_coords)
        limit = count_vertices - 1;

        for i in range(count_vertices):
            if(poly_y_coords[limit] == poly_y_coords[i]):
                constants.append(poly_x_coords[i])
                multipliers.append(0)
            else:
                constants.append(poly_x_coords[i] - (poly_y_coords[i] * poly_x_coords[limit]) / (poly_y_coords[limit] - poly_y_coords[i]) + (poly_y_coords[i] * poly_x_coords[i]) / (poly_y_coords[limit] - poly_y_coords[i]))
                multipliers.append((poly_x_coords[limit] - poly_x_coords[i]) / (poly_y_coords[limit] - poly_y_coords[i])) 

            limit = i;
            
        return (constants, multipliers)
    
    def isInsidePoly(self, x, y):
        poly_x_coords = [axis[0] for axis in self.polygon_coords]
        poly_y_coords = [axis[1] for axis in self.polygon_coords]

        (constants, multipliers) = self.calculateVertices(poly_x_coords, poly_y_coords)

        is_poly_inside = False
        count_vertices = len(self.polygon_coords)
        current_node = poly_y_coords[count_vertices - 1] > y
        
        for i in range(count_vertices):
            previous_node = current_node
            current_node = poly_y_coords[i] > y; 
            if (current_node != previous_node):
                is_poly_inside ^= y * multipliers[i] + constants[i] < x
        
        return is_poly_inside
        
    def glFillPolygon(self):
        x_min = min(self.polygon_coords, key = lambda i : i[0])[0]
        y_min = min(self.polygon_coords, key = lambda i : i[1])[1]
        
        x_max = max(self.polygon_coords, key = lambda i : i[0])[0]
        y_max = max(self.polygon_coords, key = lambda i : i[1])[1]
        
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):                 
                if self.isInsidePoly(x, y):
                    self.point(x,y) 
    
    def glLine(self, x0, y0, x1, y1) :

        steep = abs(y1 - y0) > abs(x1 - x0)

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0 
        y = y0
        threshold =  dx

        for x in range(x0, x1):
            self.point(y, x) if steep else self.point(x, y)
            
            offset += 2*dy

            if offset >= threshold:
                y += -1 if y0 > y1 else 1
                threshold += 2*dx
                

    def glFinish(self, filename='output.bmp'):
        # starts creating a new bmp file
        f = open(filename, 'bw')

        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # finishing placing points
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()