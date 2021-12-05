from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from math import *
# from MainWin import MainWin
import sys
  
class clockForm(QWidget):
    def __init__(self):
        super(clockForm, self).__init__()
        # self.setWindowTitle("Clock")
        self.timer=QTimer()
        #设置窗口计时器
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)
          
    def paintEvent(self,event):
        #时钟指针坐标点
        hourPoint = [QPoint(7,8), QPoint(-7,8), QPoint(0, -30)]
        minPoint = [QPoint(7,8), QPoint(-7,8), QPoint(0, -65)]
        secPoint = [QPoint(7,8), QPoint(-7,8), QPoint(0, -80)]
        #时钟指针颜色
        hourColor = QColor(200, 100, 0, 200)
        minColor = QColor(0, 127, 127, 150)
        secColor = QColor(0, 160, 230, 150)

        # side = min(self.width(), self.height())
        side = 400

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # painter.translate(self.width()/2, self.height()/2)  #painter坐标系原点移至widget中央
        painter.translate(0, 0)
        painter.scale(side / 200, side / 200)               #缩放painterwidget坐标系，使绘制的时钟位于widge中央,即钟表支持缩放

        #绘制小时和分钟刻度线
        painter.save()
        for i in range(0, 60):
            if (i % 5) != 0:
                painter.setPen(minColor)
                painter.drawLine(92, 0, 96, 0)#绘制分钟刻度线
            else:
                painter.setPen(hourColor)
                painter.drawLine(88, 0, 96, 0)#绘制小时刻度线
            painter.rotate(360/60)
        painter.restore()

        #绘制小时数字
        painter.save()
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        pointSize = font.pointSize()
        painter.setPen(hourColor)
        nhour = 0
        radius = 100
        for i in range(0, 12):
            nhour = i + 3   #按QT-Qpainter的坐标系换算，3小时的刻度线对应坐标轴0度
            if nhour > 12:
                nhour = nhour - 12

            x = radius*0.8*cos(i*30*pi/180.0) - pointSize
            y = radius*0.8*sin(i*30*pi/180.0) - pointSize/2.0
            width = pointSize*2
            height = pointSize
            painter.drawText(QRectF(x,y,width,height), Qt.AlignCenter, str(nhour))
        painter.restore()

        time = QTime.currentTime()

        #绘制小时指针
        painter.save()
        painter.setPen(Qt.NoPen)        #无轮廓线
        painter.setBrush(hourColor)     #填充色
        painter.rotate(30*(time.hour() + time.minute() / 60))#每圈360° = 12h 即：旋转角度 = 小时数 * 30°
        print(time.hour())
        painter.drawConvexPolygon(QPolygonF(hourPoint))
        painter.restore()

        #绘制分钟指针
        painter.save()
        painter.setPen(Qt.NoPen)        #无轮廓线
        painter.setBrush(minColor)      #填充色
        painter.rotate(6*(time.minute() + time.second() / 60))#每圈360° = 60m 即：旋转角度 = 分钟数 * 6°
        painter.drawConvexPolygon(QPolygonF(minPoint))
        painter.restore()

        #绘制秒钟指针
        painter.save()
        painter.setPen(Qt.NoPen)        #无轮廓线
        painter.setBrush(secColor)      #填充色
        painter.rotate(6*time.second())
        painter.drawConvexPolygon(QPolygonF(secPoint))      #每圈360° = 60s 即：旋转角度 = 秒数 * 6°
        painter.restore()

