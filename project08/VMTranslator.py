import argparse
from parser import Parser
from codeWriter import CodeWriter, Command
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic Hack Assembler")
    parser.add_argument("source", help=".vm file")
    args = parser.parse_args()

    source: str = args.source
    prog_name = source.replace(".vm", "")

    try:
        vm_stem = Path(source).stem
        p = Parser(source_path=source)
        w = CodeWriter(prog_name=prog_name)
        while p.hasMoreLines():
            p.advance()
            if p.commandType() in (Command.C_PUSH, Command.C_POP):
                c = f"{p.current_line:30}| {p.commandType():20} {p.arg1():10} {str(p.arg2()):10}"
                print(c)
                w.writeComment(c)

                w.writePushPop(p.commandType(), p.arg1(), p.arg2())
            elif p.commandType() == Command.C_LABEL:
                c = f"{p.current_line:30}| {p.commandType():20} {p.arg1():10}"
                print(c)
                w.writeComment(c)

                w.writeLabel(p.arg1())
            elif p.commandType() == Command.C_GOTO:
                c = f"{p.current_line:30}| {p.commandType():20} {p.arg1():10}"
                print(c)
                w.writeComment(c)

                w.writeGoto(p.arg1())
            elif p.commandType() == Command.C_IF:
                c = f"{p.current_line:30}| {p.commandType():20} {p.arg1():10}"
                print(c)
                w.writeComment(c)

                w.writeIf(p.arg1())
            else:
                c = f"{p.current_line:30}| {p.commandType():20} {p.arg1():10}"
                print(c)
                w.writeComment(c)

                w.writeArithmetic(p.arg1())
    except Exception as e:
        raise e
    finally:
        w.close()
