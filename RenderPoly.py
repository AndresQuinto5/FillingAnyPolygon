#Andres Emilio Quinto Villagran
#carne 18288
#Filling any polygon


from gl import Render

Dark = (0, 0, 0)

render = Render()

render.glCreateWindow(900, 500) # Screen size
render.glClearColor(0, 0, 0) 


render.glColor(0, 0.254, 0.255) 
render.glDrawPolygon([(165, 380),(185, 360),(180, 330),(207, 345),(233, 330),(230, 360),(250, 380),(220, 385),(205, 410),(193, 383)])
render.glFillPolygon()
render.glColor(0, 0.255, 0.255) 

render.glDrawPolygon([(321, 335),(288, 286),(339, 251),(374, 302)])
render.glFillPolygon()
render.glColor(0, 0.255, 0.255) 
render.glDrawPolygon([(377, 249),(411, 197),(436, 249)])
render.glFillPolygon()

render.glColor(0.255, 0.255, 0.1) 
render.glDrawPolygon([(413, 177),(448, 159),(502, 88),(553, 53),(535, 36),(676, 37),(660, 52),(750, 145),(761, 179),(672, 192),(659, 214),(615, 214),(632, 230),(580, 230),(597, 215),(552, 214),(517, 144),(466, 180)])
render.glFillPolygon()

render.glColor(0,0,0)
render.glDrawPolygon([(682, 175),(708, 120),(735, 148),(739, 170)])
render.glFillPolygon()

render.glFinish()