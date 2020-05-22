"""CPU functionality."""

import sys

HLT = 1
PRN = 71
LDI = 130
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 0xf3 #243
        self.next_function_address = 0
        self.branchtable = {}
        self.branchtable[162] = self.multiply
        self.branchtable[130] = self.ldi
        self.branchtable[71] = self.prn
        self.branchtable[70] = self.pop
        self.branchtable[69] = self.push
        self.branchtable[80] = self.call
        self.branchtable[160] = self.add
        self.branchtable[17] = self.ret

    def load(self):
        """Load a program into memory."""
        file_path = sys.argv[1]
        program = open(f"{file_path}", "r")
        address = 0
        for line in program:
            if line[0] == "0" or line[0] == "1":
                command = line.split("#", 1)[0]
                self.ram[address] = int(command, 2)
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR
        return self.ram[MAR]

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def multiply(self, a, b):
        multiple = self.reg[a] * self.reg[b]
        self.reg[a] = multiple
        self.pc += 3

    def ldi(self, a, b):
        self.reg[a] = b
        self.pc += 3

    def prn(self, a, b):
        print(self.reg[a])
        self.pc += 2

    def call(self, a, b):
        self.next_function_address = self.pc + 2
        self.pc = self.reg[a]
        while self.ram[self.pc] != 0:
            instruction = self.ram[self.pc]
            if instruction != 17:
                self.branchtable[instruction](self.ram[self.pc + 1], self.ram[self.pc + 2])
            elif instruction == 17:
                self.pc = self.next_function_address
                break

    def ret(self, a, b):
        self.pc = self.next_function_address

    def add(self, a, b):
        # print("a", a)
        # print("b", b)
        self.reg[a] += self.reg[b]
        self.pc += 3

    def push(self, a, b):
        self.sp -= 1
        self.ram[self.sp] = self.reg[a]
        self.pc += 2

    def pop(self, a, b):
        value = self.ram[self.sp]
        self.reg[a] = value
        self.sp += 1
        self.pc += 2

    def run(self):
        halted = False
        while not halted:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if instruction == HLT:
                halted = True
            else:
                self.branchtable[instruction](operand_a, operand_b)

# cpu = CPU()

# cpu.load()
# print(cpu.ram)