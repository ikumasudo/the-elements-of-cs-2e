import argparse
from parser import Parser
from codeWriter import CodeWriter, Command
from pathlib import Path


def translate(p: Parser, w: CodeWriter):
    w.write_bootstrap()
    while p.hasMoreLines():
        p.advance()
        if p.commandType() in (Command.C_PUSH, Command.C_POP):
            c = f"{p.current_line:30}| {p.commandType():20} {p.arg1():10} {str(p.arg2()):10}"
            print(c)
            w.writeComment(c)

            w.writePushPop(p.commandType(), p.arg1(), p.arg2())
        elif p.commandType() == Command.C_CALL:
            c = f"{p.current_line:30}| {p.commandType():20} {p.arg1():10} {str(p.arg2()):10}"
            print(c)
            w.writeComment(c)

            w.writeCall(p.arg1(), str(p.arg2()))
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
        elif p.commandType() == Command.C_FUNCTION:
            c = f"{p.current_line:30}| {p.commandType():20} {p.arg1():10} {str(p.arg2()):10}"
            print(c)
            w.writeComment(c)

            w.writeFunction(p.arg1(), str(p.arg2()))
        elif p.commandType() == Command.C_RETURN:
            c = f"{p.current_line:30}| {p.commandType():20}"
            print(c)
            w.writeComment(c)

            w.writeReturn()
        elif p.commandType() == Command.C_ARITHMETIC:
            c = f"{p.current_line:30}| {p.commandType():20}"
            print(c)
            w.writeComment(c)

            w.writeArithmetic(p.arg1())
        else:
            c = f"{p.current_line:30}| {p.commandType():20}"
            print(c)
            w.writeComment(c)

            w.writeArithmetic(p.arg1())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic Hack Assembler")
    parser.add_argument("source", help=".vm file")
    args = parser.parse_args()

    source = Path(args.source)
    parsers: list[tuple[Path, Parser]] = []
    if source.is_file():
        prog_name = source.stem
        p = Parser(source_path=str(source))
        parsers.append((source, p))
    else:
        # `source` is a directory
        prog_name = source.stem
        for vm_file in source.glob("*.vm"):
            p = Parser(source_path=str(vm_file))
            parsers.append((vm_file, p))

    w: CodeWriter | None = None
    try:
        w = CodeWriter(prog_name=prog_name)

        for vm_file, p in parsers:
            w.setFileName(file_name=vm_file.stem)
            translate(p, w)

    except Exception as e:
        raise e
    finally:
        if w:
            w.close()
