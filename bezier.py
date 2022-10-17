import numpy as np
import matplotlib.pyplot as plt
import math
import imageio
import sympy
from sympy import diff, sin, exp, Symbol

x = Symbol('x')
y = Symbol('y')
t = Symbol('t')
a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')
e = Symbol('e')
f = Symbol('f')
g = Symbol('g')
Symbols = [a, b, c, d, e, f, g]
P = np.array([[70, 125],
              [85, 140],
              [70, 150],
              [80, 225]])


def combination(n, r):
    return math.factorial(n)/(math.factorial(r)*math.factorial(n-r))


def bernstein(n, i):
    return lambda t: combination(n, i)*(t**i)*(1-t)**(n-i)


def bezier(n, t, Points):
    total = 0
    for i in range(n+1):
        total += bernstein(n, i)(t) * Points[i]
    return total


def line_percent(points, percent):
    return points[0] + (points[1]-points[0])*percent


def draw_line_percent(percent, Points):
    n = len(Points)
    all_points = [Points]
    for i in range(n-2):
        temp_points = []
        for pair in [all_points[i][a:a+2] for a in range(len(all_points[i])-1)]:
            temp_points.append(line_percent(pair, percent))
        all_points.append(temp_points)

    return all_points


def generate_points(Points, time_step):
    return np.array([bezier(len(Points) - 1, t / float(time_step), Points) for t in range(time_step)])


def combination_interpolate(n, r):
    return sympy.factorial(n)/(sympy.factorial(r)*sympy.factorial(n-r))


def bernstein_interpolate(n, i):
    return combination_interpolate(n, i)*(t**i)*(1-t)**(n-i)


def bezier_interpolate(pair, n):
    eqn = 0
    for i in range(n + 1):
        eqn += bernstein_interpolate(n, i) * Symbols[-1 if i == n else i]
    return eqn


def interpolate(n):
    # .subs([(a, P[0]), (g, P[-1])])
    # global a
    # global g
    eqn = bezier_interpolate(1, n)
    eqn_d = diff(eqn, t)
    eqn_d2 = diff(eqn_d, t)
    print(eqn)
    print(eqn_d)
    print(eqn_d2)
    for pair in [P[a:a + 2] for a in range(len(P) - 1)]:
        pass


def main():

    show_plot = 1
    curve_only = 0
    if show_plot:
        x_space = np.linspace(0, 1, 5000)
        points = np.array([bezier(len(P) - 1, x, P) for x in x_space])
        plt.plot(points[:, 0], points[:, 1], color='b', linewidth='3')
        if not curve_only:
            plt.plot(P[:, 0], P[:, 1], marker='o', markersize='4')
        plt.show()

    animate = 1
    if animate:
        filenames = []
        for i, percentage in enumerate(np.linspace(0, 1, 100)):
            points = np.array([bezier(len(P)-1, x / 1000.0, P) for x in range(1000)])
            # plot the curve itself
            plt.plot(points[:, 0], points[:, 1], color='b', linewidth='3')
            # plot the control plots
            plt.plot(P[:, 0], P[:, 1], marker='o', markersize='4')
            # plot the 'drawing' point
            plt.plot(*bezier(len(P)-1, percentage, P), marker='o', markersize='5', color='r')

            all_p = draw_line_percent(percentage, P)
            for j, set_p in enumerate(all_p):
                a = .7*(j/(len(all_p))) + .2
                x, y = zip(*set_p)
                plt.plot(x, y, marker='o', markersize='3', alpha=a)
            filenames.append("plots/{0}.png".format(i+1))
            plt.savefig("plots/{0}.png".format(i+1))
            plt.clf()

        with imageio.get_writer('animated_bezier.gif', mode='I', fps=10) as writer:
            for filename in filenames: 
                image = imageio.imread(filename)
                writer.append_data(image)


if __name__ == '__main__':
    main()
