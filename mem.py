class Memory:
    def __init__(self, mem_sz=128):
        self.addrs = []
        self.value = [0] * mem_sz

        for i in range(mem_sz):
            self.addrs.append(hex(i))

    def write(self, address, value):
        self.value[int(address, 16)] = bin(int(value, 2))

    def read_one(self, address):
        return self.value[int(address, 16)], address

    def read_all(self):
        return self.value, self.addrs

    def clear(self):
        self.value = [0] * len(self.value)


is_running = True
mem = Memory()

while is_running:
    cmd = input("MEM_SIM>")
    if cmd == "read":
        addr = input("ADDRESS:")
        print(mem.read_one(addr))
    elif cmd == "write":
        addr = input("ADDRESS:")
        value = input("VALUE:")
        mem.write(addr, value)
    elif cmd == "print":
        print(mem.read_all())
    elif cmd == "clear":
        mem.clear()
