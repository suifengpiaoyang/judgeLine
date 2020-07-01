import sys
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


class Point(list):

    def __init__(self, *point):
        if len(point) == 2:
            self.point = point
            self.length = cmath.sqrt(
                self.point[0] ** 2 + self.point[1] ** 2).real
        else:
            raise Exception('Point must be tow numbers.')

    def __add__(self, other):
        return Point(self.point[0] + other.point[0], self.point[1] + other.point[1])

    def __sub__(self, other):
        return Point(self.point[0] - other.point[0], self.point[1] - other.point[1])

    def __rmul__(self, other):
        return Point(other * self.point[0], other * self.point[1])

    def __neg__(self):
        # 定义负号
        return Point(-self.point[0], -self.point[1])

    def __str__(self):
        return '{}'.format(self.point)

    def __repr__(self):
        return '{}'.format(self.point)

    def __getitem__(self, key):
        # 定义该类下标引用的数值调用方式，不允许切片
        if isinstance(key, int):
            if key in (0, 1):
                return self.point[key]
            else:
                raise IndexError('The index must in (0,1)')
        else:
            raise TypeError('The key type can not be slice.')


class Vector(list):

    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.location = self.endPoint - self.startPoint
        self.length = cmath.sqrt(
            self.location[0] ** 2 + self.location[1] ** 2).real


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


def getLineSegmentArguments(vector1, vector2):
    # w 代表起点在 vector1 ,终点在 vector2 的向量
    # w = C0 - A0 + n * ( D0 - C0 ) - t * (B0 - A0)
    # 0 =< n,t <= 1
    # p = C0 - A0 , q = D0 - C0, r = - (B0 - A0)
    # w = n * q + t * r + p
    # Lab = A0 + t * (B0 - A0)
    # Lcd = C0 + n * (D0 - C0)
    A = vector1.startPoint
    B = vector1.endPoint
    C = vector2.startPoint
    D = vector2.endPoint
    p = C - A
    q = D - C
    r = A - B

    return q, r, p


def judgeCrossPoint(linesegment1, linesegment2):
    q, r, p = getLineSegmentArguments(linesegment1, linesegment2)

    lineX = [each[0] for each in (q, r, p)]
    lineY = [each[1] for each in (q, r, p)]
    result = solveEquationsOfTwoUnknowns(lineX, lineY)
    if result is not None:
        t, n = result
        logging.debug('t : {} n: {}'.format(t, n))
        if t >= 0 and t <= 1 and n >= 0 and n <= 1:
            # 交点坐标
            crossPointLocation = linesegment1.startPoint + t * \
                (linesegment1.startPoint - linesegment1.endPoint)
            logging.info(crossPointLocation)
            logging.info('两条线段相交。')
            return 1
        else:
            logging.debug('t 和 n 必须在 [0,1] 之间两条线段才相交。')
            logging.debug('交点不在线段之上，重新计算最小距离。')
            return 2
    else:
        # 此处需计算最小距离
        logging.info('两条线平行。')
        return 3


def getPointToSegmentMinDistance(pointLocation, linesegment):

    # 以下 AB,AP J均为向量，在这里无法加特别标志，在此说明。
    P = pointLocation
    A = linesegment.startPoint
    B = linesegment.endPoint
    AB = B - A
    AP = P - A
    BP = P - B

    ACDirectionFlag = (AB[0] * AP[0] - AB[1] * AP[1]) / \
        (AB[0] ** 2 + AB[1] ** 2)

    if ACDirectionFlag <= 0:
        minDistance = AP.length
    elif ACDirectionFlag > 1:
        minDistance = BP.length
    else:
        ACLength = AB.length * ACDirectionFlag
        APLength = AP.length
        minDistance = cmath.sqrt(APLength ** 2 - ACLength ** 2).real
    return minDistance


def getTowSegmentsMinDistance(linesegment1, linesegment2):

    '''
    example:

    point1 = Point(1, 2)
    point2 = Point(3, 5)
    linesegment1 = Vector(point1, point2)

    point3 = Point(2, 4)
    point4 = Point(6, 10)
    linesegment2 = Vector(point3, point4)

    getTowSegmentsMinDistance(linesegment1, linesegment2)
    '''

    logging.debug('line segment : {} >> {}'.format(
        linesegment1.startPoint, linesegment1.endPoint))
    logging.debug('line segment : {} >> {}'.format(
        linesegment2.startPoint, linesegment2.endPoint))
    flag = judgeCrossPoint(linesegment1, linesegment2)
    if flag == 1:
        minDistance = 0
    elif flag == 2:
        fourPointDistanceList = []
        line1Point1 = getPointToSegmentMinDistance(
            linesegment1.startPoint, linesegment2)
        line1Point2 = getPointToSegmentMinDistance(
            linesegment1.endPoint, linesegment2)
        line2Point1 = getPointToSegmentMinDistance(
            linesegment2.startPoint, linesegment1)
        line2Point2 = getPointToSegmentMinDistance(
            linesegment2.endPoint, linesegment1)
        fourPointDistanceList = [line1Point1,
                                 line1Point2, line2Point1, line2Point2]
        minDistance = min(*fourPointDistanceList)
    elif flag == 3:
        minDistance = getPointToSegmentMinDistance(
            linesegment1.startPoint, linesegment2)
    logging.info('线段最小距离为 {}'.format(minDistance))


def test():

    logging.debug('Testing getTowSegmentsMinDistance...')

    testPointList = [((1, 2), (3, 5)),
                     ((2, 4), (6, 10)),
                     ((1, 5), (8, 1)),
                     ((7, 8), (11, 12))
                     ]

    linesegment1 = Vector(Point(*testPointList[0][0]),Point(*testPointList[0][1]))
    for line in testPointList[1:]:
        linesegment2 = Vector(Point(*line[0]), Point(*line[1]))
        getTowSegmentsMinDistance(linesegment1, linesegment2)
        logging.debug('----------------------------')


if __name__ == '__main__':
    test()
