from Ui_main import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from math import *
from Kernel import Kernel
# from Clock import clockForm
import sys

class MainWin(Ui_MainWindow, QMainWindow):
    def __init__(self) -> None:
        super(MainWin, self).__init__()
        self.setupUi(self)
        self.setFixedSize(600, 800)
        self.setWindowTitle("超级计算器")
        self.timer=QTimer()
        #设置窗口计时器
        self.mode = 0
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)
        self.kernel = Kernel()
        self.number_key = [self.btn0, self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6, self.btn7, self.btn8, self.btn9, 
            self.btn_ms, self.btn_mc, self.btn_mr, self.btn_mm, self.btn_mp,
            self.btn_dot, self.btn_reverse, self.btn_plus, self.btn_minus, self.btn_mul, self.btn_div, self.btn_mod, self.btn_pow, self.btn_eq,
            self.btn_l, self.btn_r]
        self.file_key = [self.btn_load, self.btn_save]
        # self.clock_widget = clockForm()
        # self.clock_widget.show()
        # self.clock_widget.move(self.width() - 100, self.height() - 100)
        self.display = "0"
        self.head = False
        self.pos = 0
        self.file_mode = False
        # self.lcd_display.display("12.38")
        self.btn_mc.setEnabled(False)
        self.btn_mr.setEnabled(False)    
        self.btn0.clicked.connect(self.btn0_clicked)
        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)
        self.btn3.clicked.connect(self.btn3_clicked)
        self.btn4.clicked.connect(self.btn4_clicked)
        self.btn5.clicked.connect(self.btn5_clicked)
        self.btn6.clicked.connect(self.btn6_clicked)
        self.btn7.clicked.connect(self.btn7_clicked)
        self.btn8.clicked.connect(self.btn8_clicked)
        self.btn9.clicked.connect(self.btn9_clicked)
        self.btn_dot.clicked.connect(self.btn_dot_clicked)
        self.btn_plus.clicked.connect(self.btn_plus_clicked)
        self.btn_minus.clicked.connect(self.btn_min_clicked)
        self.btn_mul.clicked.connect(self.btn_mul_clicked)
        self.btn_div.clicked.connect(self.btn_div_clicked)
        self.btn_mod.clicked.connect(self.btn_mod_clicked)
        self.btn_pow.clicked.connect(self.btn_pow_clicked)
        self.btn_eq.clicked.connect(self.btn_eq_clicked)
        self.btn_reverse.clicked.connect(self.btn_reverse_clicked)
        self.btn_mc.clicked.connect(self.btn_mc_clicked)
        self.btn_mr.clicked.connect(self.btn_mr_clicked)
        self.btn_mp.clicked.connect(self.btn_mp_clicked)
        self.btn_mm.clicked.connect(self.btn_mm_clicked)
        self.btn_ms.clicked.connect(self.btn_ms_clicked)
        self.btn_ac.clicked.connect(self.btn_ac_clicked)
        self.btn_l.clicked.connect(self.btn_l_clicked)
        self.btn_r.clicked.connect(self.btn_r_clicked)
        self.btn_exit.clicked.connect(self.close)
        self.btn_load.clicked.connect(self.btn_load_clicked)
        self.btn_save.clicked.connect(self.btn_save_clicked)

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
        # side = 400

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # painter.translate(self.width()/2, self.height()/2)  #painter坐标系原点移至widget中央
        painter.translate(465, 650) #位置
        painter.scale(1.1, 1.1)    #大小           #缩放painterwidget坐标系，使绘制的时钟位于widge中央,即钟表支持缩放

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
        # print(time.hour())
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

    def closeEvent(self, event):
        if self.mode == 1:
            choice = QMessageBox.warning(self, "警告", "你的文件运算结果还没保存噢~\n点击Yes保存文件，No或关闭对话框则不保存退出", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.No:
                event.accept()
           
            if choice == QMessageBox.Yes:
                save_path = self.btn_save_clicked()
                if not save_path:
                    event.ignore()

        else:
            event.accept()
        
    def set_mode(self, mode):
        self.mode = mode
        if mode == 1:
            # print("file mode")
            for key in self.number_key:
                key.setEnabled(False)
        if mode == 0:
            for key in self.number_key:
                key.setEnabled(True)

    def btn0_clicked(self):
        self.display = self.kernel.get_number('0')
        self.lcd_display.display(self.display)
        self.kernel.display = self.display

    def btn1_clicked(self):
        self.display = self.kernel.get_number('1')
        self.lcd_display.display(self.display)
        self.kernel.display = self.display

    def btn2_clicked(self):
        self.display = self.kernel.get_number('2')
        self.lcd_display.display(self.display)
        self.kernel.display = self.display

    def btn3_clicked(self):
        self.display = self.kernel.get_number('3')
        self.lcd_display.display(self.display)
        self.kernel.display = self.display

    def btn4_clicked(self):
        self.display = self.kernel.get_number('4')
        self.lcd_display.display(self.display)
        self.kernel.display = self.display

    def btn5_clicked(self):
        self.display = self.kernel.get_number('5')
        self.lcd_display.display(self.display)
        self.kernel.display = self.display

    def btn6_clicked(self):
        self.display = self.kernel.get_number('6')
        self.lcd_display.display(self.display)
        self.kernel.display = self.display

    def btn7_clicked(self):
        self.display = self.kernel.get_number('7')
        self.lcd_display.display(self.display)
        self.kernel.display = self.display

    def btn8_clicked(self):
        self.display = self.kernel.get_number('8')
        self.lcd_display.display(self.display)
        self.kernel.display = self.display   

    def btn9_clicked(self):
        self.display = self.kernel.get_number('9')
        self.lcd_display.display(self.display)
        self.kernel.display = self.display

    def btn_dot_clicked(self):
        self.display = self.kernel.get_number('.')
        self.lcd_display.display(self.display)
        self.kernel.display = self.display       

    def btn_plus_clicked(self):
        try:
            self.kernel.get_operation('+')
            self.kernel.display = self.display
        except:
            self.lcd_display.display("Error")

    def btn_min_clicked(self):
        try:
            self.kernel.get_operation('-')
            self.kernel.display = self.display
        except:
            self.lcd_display.display("Error")

    def btn_mul_clicked(self):
        try:
            self.kernel.get_operation('*')
            self.kernel.display = self.display
        except:
            self.lcd_display.display("Error")

    def btn_div_clicked(self):
        try:
            self.kernel.get_operation('/')
            self.kernel.display = self.display
        except:
            self.lcd_display.display("Error")

    def btn_mod_clicked(self):
        try:
            self.kernel.get_operation('%')
            self.kernel.display = self.display
        except:
            self.lcd_display.display("Error")

    def btn_pow_clicked(self):
        try:
            self.kernel.get_operation('**')
            self.kernel.display = self.display
        except:
            self.lcd_display.display("Error")

    def btn_eq_clicked(self):
        try:
            self.kernel.get_operation('=')
            self.display = str(self.kernel.result)
            self.lcd_display.display(self.display)
            self.kernel.display = self.display
        except:
            self.lcd_display.display("Error")

    def btn_reverse_clicked(self):
        try:
            self.kernel.get_operation('~')
            if self.kernel.current_input:
                self.lcd_display.display(str(self.kernel.current_input))
            self.kernel.display = self.display

        except:
            self.lcd_display.display("Error")

    def btn_mc_clicked(self):
        self.kernel.get_m('mc')
        self.btn_mc.setEnabled(False)
        self.btn_mr.setEnabled(False)   

    def btn_mr_clicked(self):
        self.kernel.get_m('mr')
        self.display = self.kernel.current_input
        self.lcd_display.display(self.display)

    def btn_mp_clicked(self):
        self.kernel.get_m('m+')
        self.btn_mc.setEnabled(True)
        self.btn_mr.setEnabled(True)   
    
    def btn_mm_clicked(self):
        self.kernel.get_m('m-')
        self.btn_mc.setEnabled(True)
        self.btn_mr.setEnabled(True)   

    def btn_ms_clicked(self):
        self.kernel.get_m('ms')
        self.btn_mc.setEnabled(True)
        self.btn_mr.setEnabled(True)   

    def btn_ac_clicked(self):
        self.kernel.ac()
        self.display = '0'
        self.lcd_display.display(self.display)
        self.btn_mc.setEnabled(False)
        self.btn_mr.setEnabled(False)
        if self.mode == 1:
            self.set_mode(0)

    def btn_l_clicked(self):
        if len(self.display) > 12:
            self.lcd_display.display(self.display[0:12])
            self.head = True
            self.pos = 0

    def btn_r_clicked(self):
        if len(self.display) - self.pos >= 12:
            self.pos += 1
            self.lcd_display.display(self.display[self.pos:self.pos+12])

    def btn_load_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "浏览计算文件", './', '*.txt')
        # print(file_name)
        if file_name:
            try:
                self.set_mode(1)
                self.lcd_display.display("F")
                self.kernel.file_mode(file_name)
            except:
                self.lcd_display.display("Error")
       
    def btn_save_clicked(self):
        if self.mode == 1:
            save_path, _ = QFileDialog.getSaveFileName(self, "浏览结果保存位置", './', '*.txt')
            if save_path:
                self.kernel.file_saver(save_path)
                self.set_mode(0)
                self.lcd_display.display("0")
                return save_path