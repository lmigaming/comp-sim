class Memory:
    def __init__(self, mem_sz=128):
        self.size = 128
        self.addrs = []
        self.value = [0] * mem_sz

        for i in range(mem_sz):
            self.addrs.append(i)

    def write(self, address, value):
        self.value[address] = value

    def read_one(self, address):
        return self.value[address], address

    def read_all(self):
        return self.value, self.addrs

    def clear(self):
        self.value = [0] * 128


class CPU:
    def __init__(self):
        self.reg = [0] * 4
        self.flags = [0] * 2
        self.pc = 0
        self.mem = Memory()
        self.isrunning = True
    
    def load(self, program):
        for i in range(len(program)):
            self.mem.write(address=i, value=program[i])

    def fetch(self):
        opcode = self.mem.read_one(address=self.pc)[0]
        operands = [self.mem.read_one(address=self.pc + i)[0] for i in range(1, 3)]
        self.pc += 3
        return opcode, operands
        
    def execute(self, opcode, operands):
        if self.isrunning:    
            if opcode == 0:
                self.reg[operands[0]] = self.mem.read_one(operands[1])[0]
            elif opcode == 1:
                self.mem.write(address=operands[0], value=self.reg[operands[1]])
            elif opcode == 2:
                self.reg[operands[0]] += self.reg[operands[1]]
                if self.reg[operands[0]] == 0:
                    self.flags[0] = 0b1
                elif len(str(self.reg[operands[0]])) > 8:
                    self.reg[operands[0]] = 0
                    self.flags[1] = 1
            elif opcode == 3:
                self.reg[operands[0]] -= self.reg[operands[1]]
                if self.reg[operands[0]] == 0:
                    self.flags[0] = 0b1
                elif len(str(self.reg[operands[0]])) > 8:
                    self.reg[operands[0]] = 0
                    self.flags[1] = 1
            elif opcode == 4:
                self.reg[operands[0]] *= self.reg[operands[1]]
                if self.reg[operands[0]] == 0:
                    self.flags[0] = 0b1
                elif len(str(self.reg[operands[0]])) > 8:
                    self.reg[operands[0]] = 0
                    self.flags[1] = 1
            elif opcode == 5:
                self.reg[operands[0]] /= self.reg[operands[1]]
                if self.reg[operands[0]] == 0:
                    self.flags[0] = 1
                elif len(str(self.reg[operands[0]])) > 8:
                    self.reg[operands[0]] = 0
                    self.flags[1] = 1
            elif opcode == 6:
                self.reg[operands[0]] = operands[1]
            elif opcode == 7:
                self.isrunning = False
        else:
            return 1

    def run(self):
        program = [6,0,1,6,1,2,2,0,1,7]
        self.load(program)
        while self.isrunning:
            print("Registers:", self.reg)
            print("Memory:", self.mem.read_all())
            print("Flags:", self.flags)
            print("Program Counter:", self.pc)
            opcode, operands = self.fetch()
            halt = self.execute(opcode, operands)
            if halt:
                print("HALTED")
                break

            if self.pc >= self.mem.size:
                self.mem.clear()
                print("Memory cleared.")
                self.pc = 0  # Reset program counter after clearing memory

def main():
    cpu = CPU()
    cpu.run()

if __name__ == "__main__":
    main()
