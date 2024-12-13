import struct
import argparse
import csv

class VirtualMachine:
    def __init__(self):
        self.memory = [0] * 256
        self.A = 0
        self.B = 0
        self.C = 0

    def execute(self, binary_file, result_file, memory_range):
        COMMANDS = {
            0xD6: "LOAD_CONST",
            0xBD: "WRITE_MEM",
            0xF3: "SHIFT_LEFT"
        }

        with open(binary_file, "rb") as infile, open(result_file, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Command", "Memory"])

            while True:
                byte = infile.read(1)
                if not byte:
                    break

                command = struct.unpack("B", byte)[0]

                if command == 0xD6:  # LOAD_CONST
                    self.A = struct.unpack("I", infile.read(4))[0]
                    self.B = struct.unpack("I", infile.read(4))[0]
                    self.C = struct.unpack("I", infile.read(4))[0]
                    print(f"LOAD_CONST: A={self.A}, B={self.B}, C={self.C}")
                    csv_writer.writerow(["LOAD_CONST", self.memory[memory_range[0]:memory_range[1]]])

                elif command == 0xBD:  # WRITE_MEM
                    self.memory[self.B] = self.memory[self.C]
                    print(f"WRITE_MEM: Memory[{self.B}] = {self.memory[self.B]}")
                    csv_writer.writerow(["WRITE_MEM", self.memory[memory_range[0]:memory_range[1]]])

                elif command == 0xF3:  # SHIFT_LEFT
                    self.memory[self.A] <<= 1
                    print(f"SHIFT_LEFT: Memory[{self.A}] = {self.memory[self.A]}")
                    csv_writer.writerow(["SHIFT_LEFT", self.memory[memory_range[0]:memory_range[1]]])

                else:
                    print(f"Нераспознанная команда: 0x{command:02X}")
                    break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter for a custom virtual machine.")
    parser.add_argument("binary_file", help="Input binary file.")
    parser.add_argument("result_file", help="Output CSV file.")
    parser.add_argument("--memory_range", nargs=2, type=int, default=[0, 10], help="Memory range to output in results.")

    args = parser.parse_args()

    vm = VirtualMachine()
    vm.execute(args.binary_file, args.result_file, args.memory_range)
