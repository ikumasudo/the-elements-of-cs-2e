import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic Hack Assembler")
    parser.add_argument("source", help=".vm file")
    args = parser.parse_args()

    source_file: str = args.source
    asm_file = source_file.replace(".vm", ".asm")
    print(source_file, asm_file)

    # try:
    #     with open(filename) as f:
    #         lines = f.readlines()

    #     hack = Hack(lines)
    #     bin_lines = hack.convert()

    #     with open(output_filename, "w", encoding="utf-8") as out:
    #         out.write("\n".join(bin_lines))

    # except FileNotFoundError:
    #     print(f"エラー: 入力ファイルが見つかりません: {filename}")
    # except ParsingError as e:
    #     print(f"パースエラー: {e}")
    # except Exception as e:
    #     print(f"予期せぬエラーが発生しました: {e}")
