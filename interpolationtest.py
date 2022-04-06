import matplotlib.pyplot as plt

from utils.linearinterpolator import LinearInterpolator

points = [[1, 2], [2, 3], [4, 7], [5, 8], [6, 9], [10, 11], [12, 13]]

points_x = [i[0] for i in points]
points_y = [i[1] for i in points]
interpolated_points = []

plt.plot(points_x, points_y, "ro")

x = []
interpolator = LinearInterpolator(points)

for i in range(15):
    if i not in points_x:
        x.append(i)
        interpolated_points.append(interpolator.interpolate(i))

print(interpolated_points)
plt.plot(x, interpolated_points, "bo")
plt.show()
