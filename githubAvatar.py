import random
import numpy
import cv2

"""

+-------------------+
|                   |
|   +---+---+---+   |
|   |   |███|   |   |
|   +---+---+---+   |
|   |███|███|███|   |
|   +---+---+---+   |
|   |███|   |███|   |
|   +---+---+---+   |
|                   |
+-------------------+
 
"""


class GithubAvatarGenerator:
    GITHUB_AVATAR_ROWS = 420
    GITHUB_AVATAR_COLS = 420

    #  围边使用的灰色 ； 默认背景色
    COLOR_GREY_BGR = [230, 230, 230]
    #  外围宽度  色块到边界的距离
    GITHUB_AVATAR_FRAME_WIDTH = 35;
    #  Block宽度  前景色块大小
    GITHUB_AVATAR_BLOCK_WIDTH = 70;

    #  Vertex 大小 ； 色块矩阵大小
    # 前景区域为 5 * 5 矩阵
    GITHUB_AVATAR_VERTEX_WIDTH = 5;

    """
    获取gbr 颜色列表
    """

    def getGBR(self):
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        r = random.randint(0, 255)
        return [g, b, r]

    """
         获取一个 5x5 的随机填充对称矩阵
         5x5 随机填充对称矩阵 
    """

    def getGithubAvatarVertex(self):
        # // 新建矩阵
        # 初始化 5 * 5 二维列表
        vertex = numpy.zeros([5, 5])

        """
        ▢ ▢ ▩ ▢ ▢
        ▢ ▢ ▩ ▢ ▢
        ▢ ▢ ▩ ▢ ▢
        ▢ ▢ ▩ ▢ ▢
        ▢ ▢ ▩ ▢ ▢
         """
        # // 先随机填充中间一条
        # 5 * 5 二维列表， 中间一列 随机填充True
        for i in range(5):
            # random.choice 随机获取True False
            # 若为True 改变对应值为True
            if (random.choice([True, False])):
                vertex[i][2] = True

        """
        ▩ ▩ ▢ ▢ ▢
        ▩ ▩ ▢ ▢ ▢
        ▩ ▩ ▢ ▢ ▢
        ▩ ▩ ▢ ▢ ▢
        ▩ ▩ ▢ ▢ ▢
        """
        # // 随机填充半边
        for i in range(5):
            for j in range(2):
                if (random.choice([True, False])):
                    vertex[i][j] = True

        # // 将填充的半边对称复制到另外半边
        for i in range(5):
            for j in {3, 4}:
                vertex[i][j] = vertex[i][4 - j];

        # print(vertex)
        return vertex

    # 获取图片像素bgr信息
    def getGithubAvatarRGBData(self):
        # 通道数 bgr 三个通道
        channels = 3

        # 宽度
        img_border = self.GITHUB_AVATAR_FRAME_WIDTH
        # 色块大小
        block_size = self.GITHUB_AVATAR_BLOCK_WIDTH
        img_size = self.GITHUB_AVATAR_ROWS

        # BGR 信息
        bgrData = numpy.zeros([self.GITHUB_AVATAR_ROWS, self.GITHUB_AVATAR_ROWS, 3], numpy.uint8)
        # 获取随机的颜色索引
        randomColor = self.getGBR()
        # print(randomColor)

        # 填充四周背景色
        #  top
        for i in range(0, img_border):
            for j in range(img_size):
                for k in range(channels):
                    bgrData[i][j][k] = self.COLOR_GREY_BGR[k]

        for i in range(-img_border, 0):
            for j in range(img_size):
                for k in range(channels):
                    bgrData[i][j][k] = self.COLOR_GREY_BGR[k]

        #  left
        for i in range(img_size):
            for j in range(img_border):
                for k in range(channels):
                    bgrData[i][j][k] = self.COLOR_GREY_BGR[k]

        #  right
        for i in range(-img_border, img_size):
            for j in range(-img_size, 0):
                for k in range(channels):
                    bgrData[i][j][k] = self.COLOR_GREY_BGR[k]

        # // 将中间 5x5 的范围按照矩阵信息填充
        vertex = self.getGithubAvatarVertex()
        for i in range(5):
            for j in range(5):
                if (vertex[i][j]):
                    # 填充前景色块
                    for m in range(img_border + i * block_size, img_border + i * block_size + block_size):
                        for n in range(img_border + j * block_size, img_border + j * block_size + block_size):
                            for k in range(channels):
                                bgrData[m][n][k] = randomColor[k]
                else:
                    # 填充 背景色快
                    for m in range(img_border + i * block_size, img_border + i * block_size + block_size):
                        for n in range(img_border + j * block_size, img_border + j * block_size + block_size):
                            for k in range(channels):
                                bgrData[m][n][k] = self.COLOR_GREY_BGR[k]
        return bgrData


if __name__ == '__main__':
    githubIcon = GithubAvatarGenerator()
    for i in range(10):
        img = githubIcon.getGithubAvatarRGBData()
        cv2.imshow("123", img)
        cv2.waitKey(0)

    # for i in range(10):
    #     img = githubIcon.getGithubAvatarRGBData()
    #     filePath = "./random%s.png" % i
    #     print(filePath)
    #     cv2.imwrite(filePath, img)
