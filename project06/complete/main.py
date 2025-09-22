from enum import Enum, auto
import argparse
from pprint import pprint


class ParsingError(Exception):
    """Hackアセンブリ言語のパース中に発生したエラーを表す基底例外"""

    pass


class InvalidInstructionError(ParsingError):
    """命令の形式が不正な場合に発生"""

    pass


class Instruction(Enum):
    A = auto()
    C = auto()
    L = auto()


def strip(l: str):
    index = l.find("//")
    if index >= 0:
        l = l[0:index]

    l = l.strip()

    return l


class Parser:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.cur = -1
        self.advance()

    def hasMoreLines(self):
        return self.cur + 1 < len(self.lines)

    def advance(self):
        for tmp_cur in range(self.cur + 1, len(self.lines)):
            l = self.lines[tmp_cur]
            l = strip(l)

            if len(l) > 0:
                self.cur = tmp_cur
                break

    def instruction_type(self):
        l = self.lines[self.cur].strip()

        if not l:
            raise InvalidInstructionError(f"空の命令です (行 {self.cur + 1})")

        if l.startswith("@"):
            return Instruction.A
        elif len(l) >= 2 and l[0] == "(" and l[-1] == ")":
            return Instruction.L
        elif "=" in l or ";" in l:
            return Instruction.C
        else:
            line_content = l
            raise InvalidInstructionError(
                f"不正な命令形式です (行 {self.cur + 1}: '{line_content}')"
            )

    def symbol(self):
        type = self.instruction_type()

        l = strip(self.lines[self.cur])
        if type == Instruction.L:
            return l.strip("()").strip()
        elif type == Instruction.A:
            return l[1:].strip()
        else:
            line_content = l
            raise ParsingError(
                f"C命令にはシンボルがありません (行 {self.cur + 1}: '{line_content}')"
            )

    def dest(self):
        l = self.lines[self.cur].strip()
        index = l.find("=")
        if index < 0:
            return None
        dest = l[:index]
        return dest

    def comp(self):
        l = self.lines[self.cur].strip()
        idx1 = l.find("=")
        idx2 = l.find(";")

        if idx1 < 0 and idx2 < 0:
            return None
        elif idx1 < 0 and idx2 > 0:
            return l[:idx2]
        elif idx1 > 0 and idx2 < 0:
            return l[idx1 + 1 :]
        else:
            return l[idx1 + 1 : idx2]

    def jump(self):
        l = self.lines[self.cur].strip()
        idx = l.find(";")
        if idx < 0:
            return None
        return l[idx + 1 :]


class Code:
    DEST = {
        "null": "000",
        "M": "001",
        "D": "010",
        "DM": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "ADM": "111",
    }
    COMP = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "M": "1110000",
        "!D": "0001101",
        "!A": "0110001",
        "!M": "1110001",
        "-D": "0001111",
        "-A": "0110011",
        "-M": "1110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "M+1": "1110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "M-1": "1110010",
        "D+A": "0000010",
        "D+M": "1000010",
        "D-A": "0010011",
        "D-M": "1010011",
        "A-D": "0000111",
        "M-D": "1000111",
        "D&A": "0000000",
        "D&M": "1000000",
        "D|A": "0010101",
        "D|M": "1010101",
    }
    JUMP = {
        "null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }

    @classmethod
    def dest(cls, s):
        key = "null" if s in (None, "") else s
        try:
            return cls.DEST[key]
        except KeyError as exc:
            raise KeyError(f"unknown dest mnemonic: {s}") from exc

    @classmethod
    def comp(cls, s):
        try:
            return cls.COMP[s]
        except KeyError as exc:
            raise KeyError(f"unknown comp mnemonic: {s}") from exc

    @classmethod
    def jump(cls, s):
        key = "null" if s in (None, "") else s
        try:
            return cls.JUMP[key]
        except KeyError as exc:
            raise KeyError(f"unknown jump mnemonic: {s}") from exc


class SymbolTable:
    def __init__(self):
        self.table: dict[str, int] = {
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576,
        }

    def addEntry(self, symbol: str, address: int):
        self.table[symbol] = address

    def contains(self, symbol: str) -> bool:
        return symbol in self.table

    def getAddress(self, symbol: str) -> int:
        return self.table[symbol]


class Hack:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.parser = Parser(lines)
        self.table = SymbolTable()

    def convert(self):
        row_number = -1
        while True:
            inst_type = self.parser.instruction_type()
            # 行番号。L命令は無視してカウント。
            if inst_type in (Instruction.A, Instruction.C):
                row_number += 1
            print(
                f"Row Number: {row_number:4}\tInstruction Type: {inst_type:1}\t{self.parser.lines[self.parser.cur].strip():20}"
            )
            if inst_type == Instruction.L:
                symbol = self.parser.symbol()
                if not self.table.contains(symbol):
                    address = row_number + 1
                    self.table.addEntry(symbol, address)
                    print(
                        f"Row Number: {row_number:4}\tNew Symbol: {symbol:30} at {address:5}"
                    )

            if self.parser.hasMoreLines():
                self.parser.advance()
            else:
                break

        # reset parser cursor
        self.parser = Parser(lines)

        # 次の変数用アドレス。R15のあとに続く。
        next_variable_addr = 16

        bin_lines = []
        while True:
            inst_type = self.parser.instruction_type()
            if inst_type == Instruction.A:
                symbol = self.parser.symbol()
                if symbol.isdigit():
                    binary_str = bin(int(symbol))[2:].zfill(16)
                    bin_lines.append(binary_str)
                elif self.table.contains(symbol):
                    addr_dec = self.table.getAddress(symbol)
                    addr_bin = bin(addr_dec)[2:].zfill(16)
                    bin_lines.append(addr_bin)
                else:
                    self.table.addEntry(symbol, next_variable_addr)
                    addr_bin = bin(next_variable_addr)[2:].zfill(16)
                    bin_lines.append(addr_bin)

                    next_variable_addr += 1

            elif inst_type == Instruction.C:
                dest = self.parser.dest()
                comp = self.parser.comp()
                jump = self.parser.jump()
                dest_bin = Code.dest(dest)
                comp_bin = Code.comp(comp)
                jump_bin = Code.jump(jump)
                bin_lines.append(f"111{comp_bin}{dest_bin}{jump_bin}")

            if self.parser.hasMoreLines():
                self.parser.advance()
            else:
                break
        return bin_lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic Hack Assembler")
    parser.add_argument("file", help=".asm file")
    parser.add_argument("out", help=".hack file")
    args = parser.parse_args()

    filename = args.file
    output_filename = args.out

    try:
        with open(filename) as f:
            lines = f.readlines()

        hack = Hack(lines)
        bin_lines = hack.convert()
        pprint(hack.table.table, indent=2)

        with open(output_filename, "w", encoding="utf-8") as out:
            out.write("\n".join(bin_lines))

    except FileNotFoundError:
        print(f"エラー: 入力ファイルが見つかりません: {filename}")
    except ParsingError as e:
        print(f"パースエラー: {e}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
