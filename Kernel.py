from PyQt5.QtWidgets import QFileDialog
from ERROR import INVALID_OPERAND
class Kernel:
    def __init__(self, mode=0) -> None:
        self.mode = mode
        self.get_ready()
        self.file = None
        self.file_cal_result = []
        
    def get_ready(self):
        self.memory = 0
        self.draft = 0
        self.result = 0
        self.current_input = ''
        self.current_op = ''
        self.display = ''

        self.numer = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
        self.operation = ['+', '-', '*', '/', '**', '%', '~', '=']

    def set_mode(self, mode):
        self.mode = mode
        if self.mode == 0:
            self.get_ready()
        else:
            self.cal_on_file()


    def get_number(self, char):
        if char in self.numer:
            self.current_input += char
            return self.current_input

    def get_operation(self, op):
        if op in self.operation:
            if self.current_input:
                if op == '~':
                    if self.current_input[0] == '-':
                        self.current_input = self.current_input[1 : ]
                    else:
                        self.current_input = '-' + self.current_input

                else:
                    number = eval(self.current_input)
                    self.current_input = ''
                    if isinstance(number, float) or isinstance(number, int):
                        if self.current_op == '':
                            self.current_op = op
                            self.draft = number
                        else:
                            self.draft = eval(str(self.draft) + self.current_op + str(number))
                        if op != '=':
                            self.current_op = op
                        else:
                            self.result = self.draft
                            self.current_op = ''
                    else:
                        raise INVALID_OPERAND

            else:
                if op == '=':
                    self.result = self.draft
                    self.current_op = ''
                elif op != '~':
                    self.current_op = op

    def get_m(self, m):
        if m == 'ms':
            if self.display:
                self.memory = eval(self.display)
            self.current_input = ''
        elif m == 'mc':
            self.memory = 0
        elif m == 'mr':
            self.current_input = str(self.memory)
        elif m == 'm+':
            if self.display:
                self.memory += eval(self.display)
            self.current_input = ''
        else:
            if self.display:
                self.memory -= eval(self.display)
            self.current_input = ''

    def ac(self):
        self.memory = 0
        self.draft = 0
        self.result = 0
        self.current_input = ''
        self.current_op = ''
        self.file = None
        self.file_cal_result = []
        self

    def file_mode(self, file_name):
        self.open_file(file_name)
        self.file_operation()

    def open_file(self, file_name):
        if file_name:
            self.file = open(file_name, 'r')

    def file_operation(self):
        task = self.file.readlines()
        task = [item.rstrip('\n') for item in task]
        self.file_cal_result = []
        for t in task:
            try:
                result = eval(t)
                self.file_cal_result.append(result)
            except:
                self.file_cal_result.append("Error")

    def file_saver(self, save_path):
        file_result = open(save_path, mode = 'w')
        for result in self.file_cal_result:
            file_result.write(str(result) + '\n')