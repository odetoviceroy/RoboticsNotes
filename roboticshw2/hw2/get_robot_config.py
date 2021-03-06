# George Juarez - ICEN464 - Robotics
import math as m
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys

class Coordinate:
    def __init__(self,x,y):
        self.x = x
        self.y = y

# get_arm_config: this function takes in the lengths of the robot arms, and the coordinate of the end effector
# Output: returns the angle at which the robot arms are positioned by [theta1, theta2]
def get_arm_config(length1, length2, coord):
    cos_theta2 = m.sqrt(m.pow(coord.x, 2) + m.pow(coord.y, 2)) - (m.pow(length1, 2)) \
                 + (m.pow(length2, 2))
    theta2 = m.pi - m.acos(cos_theta2 / (-2 * length1 * length2))
    angle_b = m.atan((length2 * m.sin(theta2)) / (length1 + length2 * m.cos(theta2)))
    theta1 = m.atan(coord.y / coord.x) - angle_b
    print "Theta 1: ", theta1, "\nTheta 2: ", theta2
    return [theta1, theta2] 

# generate_robot_plotpts: this function takes in two angles and two lengths, for the angles and lengths of robot arms
# Output: returns two tuples: first tuple specifies the x coordinates of the arm joints (Ex: [0,3,5])
# Next tuple specifies y coordinates of the arm joints (Ex: [0,1,2])...so end effector is at point (5,2)
def generate_robot_plotpts(theta1, theta2, length1, length2):
    x2 = length1 * m.cos(theta1) + length2 * m.cos(theta1 + theta2) 
    y2 = length1 * m.sin(theta1) + length2 * m.sin(theta1 + theta2)
    return [[0,length1 * m.cos(theta1),x2],[0,length1 * m.sin(theta1),y2]]

# robot_draw_arm: function returns a plot to view of the current robot configuration, takes in two tuples
# that are generated with generate_robot_plotpts
def robot_draw_arm(x,y):
    print x, "\n", y
    plt.plot(x,y, 'ro-')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

# robot_draw_circle: function that takes in a radius and a center point, generates two tuples (one for x coordinates)
# (and the other for y coordinates)...these tuples have 50 values each
def robot_draw_circle(radius, center):
    time = [x*0.2 for x in range(0, 51)]
    theta = []
    x_vals = []
    y_vals = []
    for t in time:
        theta.append(t * (2 * m.pi)/10)
    for i in range(0, len(theta)):
        x_vals.append(center.x + radius * m.cos(theta[i]))
        y_vals.append(center.y + radius * m.sin(theta[i]))

    return [x_vals, y_vals]

fig = plt.figure()
ax = plt.axes(xlim = (-8,8), ylim = (-8,8))
N = 3
points = ax.plot(*([[], []]*N), color = 'green', linestyle ='--', marker = 'o')

def init():
    for line in points:
        line.set_data([],[])
    return points

def animate(i, second_joint_config, end_effector_config):
    points[0].set_data([0],[0])
    points[1].set_data([[second_joint_config[i][0]],[second_joint_config[i][1]]])
    points[2].set_data([[end_effector_config[i][0]],[end_effector_config[i][1]]])
    print "SECOND POINT POSITION: (", second_joint_config[i][0], ",", second_joint_config[i][1], ")"
    print "END EFFECTOR POSITION: (", second_joint_config[i][0], ",", second_joint_config[i][1], ")"
    return points

# robot_trace_circle: function that takes in two lengths for the robot arm, and x_vals and y_vals generated from robot_draw_circle
# Output is the final animation for problem 2
def robot_trace_circle(length1, length2, x_vals, y_vals):
    arm_config = [] # master list of configurations of all arm positions
    # setup:  [ [[0,x11,x12], [0,y11,y12]] , [[0,x12,x22], [0,y12,y22]], ...]
    first_joint_config =[] # master list of configurations of the first joint, all contain zeroes
    second_joint_config = [] # second joint
    end_effector_config = [] # end effector
    for i in range(0, len(x_vals) - 1):
        [theta1, theta2] = get_arm_config(length1, length2, Coordinate(x_vals[i], y_vals[i]))
        [x,y] = generate_robot_plotpts(theta1, theta2, length1, length2)
        arm_config.append([x,y])
    for setup in arm_config:
        first_joint_config.append([setup[0][0], setup[1][0]])
        second_joint_config.append([setup[0][1], setup[1][1]])
    for i in range(0, len(x_vals)):
        end_effector_config.append([x_vals[i], y_vals[i]])        
    print first_joint_config, "\n", len(first_joint_config)
    print second_joint_config, "\n", len(first_joint_config)
    print end_effector_config, "\n", len(first_joint_config)
    
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=50, fargs=(
        second_joint_config,
        end_effector_config,
        ), interval=100, blit=True)

    fig.suptitle('ROBOT DRAW CIRCLE', fontsize=20)
    plt.show()

if __name__ == "__main__": # main function
    length1 = 3
    length2 = 6
    if sys.argv[1] == "p1": # Triggered by: python get_robot_config.py p1
        coord = Coordinate(2,4)
        [theta1, theta2] = get_arm_config(length1, length2, coord)
        [x,y] = generate_robot_plotpts(theta1, theta2, length1, length2)
        robot_draw_arm(x,y)
    if sys.argv[1] == "p2": # Triggered by: python get_robot_config.py p1
        center = Coordinate(3,4)
        radius = 2
        [x_vals, y_vals] = robot_draw_circle(radius, center)
        robot_trace_circle(length1, length2, x_vals, y_vals)
