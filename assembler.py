import struct
import argparse

def assemble(input_file, output_file, commands_file):
    COMMANDS = {
        "LOAD_CONST": 0xD6,
        "WRITE_MEM": 0xBD,
        "SHIFT_LEFT": 0xF3
    }

    with open(input_file, "r") as infile, open(output_file, "wb") as outfile, open(commands_file, "w") as cmdfile:
        cmdfile.write("Command,Arguments\n")
        for line in infile:
            parts = line.strip().split()
            if not parts or parts[0].startswith("#"):
                continue

            cmd = parts[0]
            args = list(map(int, parts[1:]))

            if cmd in COMMANDS:
                outfile.write(struct.pack("B", COMMANDS[cmd]))
                cmdfile.write(f"{cmd},{' '.join(map(str, args))}\n")

                for arg in args:
                    outfile.write(struct.pack("I", arg))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembler for a custom virtual machine.")
    parser.add_argument("input_file", help="Input assembly file.")
    parser.add_argument("output_file", help="Output binary file.")
    parser.add_argument("commands_file", help="Commands CSV file.")

    args = parser.parse_args()

    assemble(args.input_file, args.output_file, args.commands_file)
