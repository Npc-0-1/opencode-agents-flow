import argparse, os, sys, datetime
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--content', nargs='*', default=None)
    parser.add_argument('--category', default='tech-decision')
    parser.add_argument('--file', default=None)
    args, unknown = parser.parse_known_args()

    if args.content is None and unknown:
        args.content = unknown
    if not args.content:
        print("No content provided")
        sys.exit(1)

    content_text = ' '.join(args.content)
    category_map = {
        'tech-decision': '技术决策',
        'project-status': '项目状态',
        'preference': '用户偏好',
        'issue': '问题记录',
    }
    category_label = category_map.get(args.category, args.category)

    script_dir = Path(__file__).resolve().parent
    file_path = Path(args.file) if args.file else script_dir.parent / 'references' / 'memory.md'
    file_path = file_path.resolve()

    today = datetime.date.today().strftime('%Y-%m-%d')
    today_header = f'## {today}'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if today_header not in content:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'\n\n{today_header}\n\n### 技术决策\n\n### 项目状态\n\n### 用户偏好\n\n### 问题记录\n')
        content = content + f'\n\n{today_header}\n\n### 技术决策\n\n### 项目状态\n\n### 用户偏好\n\n### 问题记录\n'

    lines = content.split('\n')
    category_header = f'### {category_label}'
    insert_pos = None
    for i, line in enumerate(lines):
        if line.strip() == category_header:
            # find the next section or end to insert
            insert_pos = i + 1
            break

    if insert_pos is None:
        print(f"Category '{category_label}' not found in file")
        sys.exit(1)

    # check if next line is empty, if so insert after empty lines
    while insert_pos < len(lines) and lines[insert_pos].strip() == '':
        insert_pos += 1

    entry = f'- {content_text}'
    lines.insert(insert_pos, entry)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Memory saved: [{args.category}] {content_text}")

if __name__ == '__main__':
    main()
