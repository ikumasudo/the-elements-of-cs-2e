from parser import Command, split_command
from typing import Literal


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
        "D;JLE",
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


class CodeWriter:
    def __init__(self, asm_path: str):
        self.asm_file = open(asm_path, "w")

        self.jump_label_idx = 0

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

            asms = f"A=M-1\nD=M\nA=A-1\n{op}\nD=A+1\n@SP\nM=D\n"
            self.asm_file.write(asms)
        elif command in ("neg", "not"):
            if command == "neg":
                op = "M=-M"
            elif command == "not":
                op = "M=!M"

            asms = f"@SP\n@A=M-1\n{op}\n"
            self.asm_file.write(asms)
        elif command in ("eq", "gt", "lt"):
            eq = command == "eq"
            gt = command == "gt"
            lt = command == "lt"
            asms = get_comparison_asms(gt, lt, eq, self.jump_label_idx)
            asms_str = "\n".join(asms) + "\n"

            self.asm_file.write(asms_str)

            self.jump_label_idx += 1

    def writePushPop(
        self, command: Literal[Command.C_PUSH, Command.C_POP], segment: str, index: int
    ):
        pass

    def close(self):
        self.asm_file.close()
