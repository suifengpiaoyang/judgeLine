import sympy


class LineSegment:

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.minX = min(point1[0], point2[0])
        self.maxX = max(point1[0], point2[0])
        self.minY = min(point1[1], point2[1])
        self.maxY = max(point1[1], point2[1])
        self.line = self.transformPoint2Line(point1, point2)

    def transformPoint2Line(self, point1, point2):
        # line: Ax + By + C = 0
        # return A, B, C
        X1, Y1 = point1
        X2, Y2 = point2
        A = Y2 - Y1
        B = X1 - X2
        C = X2 * Y1 - X1 * Y2
        return A, B, C


def solveEquationsOfTwoUnknowns(line1, line2):
    A1, B1, C1 = line1
    A2, B2, C2 = line2
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    result = sympy.solve([A1 * x + B1 * y + C1, A2 * x + B2 * y + C2], [x, y])
    intersection = (result[x], result[y])
    return intersection


def judge2LineSegments(LineSegment1, LineSegment2):
    # 判断交点是否在线段上，还是在线段的延长线上
    # 如果没有交点，线段在平面上的情况有两种
    # 假设第一条线段水平布置
    # 第一种就是第二条线段在第一条线段 Y 轴上的射影没有重叠
    # 此时的最小距离是两条线段边缘两点之间的距离
    # 第二种就是由重叠，此时的线段距离最小值是第二条线段的
    # 最小 Y 值引一条垂直于第一条线段的线，该线与第一线段
    # 产生一个交点，这个点和第二线段最小 Y 值之间的距离就是
    # 线段距离最小值
    intersection = solveEquationsOfTwoUnknowns(
        LineSegment1.line, LineSegment2.line)
    if (intersection[0] >= LineSegment1.minX and intersection[0] <= LineSegment1.maxX) and \
            (intersection[0] >= LineSegment2.minX and intersection[0] <= LineSegment2.maxX):
        minLength = 0
        return intersection, minLength
    else:
        pass


def run():

    point1 = (1, 2)
    point2 = (3, 5)
    linesegment1 = LineSegment(point1, point2)
    point3 = (7, 8)
    point4 = (11, 12)
    linesegment2 = LineSegment(point3, point4)
    print(linesegment1.line)
    print(linesegment2.line)
    print(solveEquationsOfTwoUnknowns(linesegment1.line, linesegment2.line))

if __name__ == '__main__':
    run()
