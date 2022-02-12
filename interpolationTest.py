from utils.linearInterpolator import LinearInterpolator

points = [[1, 2], [2, 3], [4, 7]]

interpolator = LinearInterpolator(points)

print(interpolator.interpolate(3))
