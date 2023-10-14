class BigInt:
    def __init__(self, num, base=16):   #за замовчуванням приймаємо, що число подане у 16тковій сч
        if base == 16:
            self.num = num
        #якщо це не так, то переводимо його у гекс
        elif base == 10:
            self.num = hex(num)[2:]
        else:
            self.num = hex(int(num, base))[2:]
        self.base = 16
        self.numblock = []
        #розділяємо числа на блоки так, щоб у кодному блоці було по 16 гекс символів, таким чином кожен елемент масиву важить 64 біти
        for i in range(0, len(str(self.num)), 16):
            self.numblock.append(str(self.num)[i:(i + 16)])
    '''введемо функції ініціалізації для трьох необхідних типів даних: 16 сч, 10 сч і двійкова, 
    в останніх двох додатково будемо переводити числа у ці сч з урахуванням того, що кожен блок
    має важити не більше 64 біт'''
    def setHex(self):
        for i in range(0, len(self.numblock)):
            self.numblock[i] = hex(int(self.numblock[i], self.base))[2:]
        self.base = 16

    def setDecim(self):
        numd = ''
        for i in range(0, len(self.numblock)):
            numd = numd + self.numblock[i]
        tempblock = []
        numd = str(int(numd, self.base))
        while len(numd) % 16 != 0:
            numd = '0' + numd
        for i in range(0, len(numd), 16):
            tempblock.append(numd[i:i+16])
        self.numblock = tempblock
        self.base = 10

    def setBin(self):
        self.num = bin(int(self.num, self.base))[2:]
        while len(self.num) % 64 != 0:
            self.num = '0' + self.num
        for i in range(0, len(self.numblock)):
            self.numblock[i] = self.num[i * 64: i * 64 + 64]
        self.base = 2
    #через обраний метод зберігання, можна створити єдиний метод виводу на всі три типи даних
    def get(self):
        number = ''
        if self.base == 2:
            i = 0
            while self.numblock[0][i] != '1':
                i += 1
            self.numblock[0] = self.numblock[0][i:]
        for i in range(len(self.numblock)):
            number += str(self.numblock[i])
        return number
    '''у наступних двох функціях записані фрагменти коду, які часто б повторювалися у двійкових і десяткових операціях відповідно
    тож для зручності ці рядки були виділені окремо'''
    def BinaryOp(self):
        num1 = BigInt(self.num)
        num1.setBin()
        return num1

    def decimop(self):
        num1 = BigInt(self.num)
        num1.setDecim()
        return num1

    '''
    число зберігається в блоках, кожен з яких важить 64 біти, отримаємо двійковий запис числа, у циклі
    побітово виконуємо операцію XOR на кожному елементі кожного блоку у подальшому переводимо результат
    у 16 сч
    '''
    def XOR(self, num1, num2):
        if num1.base != 2:
            num1 = num1.BinaryOp()
        if num2.base != 2:
            num2 = num2.BinaryOp()
        num3 = ''
        for i in range(len(num1.numblock)):
            for j in range(len(num1.numblock[i])):
                if num1.numblock[i][j] == num2.numblock[i][j]:
                    num3 += '0'
                else:
                    num3 += '1'
        num3 = hex(int(num3, 2))[2:]
        return num3
    '''
    всі побітові операції мають подібний принцип до XOR, різниця лише в кількості аргументів і логічних діях,
    які виконуються над діями
    '''
    def INV(self, num1):
        if num1.base != 2:
            num1 = num1.BinaryOp()
        numres = ''
        #
        for i in range(len(num1.numblock)):
            for j in range(len(num1.numblock[i])):
                if num1.numblock[i][j] == '1':
                    numres += '0'
                else:
                    numres += '1'
        numres = hex(int(numres, 2))[2:]
        return numres

    def AND(self, num1, num2):
        if num1.base != 2:
            num1 = num1.BinaryOp()
        if num2.base != 2:
            num2 = num2.BinaryOp()
        num3 = ''
        for i in range(len(num1.numblock)):
            for j in range(len(num1.numblock[i])):
                if num1.numblock[i][j] == '1' and num2.numblock[i][j] == '1':
                    num3 += '1'
                else:
                    num3 += '0'
        num3 = hex(int(num3, 2))[2:]
        return num3

    def OR(self, num1, num2):
        if num1.base != 2:
            num1 = num1.BinaryOp()
        if num2.base != 2:
            num2 = num2.BinaryOp()
        num3 = ''
        for i in range(len(num1.numblock)):
            for j in range(len(num1.numblock[i])):
                if num1.numblock[i][j] == '1' or num2.numblock[i][j] == '1':
                    num3 += '1'
                else:
                    num3 += '0'
        num3 = hex(int(num3, 2))[2:]
        return num3

    def shiftR(self, num1, shift):
        if num1.base != 2:
            num1 = num1.BinaryOp()
        #для зсуву переводимо число у двійковий рядок і після цього переставляємо частини рядка правильним чином
        num1 = num1.get()
        return num1[len(num1) - shift:] + num1[:len(num1) - shift]

    def shiftL(self, num1, shift):
        if num1.base != 2:
            num1 = num1.BinaryOp()
        num1 = num1.get()
        return num1[shift:] + num1[:shift]

    '''
    якщо внаслідок додавання утворилося число, яке має більше 16 розрядів, то зайві розряди треба перенести
    в наступний рядок, так як унаслідок додавання двох 16ти розрядних чисел не може утворитися число, що має
    більше 17ти розрядів, то і переносимо лише перший елемент результуючого рядка і робимо зріз викидаючи перший елемент
    '''
    def ADD(self, num1, num2):
        if num1.base != 10:
            num1 = num1.decimop()
        if num2.base != 10:
            num2 = num2.decimop()
        numr = []
        numres = ''
        for i in range(len(num1.numblock) - 1, -1, -1):
            numr.insert(0, str(int(num1.numblock[i]) + int(num2.numblock[i])))
            if len(numr[0]) > 16:
                num1.numblock[i - 1] = int(num1.numblock[i - 1]) + int(numr[0][0])
                numr[0] = numr[0][1:]
        for i in range(len(numr)):
            numres = numres + str(numr[i])
        return hex(int(numres))[2:]

    def SUB(self, num1, num2):
        if num1.base != 10:
            num1 = num1.decimop()
        if num2.base != 10:
            num2 = num2.decimop()
        numr = []
        numres = ''
        for i in range(len(num1.numblock) - 1, -1, -1):
        #якщо число в і-тому блоці першого числа менше за число в і-тому блоці другого, то переносимо останнє число
        #наступного розряду на початок першого числа
            if int(num1.numblock[i]) < int(num2.numblock[i]):
                num1.numblock[i] = num1.numblock[i - 1][15] + num1.numblock[i]
                num1.numblock[i - 1] = num1.numblock[i - 1][:15] + '0'
            numr.insert(0, str(int(num1.numblock[i]) - int(num2.numblock[i])))
            while len(numr[0]) < 16:
                numr[0] = '0' + numr[0]
        #за аналогічною логікою до додавання, лише перший елемент може вилізати з блоку, тому лише його
        #відокремлюємемо від акутального блоку і лише це число ми повертаємо в блок першого числа, з якого
        #забрали останню цифру
            if len(numr[0]) > 16:
                num1.numblock[i - 1] = str(int(num1.numblock[i - 1]) + int(numr[0][0]))
                numr[0] = numr[0][1:]
        for i in range(len(numr)):
            numres = numres + str(numr[i])
        return hex(int(numres))[2:]

    def MODP(self, num1, m):
        if num1.base != 10:
            num1 = num1.decimop()
        num1 = int(num1.get())
        return num1 % m
