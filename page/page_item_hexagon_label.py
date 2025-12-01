import math
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QBrush, QBitmap
from PyQt5.QtWidgets import  QLabel

class HexagonLabel(QLabel):
    def __init__(self, parent=None, border_color=Qt.blue, border_width=3):
        '''
        六边形边框标签
        :param parent:
        :param border_color:
        :param border_width:
        '''
        super().__init__(parent)
        self.border_color = border_color  # 边框颜色
        self.border_width = border_width  # 边框宽度
        self.setMinimumSize(20, 20)  # 最小尺寸确保可见性
        self._update_mask()  # 初始化遮罩

    def set_border_style(self, color, width):
        """设置边框样式"""
        self.border_color = color
        self.border_width = width
        self.update()  # 触发重绘

    def paintEvent(self, event):
        # 调用父类方法绘制文本/图片
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿处理

        # 计算六边形路径
        hex_path = self._calculate_hexagon_path()

        # 设置剪辑区域，仅保留六边形内部
        painter.setClipPath(hex_path)
        # 绘制背景（可选）
        #painter.fillPath(hex_path, QBrush(Qt.white))
        # 绘制边框（使用设置的参数）
        painter.setPen(QPen(self.border_color, self.border_width))
        painter.drawPath(hex_path)

    def resizeEvent(self, event):
        self._update_mask()  # 窗口大小变化时更新遮罩
        super().resizeEvent(event)

    def _calculate_hexagon_path(self):
        """计算六边形的顶点坐标"""
        path = QPainterPath()
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2-2   # 边距避免溢出

        # 计算6个顶点坐标
        for i in range(6):
            angle = 60 * i + 30  # 30°偏移使顶点朝上
            radian = math.radians(angle)
            x = center.x() + radius * math.cos(radian)
            y = center.y() + radius * math.sin(radian)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.closeSubpath()
        return path

    def _update_mask(self):
        """更新遮罩以隐藏六边形外的像素"""
        mask = QBitmap(self.size())
        mask.fill(Qt.color0)  # 初始化为全透明
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        # 绘制白色区域（保留部分）
        painter.fillPath(self._calculate_hexagon_path(), QBrush(Qt.color1))
        painter.end()
        self.setMask(mask)  # 应用遮罩