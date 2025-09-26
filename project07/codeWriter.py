from parser import Command, split_command
from typing import Literal
from pathlib import Path


def get_comparison_asms(gt: bool, lt: bool, eq: bool, jump_label_idx: int) -> list[str]:
    asms = [
        "@SP",
        "A=M-1",
        "D=M",
        "A=A-1",
        # M: arg1, D: arg2
        "D=M-D",
        f"@A{jump_label_idx}",
        "D;JGT",
        f"@B{jump_label_idx}",
        "D;JLT",
        f"@C{jump_label_idx}",
        "D;JEQ",
        f"(A{jump_label_idx})",
        "@SP",
        "A=M-1",
        "A=A-1",
        f"M={-1 if gt else 0}",
        "D=A+1",
        "@SP",
        "M=D",
        f"@END{jump_label_idx}",
        "0;JMP",
        f"(B{jump_label_idx})",
        "@SP",
        "A=M-1",
        "A=A-1",
        f"M={-1 if lt else 0}",
        "D=A+1",
        "@SP",
        "M=D",
        f"@END{jump_label_idx}",
        "0;JMP",
        f"(C{jump_label_idx})",
        "@SP",
        "A=M-1",
        "A=A-1",
        f"M={-1 if eq else 0}",
        "D=A+1",
        "@SP",
        "M=D",
        f"@END{jump_label_idx}",
        "0;JMP",
        f"(END{jump_label_idx})",
    ]
    return asms


def get_segment_asms(op: Command, segment: str, i: int, prog_name: str) -> str:
    segment_pointer = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
    }

    if op == Command.C_PUSH:
        if segment in segment_pointer:
            asms = [
                f"@{segment_pointer[segment]}",
                "D=M",
                f"@{i}",
                "A=D+A",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]
            return "\n".join(asms) + "\n"
        elif segment == "pointer":
            t = "THIS" if i == 0 else "THAT"
            asms = [f"@{t}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
            return "\n".join(asms) + "\n"
        elif segment == "temp":
            asms = [
                "@5",
                "D=A",
                f"@{i}",
                "A=D+A",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]
            return "\n".join(asms) + "\n"
        elif segment == "constant":
            asms = [f"@{i}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
            return "\n".join(asms) + "\n"
        elif segment == "static":
            asms = [f"@{prog_name}.{i}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
            return "\n".join(asms) + "\n"
        else:
            raise Exception("不正なセグメントです")
    elif op == Command.C_POP:
        if segment in segment_pointer:
            asms = [
                f"@{segment_pointer[segment]}",
                "A=M",
                "D=A",
                f"@{i}",
                "D=D+A",
                "@R13",
                "M=D",
                "@SP",
                "A=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D",
                "@SP",
                "M=M-1",
            ]
            return "\n".join(asms) + "\n"
        elif segment == "temp":
            asms = [
                "@5",
                "D=A",
                f"@{i}",
                "D=D+A",
                "@R13",
                "M=D",
                "@SP",
                "A=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D",
                "@SP",
                "M=M-1",
            ]
            return "\n".join(asms) + "\n"
        elif segment == "pointer":
            print(i, type(i))
            t = "THIS" if i == 0 else "THAT"
            asms = [f"@SP", "A=M-1", "D=M", f"@{t}", "M=D", "@SP", "M=M-1"]
            return "\n".join(asms) + "\n"
        elif segment == "static":
            asms = ["@SP", "A=M-1", "D=M", f"@{prog_name}.{i}", "M=D", "@SP", "M=M-1"]
            return "\n".join(asms) + "\n"
        else:
            raise Exception("不正なセグメントです")


class CodeWriter:
    def __init__(self, prog_name: str):
        self.prog_name = prog_name
        asm_path = f"{prog_name}.asm"
        self.asm_file = open(asm_path, "w")

        self.jump_label_idx = 0

    def writeComment(self, comment: str):
        self.asm_file.write("//" + comment + "\n")

    def writeArithmetic(self, command: str):
        if command in ("add", "sub", "and", "or"):
            if command == "add":
                op = "M=D+M"
            elif command == "sub":
                op = "M=M-D"
            elif command == "and":
                op = "M=D&M"
            elif command == "or":
                op = "M=D|M"

            asms = f"@SP\nA=M-1\nD=M\nA=A-1\n{op}\n@SP\nM=M-1\n"
            self.asm_file.write(asms)
        elif command in ("neg", "not"):
            if command == "neg":
                op = "M=-M"
            elif command == "not":
                op = "M=!M"

            asms = f"@SP\nA=M-1\n{op}\n"
            self.asm_file.write(asms)
        elif command in ("eq", "gt", "lt"):
            eq = command == "eq"
            gt = command == "gt"
            lt = command == "lt"
            asms = get_comparison_asms(gt, lt, eq, self.jump_label_idx)
            asms_str = "\n".join(asms) + "\n"

            self.asm_file.write(asms_str)

            self.jump_label_idx += 1

    def writePushPop(self, command: Command, segment: str, index: int):
        asms = get_segment_asms(command, segment, index, self.prog_name)
        self.asm_file.write(asms)

    def close(self):
        self.asm_file.close()


if __name__ == "__main__":
    from parser import Parser

    try:
        source = "StaticTest.vm"
        vm_stem = Path(source).stem
        p = Parser(source_path=source)
        w = CodeWriter(prog_name=vm_stem)
        while p.hasMoreLines():
            p.advance()
            if p.commandType() in (Command.C_PUSH, Command.C_POP):
                c = f"{p.current_line:20}\t| {p.commandType():20} {p.arg1():10} {str(p.arg2()):10}"
                print(c)
                w.writeComment(c)
                w.writePushPop(p.commandType(), p.arg1(), p.arg2())
            else:
                c = f"{p.current_line:20}\t| {p.commandType():20} {p.arg1():10}"
                print(c)
                w.writeComment(c)
                w.writeArithmetic(p.arg1())
    except Exception as e:
        raise e
    finally:
        w.close()
