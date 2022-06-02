import numpy as np
from PIL import Image
from PIL import ImageDraw


RECT_SIZE = [100,100] #shape max size
AMT = 2 #number of shapes
IMG_SIZE = (1000, 1000) #image size

#funtions for matrix transformation
def f(x):
    return x**np.sqrt(np.sqrt(x)%4)
def d(x):
    return np.sin(x % (x**2+0.001))*np.sqrt(x)
def a(x):
    return np.sqrt(f(x)/np.cos(d(x)))

#generate sample point of shape
def expand_rect(rect, points = 10000):
    lower, upper, right, left = [], [], [], []
    step_x, step_y = rect[0]/points, rect[1]/points

    for i in range(points):
        lower.append([step_x*i,0])
        upper.append([step_x*i,rect[1]])
        right.append([0,step_y*i])
        left.append([rect[0],step_y*i])
    return [lower,upper,right,left]

#compute transformed points
def comp_shear(sides):
    pad_x, pad_y = IMG_SIZE[0]/2 - RECT_SIZE[0]/2, IMG_SIZE[1]/2 - RECT_SIZE[1]/2
    for side in sides:
        for val in side:
            e = np.random.randint(1,3)
            #differnt x -> T(x)
            if e == 1:
                xval = int(np.random.random(1)*np.random.randint(-1,1)*val[0]+np.random.randint(-1,1)*f(val[1])) + pad_x
                yval = int(np.random.random(1)*np.random.randint(-3,3)*d(f(val[0]))+np.random.randint(-1,1)*val[1]) + pad_y
                val[0],val[1]=xval,yval
            elif e==2:
                xval = int(np.random.random(1)*np.random.randint(-2,2)*f(val[0])-np.cos(d(val[1]))) + pad_x
                yval = int(np.random.randint(-1,1)*f(val[0])+np.random.random(1)*np.random.randint(-1,1)*val[1]) + pad_y
                val[0],val[1]=xval,yval
            else:
                xval = int(0.5*d(val[0])+np.random.randint(-1,1)*a(val[1])) + pad_x
                yval = int(np.random.randint(-1,1)*val[0]-np.random.random(1)*np.random.randint(-2,2)*val[1]) + pad_y
                val[0],val[1]=xval,yval
    return sides

#convert array of lists into array of tuples - for pil drawinf
def make_tuple_arr(arr):
    tuples = []
    for side in arr:
        tuple_side = []
        for val in side:
            tuple_side.append(tuple(val))
        tuples.append(tuple_side)
    return tuples

#draw transparent lines
def draw_transp(image,xy, color, width = 2,joint = "curve"):
    overlay = Image.new('RGBA', IMG_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.line(xy, color, width, joint)
    image.alpha_composite(overlay)

#draw final image
def draw_shape(shapes ,colors = ["red","green"]):
    image = Image.new("RGBA", IMG_SIZE, "black")
    for i,shape in enumerate(shapes):
        for side in shape:
            draw_transp(image,side,colors[i],3,"curve")
    image.save("image.png")


#generate random colors + alpha
colors = [tuple(np.append(np.random.choice(range(10,256),size = (3)),np.random.choice(range(100,200), size=1))) for i in range(AMT)]


#generate random shapes
shapes = []
for i in range(AMT):
    rect_size = [np.random.randint(0,RECT_SIZE[0]), np.random.randint(0,RECT_SIZE[1])]
    sides = expand_rect(rect_size)
    t_c_sides = make_tuple_arr(comp_shear(sides))
    shapes.append(t_c_sides)


draw_shape(shapes,colors)
