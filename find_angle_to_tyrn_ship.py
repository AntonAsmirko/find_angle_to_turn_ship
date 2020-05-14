import math
import cmath

enemy = []
ship = []
ship_direction = []
mast_vector = []
ship_plus_direction = []
is_left = False
gun_angle = None
mast_angle = None
right_gun_vector = None
dist_vector = None

def read_input():
    file = open('input.txt')
    lines = file.readlines()
    global ship
    ship = list(float(i) for i in filter(lambda x : x != '', lines[0].split(' ')))
    global ship_direction
    ship_direction = [float(i) for i in filter(lambda x : x != '', lines[1].split(' '))]
    global mast_vector
    mast_vector = [float(i) for i in filter(lambda x : x != '',lines[2].split(' '))]
    global enemy
    enemy = [float(i) for i in filter(lambda x : x != '', lines[3].split(' '))]
    file.close()

def mat_sum(x, y):
    c = []
    for i, j in zip(x, y):
        c.append(i+j);
    return c

def scalar_mult(a, b):
    sum = 0;
    for i, j in zip(a, b):
        sum = sum+i*j
    return sum

def const_mult(a, b):
    c = []
    for i in a:
        c.append(i*b)
    return c

def vector_mult(a, b):
    return [a[1]*b[2]-a[2]*b[1], -1*(a[0]*b[2]-a[2]*b[0]), a[0]*b[1]-a[1]*b[0]]


def calculate_right_gun_vector():
    global right_gun_vector
    right_gun_vector = vector_mult(ship_direction, [0., 0., 1.])

def write_answer():
    file = open('output.txt', 'w')
    if abs(gun_angle) > 60 or mast_angle > 60:
        file.write('0')
    else:   
        file.write('1\n' if is_left else '-1\n')
        file.write(str(gun_angle)+'\n')
        file.write(str(mast_angle*mast_angle_sign()*-1)+'\n')
        file.write('The ship swam to success')
    file.close()
    pass

def is_left():
    return math.acos(scalar_mult(const_mult(right_gun_vector, -1), dist_vector)/(math.sqrt(scalar_mult(dist_vector, dist_vector))*math.sqrt(scalar_mult(right_gun_vector, right_gun_vector))))*180./math.pi < 90

def mast_angle_sign():
    if (is_left):
        return 1 if math.acos(scalar_mult(const_mult(right_gun_vector, -1), mast_vector)/(math.sqrt(scalar_mult(mast_vector, mast_vector))*math.sqrt(scalar_mult(right_gun_vector, right_gun_vector))))*180./math.pi < 90 else -1
    else:
        return 1 if math.acos(scalar_mult(right_gun_vector, mast_vector)/(math.sqrt(scalar_mult(mast_vector, mast_vector))*math.sqrt(scalar_mult(right_gun_vector, right_gun_vector))))*180./math.pi < 90 else -1

def main():
    read_input()
    # Разность векторов корабль врага - наш корабль
    global dist_vector
    dist_vector = mat_sum(enemy, const_mult(ship, -1))
    # Угол между направлением нашего корабля и вектором от нашего до вражеского
    cos_dist_dir = scalar_mult(dist_vector, ship_direction)/(math.sqrt(scalar_mult(dist_vector, dist_vector))*math.sqrt(scalar_mult(ship_direction, ship_direction)))
    grad_dist_dir = math.acos(cos_dist_dir) * 180./math.pi
    calculate_right_gun_vector()
    # Угол, на который нужно повернуть пушку
    global gun_angle
    gun_angle = (90.-grad_dist_dir)
    # С какой стороны находится корабль врага
    global is_left
    is_left = is_left()
    # Угол, на который нужно повернуть мачту
    global mast_angle
    u = [0., 0., 1.]
    cos_mast_u = scalar_mult(mast_vector, u)/(math.sqrt(scalar_mult(mast_vector, mast_vector))*math.sqrt(scalar_mult(u, u)))
    grad_mast_u = math.acos(cos_mast_u)*180./math.pi
    mast_angle = abs(grad_mast_u)
    write_answer()
    pass

if __name__ == '__main__':
    main()