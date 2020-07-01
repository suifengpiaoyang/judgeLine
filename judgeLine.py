import cmath
import sympy
import logging
"""
参考网址：
[Distance between 3D Lines & Segments](http://geomalgorithms.com/a07-_distance.html)
[[计算几何] (平面上)点到线段的最短距离 矢量法](https://blog.csdn.net/Mr_HCW/article/details/82816490)
[[计算几何] (平面上)两线段最短距离 矢量法](https://blog.csdn.net/Mr_HCW/article/details/82832046)

《Distance between 3D Lines & Segments》 使用的坐标设置方式个人觉得很理想，虽然不同于解析几何的
坐标系
《[计算几何] (平面上)两线段最短距离 矢量法》 里面判断两线相交的方式我不喜欢，因为很麻烦，即使作者这么做
是没有问题的。使用上述的坐标系计算两线相交并不困难。
判断点到线段的最短距离，《[计算几何] (平面上)点到线段的最短距离 矢量法》 该文的做法很好，至少在目前我所能想到
的方式之中，应该是相当好很方便的一种了。不过我一直觉得，通过上述那种坐标系，应该有更统一的一种解决办法，只是
我一直没有想出来。《Distance between 3D Lines & Segments》 文中讨论的是 3D 平面下的，我觉得某种情况下不适合
2D 平面，就文中提出的“线段之间的最短距离垂直于两线”这种在 3D 平面下很简单的关系 2D 平面并没有。
"""

logging.basicConfig(format='[%(asctime)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)


class LineSegment:

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2


def solveEquationsOfTwoUnknowns(line1, line2):
    # 解二元一次方程，将一般式 Ax + By +C = 0 的系数 A, B, C 传入，
    # sympy.solve() 就能自动解出结果。之所以使用别人的模块，主要是
    # 简单，懒，自己实现也是做得出来的。
    A1, B1, C1 = line1
    A2, B2, C2 = line2
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    result = sympy.solve([A1 * x + B1 * y + C1, A2 * x + B2 * y + C2], [x, y])
    if len(result) == 0:
        # 平行，方程无解
        return None
    else:
        # 返回解出来的结果值
        intersection = (result[x], result[y])
        return intersection


def getTargetLineSegmentArgus(LineSegment1, LineSegment2):
    # w = C0 - A0 + n * ( D0 - C0 ) - t * (B0 - A0)
    # 0 =< n,t <= 1
    # p = C0 - A0 , q = D0 - C0, r = A0 - B0
    # w = n * q - t * r + p
    # Lab = A0 + t * (B0 - A0)
    # Lcd = C0 + n * (D0 - C0)
    px = LineSegment2.point1[0] - LineSegment1.point1[0]
    py = LineSegment2.point1[1] - LineSegment1.point1[1]
    qx = LineSegment2.point2[0] - LineSegment2.point1[0]
    qy = LineSegment2.point2[1] - LineSegment2.point1[1]
    rx = -(LineSegment1.point2[0] - LineSegment1.point1[0])
    ry = -(LineSegment1.point2[1] - LineSegment1.point1[1])

    return ((qx, rx, px), (qy, ry, py))


def judgeCrossPoint(linesegment1, linesegment2):
    groupX, groupY = getTargetLineSegmentArgus(linesegment1, linesegment2)
    logging.debug('{} {}'.format(groupX, groupY))
    result = solveEquationsOfTwoUnknowns(groupX, groupY)
    if result is not None:
        t, n = result
        logging.debug('{} {}'.format(t, n))
        if t >= 0 and t <= 1 and n >= 0 and n <= 1:
            # 交点坐标
            # crossPointLocation = (linesegment1.point1[0] + t * (linesegment1.point2[0] - linesegment1.point1[0]),
            #                       linesegment1.point1[1] + t * (linesegment1.point2[1] - linesegment1.point1[1]))
            # logging.info('两线段有交点交点坐标为：')
            # logging.info(crossPointLocation)
            # logging.info('所以两线段的距离最小值为零。')
            logging.info('两条线段相交。')
            return 1
        else:
            logging.info('交点不在线段之上，重新计算最小距离。')
            return 2
    else:
        # 此处需计算最小距离
        logging.info('两条线平行。')
        return 3


def getDistance(segmentLocation):

    x = segmentLocation[0]
    y = segmentLocation[1]
    distance = cmath.sqrt(x ** 2 + y ** 2).real
    return distance


def getPointToSegmentMinDistance(pointLocation, linesegment):

    # 以下 AB,AP J均为向量，在这里无法加特别标志，在此说明。
    P = pointLocation
    A = linesegment.point1
    B = linesegment.point2
    AB = (B[0] - A[0], B[1] - A[1])
    AP = (P[0] - A[0], P[1] - A[1])
    BP = (P[0] - B[0], P[1] - B[1])

    ACDirectionFlag = (AB[0] * AP[0] - AB[1] * AP[1]) / \
        (AB[0] ** 2 + AB[1] ** 2)

    if ACDirectionFlag <= 0:
        minDistance = getDistance(AP)
    elif ACDirectionFlag > 1:
        minDistance = getDistance(BP)
    else:
        ACLength = getDistance(AB) * ACDirectionFlag
        APLength = getDistance(AP)
        minDistance = cmath.sqrt(APLength ** 2 - ACLength ** 2).real
    return minDistance


def getTowSegmentsMinDistance(linesegment1, linesegment2):
    logging.info()
    flag = judgeCrossPoint(linesegment1, linesegment2)
    if flag == 1:
        minDistance = 0
    elif flag == 2:
        fourPointDistanceList = []
        line1Point1 = getPointToSegmentMinDistance(
            linesegment1.point1, linesegment2)
        line1Point2 = getPointToSegmentMinDistance(
            linesegment1.point2, linesegment2)
        line2Point1 = getPointToSegmentMinDistance(
            linesegment2.point1, linesegment1)
        line2Point2 = getPointToSegmentMinDistance(
            linesegment2.point2, linesegment1)
        fourPointDistanceList = [line1Point1,
                                 line1Point2, line2Point1, line2Point2]
        minDistance = min(*fourPointDistanceList)
    elif flag == 3:
        minDistance = getPointToSegmentMinDistance(
            linesegment1.point1, linesegment2)
    logging.info('线段最小距离为 {}'.format(minDistance))

def test():

    point1 = (1, 2)
    point2 = (3, 5)
    linesegment1 = LineSegment(point1, point2)
    # point3 = (2, 4)
    # point4 = (6, 10)
    # point3 = (1, 5)
    # point4 = (8, 1)
    point3 = (7, 8)
    point4 = (11, 12)
    linesegment2 = LineSegment(point3, point4)
    getTowSegmentsMinDistance(linesegment1, linesegment2)


if __name__ == '__main__':
    test()
