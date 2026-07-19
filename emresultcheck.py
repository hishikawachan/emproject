#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_csv_rows.py

複数のCSVファイルを連続して読み込み、条件に合致した行を
別のCSVファイルに書き出すプログラム。

【使い方の例】
1) input_dir 内の *.csv を対象に、"status" 列が "OK" の行を抽出
    python extract_csv_rows.py --input-dir ./input --output result.csv --condition "status==OK"

2) 複数ファイルを個別に指定し、"amount" 列が 1000 より大きい行を抽出
    python extract_csv_rows.py --files a.csv b.csv --output result.csv --condition "amount>1000"

3) 複数条件（AND）: status が OK かつ amount が 1000 以上
    python extract_csv_rows.py --input-dir ./input --output result.csv \
        --condition "status==OK" --condition "amount>=1000" --logic and

4) 複数条件（OR）: status が ERROR または WARN
    python extract_csv_rows.py --input-dir ./input --output result.csv \
        --condition "status==ERROR" --condition "status==WARN" --logic or

5) 対応する演算子: == != > >= < <= contains
   例: "name contains 田中"

6) 抽出条件をもっと複雑にしたい場合は match_condition() 関数を直接書き換えてください。
"""

import argparse
import csv
import glob
import os
import sys


OPERATORS = ["==", "!=", ">=", "<=", ">", "<", "contains"]


def parse_condition(cond_str: str):
    """
    "列名<演算子>値" 形式の文字列を (列名, 演算子, 値) に分解する。
    例: "amount>1000" -> ("amount", ">", "1000")
        "name contains 田中" -> ("name", "contains", "田中")
    """
    if " contains " in cond_str:
        col, val = cond_str.split(" contains ", 1)
        return col.strip(), "contains", val.strip()

    for op in ["==", "!=", ">=", "<="]:
        if op in cond_str:
            col, val = cond_str.split(op, 1)
            return col.strip(), op, val.strip()
    for op in [">", "<"]:
        if op in cond_str:
            col, val = cond_str.split(op, 1)
            return col.strip(), op, val.strip()

    raise ValueError(
        f"条件の形式が不正です: '{cond_str}' "
        f"(対応演算子: {', '.join(OPERATORS)})"
    )


def evaluate_condition(row: dict, col: str, op: str, val: str) -> bool:
    """1行(dict)が条件を満たすか判定する"""
    if col not in row:
        return False

    cell = row[col]

    if op == "contains":
        return val in cell

    try:
        cell_num = float(cell)
        val_num = float(val)
        if op == "==":
            return cell_num == val_num
        if op == "!=":
            return cell_num != val_num
        if op == ">":
            return cell_num > val_num
        if op == ">=":
            return cell_num >= val_num
        if op == "<":
            return cell_num < val_num
        if op == "<=":
            return cell_num <= val_num
    except (ValueError, TypeError):
        if op == "==":
            return cell == val
        if op == "!=":
            return cell != val
        if op == ">":
            return cell > val
        if op == ">=":
            return cell >= val
        if op == "<":
            return cell < val
        if op == "<=":
            return cell <= val

    return False


def match_condition(row: dict, conditions: list, logic: str) -> bool:
    """
    行(dict)が条件リストに合致するか判定する。
    logic: "and" ならすべての条件を満たす場合True、"or" なら一つでも満たせばTrue。
    条件が空の場合は常にTrue(全行抽出)。
    """
    if not conditions:
        return True

    results = [evaluate_condition(row, col, op, val) for col, op, val in conditions]

    if logic == "and":
        return all(results)
    else:
        return any(results)


def collect_input_files(input_dir: str, files: list, pattern_glob: str) -> list:
    """処理対象となるファイル一覧を収集する"""
    target_files = []

    if files:
        target_files.extend(files)

    if input_dir:
        target_files.extend(sorted(glob.glob(os.path.join(input_dir, pattern_glob))))

    seen = set()
    unique_files = []
    for f in target_files:
        if f not in seen and os.path.isfile(f):
            unique_files.append(f)
            seen.add(f)
    return unique_files


def read_csv_rows(filepath: str):
    """
    CSVファイルをDictReaderで読み込む。
    utf-8-sig を優先し、失敗したら cp932(Shift_JIS系)で再試行する。
    """
    encodings_to_try = ["utf-8-sig", "cp932"]
    last_error = None
    for enc in encodings_to_try:
        try:
            with open(filepath, "r", encoding=enc, newline="") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                rows = list(reader)
            return fieldnames, rows
        except UnicodeDecodeError as e:
            last_error = e
            continue
    raise last_error


def main():
    parser = argparse.ArgumentParser(description="複数CSVファイルから条件に合う行を抽出する")
    parser.add_argument("--input-dir", help="読み込み対象ファイルがあるディレクトリ")
    parser.add_argument("--glob", default="*.csv", help="input-dir 内で対象とするファイルパターン(デフォルト: *.csv)")
    parser.add_argument("--files", nargs="*", help="個別に指定するファイルパス(複数可)")
    parser.add_argument("--output", required=True,  help="書き出し先ファイルパス")
    parser.add_argument(
        "--condition", action="append", 
        help='条件式。"列名==値" のように指定。複数指定可(--condition を繰り返す)'
    )
    
    parser.add_argument("--logic", choices=["and", "or"], default="and",
                         help="複数条件の結合方法(デフォルト: and)")
    parser.add_argument("--with-source", action="store_true",
                         help="出力に元ファイル名の列(source_file)を追加する")
    parser.add_argument("--encoding-out", default="utf-8-sig",
                         help="出力ファイルのエンコーディング(デフォルト: utf-8-sig。Excelでの文字化け対策)")
    

    args = parser.parse_args()

    if not args.input_dir and not args.files:
        parser.error("--input-dir か --files のいずれかを指定してください")

    conditions = [parse_condition(c) for c in args.condition]

    target_files = collect_input_files(args.input_dir, args.files, args.glob)
    if not target_files:
        print("対象ファイルが見つかりませんでした。", file=sys.stderr)
        sys.exit(1)

    print(f"対象ファイル数: {len(target_files)} 件")
    for f in target_files:
        print(f"  - {f}")

    matched_rows = []
    total_rows = 0
    output_fieldnames = None

    for filepath in target_files:
        try:
            fieldnames, rows = read_csv_rows(filepath)
        except Exception as e:
            print(f"警告: {filepath} の読み込み中にエラーが発生しました: {e}", file=sys.stderr)
            continue

        if fieldnames is None:
            continue

        if output_fieldnames is None:
            output_fieldnames = list(fieldnames)
            if args.with_source:
                output_fieldnames.append("source_file")

        for row in rows:
            total_rows += 1
            if match_condition(row, conditions, args.logic):
                if args.with_source:
                    row = dict(row)
                    row["source_file"] = os.path.basename(filepath)
                matched_rows.append(row)

    if output_fieldnames is None:
        print("有効なCSVファイルを読み込めませんでした。", file=sys.stderr)
        sys.exit(1)

    with open(args.output, "w", encoding=args.encoding_out, newline="") as out_f:
        writer = csv.DictWriter(out_f, fieldnames=output_fieldnames)
        writer.writeheader()
        for row in matched_rows:
            writer.writerow(row)

    print(f"\n処理完了: 全 {total_rows} 行中 {len(matched_rows)} 行を抽出しました。")
    print(f"出力先: {args.output}")


if __name__ == "__main__":
    main()