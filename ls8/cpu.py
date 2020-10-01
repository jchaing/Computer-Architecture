"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # Memory:
        self.ram = [0] * 256

        # Register:
        self.reg = [0] * 8

        # Pointer:
        self.pc = 0

        # Running
        self.running = True

    def ram_read(self, address):
        """Returns value from memory address"""

        print(self.ram[address])

    def ram_write(self, value, address):
        """Writes value to memory address"""

        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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

    def run(self):
        """Run the CPU."""

        while self.running:
            IR = self.ram[self.pc]

            # LDI instruction
            if IR == 0b10000010:
                reg_idx = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]

                self.reg[reg_idx] = value
                self.pc += 2

            # PRN instruction
            elif IR == 0b01000111:
                reg_idx = self.ram[self.pc + 1]
                value = self.reg[reg_idx]
                print(value)

                self.pc += 1

            # HLT instruction
            elif IR == 0b00000001:
                self.running = False

            else:
                print("Unknown Command!")
                self.running = False

            self.pc += 1

        print(self.reg)
