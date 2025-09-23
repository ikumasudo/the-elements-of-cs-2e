from parser import Command, split_command
import io


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
            # TODO: eq, gt, lt 対応版に変更する
            # gt
            # asms = [
            #     "@SP",
            #     "A=M-1",
            #     "D=M",
            #     "A=A-1",
            #     # M: arg1, D: arg2
            #     "D=M-D",
            #     f"@A{self.jump_label_idx}",
            #     "D;JGT",
            #     f"@B{self.jump_label_idx}",
            #     "D;JLE",
            #     f"(A{self.jump_label_idx})",
            #     "@SP",
            #     "A=M-1",
            #     "A=A-1",
            #     "M=-1",
            #     "D=A+1",
            #     "@SP",
            #     "M=D",
            #     f"@END{self.jump_label_idx}",
            #     "0;JMP",
            #     f"(B{self.jump_label_idx})",
            #     "@SP",
            #     "A=M-1",
            #     "A=A-1",
            #     "M=0",
            #     "D=A+1",
            #     "@SP",
            #     "M=D",
            #     f"@END{self.jump_label_idx}",
            #     "0;JMP",
            #     f"(END{self.jump_label_idx})",
            # ]

            self.jump_label_idx += 1

    def writePushPop(
        self, command: Command.C_PUSH | Command.C_POP, segment: str, index: int
    ):
        pass

    def close(self):
        self.asm_file.close()
