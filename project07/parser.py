from enum import Enum, auto


class Command(Enum):
    C_ARITHMETIC = auto()
    C_PUSH = auto()
    C_POP = auto()
    C_LABEL = auto()
    C_GOTO = auto()
    C_IF = auto()
    C_FUNCTION = auto()
    C_RETURN = auto()
    C_CALL = auto()


def split_command(l: str):
    parts = l.split()
    if len(parts) == 0:
        raise Exception("不正な命令です。")

    return parts


class Parser:
    """VMコードを読み取り、構成要素に分解する。 初期化直後、必ず `Parser.advance()` を呼び出す必要がある。"""

    def __init__(self, source_path: str):
        with open(source_path) as f:
            raw_lines = f.readlines()

        self.lines = self._strip_raw_lines(raw_lines)
        self.cur = -1

    def _strip_raw_lines(self, raw_lines: list[str]) -> list[str]:
        lines = []
        for l in raw_lines:
            comment_idx = l.find("//")

            # コメント削除
            if comment_idx >= 0:
                l = l[:comment_idx]

            # 余分な空白削除
            l = l.strip()

            # 内容が残っていれば self.lines に追加
            if l:
                lines.append(l)
        return lines

    def hasMoreLines(self):
        return self.cur < len(self.lines) - 1

    @property
    def current_line(self) -> str:
        return self.lines[self.cur]

    def advance(self):
        if not self.hasMoreLines():
            raise Exception("もう行が存在しません")

        self.cur += 1

    def commandType(self) -> Command:
        parts = split_command(self.current_line)
        command = parts[0]

        # TODO: 他のコマンドタイプを追加する。
        match command:
            case "push":
                return Command.C_PUSH
            case "pop":
                return Command.C_POP
            case "add" | "sub" | "neg" | "eq" | "gt" | "lt" | "and" | "or" | "not":
                return Command.C_ARITHMETIC
            case _:
                raise Exception("不正な Command Type です。")

    def arg1(self) -> str:
        if self.commandType() == Command.C_RETURN:
            return None

        parts = split_command(self.current_line)

        command = parts[0]
        if self.commandType() == Command.C_ARITHMETIC:
            return command

        arg1 = parts[1]

        return arg1

    def arg2(self) -> int:
        if not self.commandType() in (
            Command.C_PUSH,
            Command.C_POP,
            Command.C_FUNCTION,
            Command.C_CALL,
        ):
            return None

        parts = split_command(self.current_line)
        if len(parts) < 3:
            raise Exception("引数の数が足りません")
        arg2 = parts[2]
        return arg2


if __name__ == "__main__":
    source = "BasicTest.vm"
    p = Parser(source_path=source)
    while p.hasMoreLines():
        p.advance()
        print(
            f"{p.current_line:20}\t| {p.commandType():20} {p.arg1():10} {str(p.arg2()):10}"
        )
