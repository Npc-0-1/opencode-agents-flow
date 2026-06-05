import argparse, sys, re, datetime
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', nargs='*', default=[])
    parser.add_argument('-c', '--category', default=None)
    parser.add_argument('--days', type=int, default=None)
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    file_path = script_dir.parent / 'references' / 'memory.md'

    if not file_path.exists():
        print("No memory file found")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = re.split(r'(^## \d{4}-\d{2}-\d{2})', content, flags=re.MULTILINE)
    entries = []
    current_date = None

    for part in sections:
        part = part.strip()
        if re.match(r'^## \d{4}-\d{2}-\d{2}', part):
            current_date = part.split()[-1]
        elif current_date and part:
            entries.append((current_date, part))

    # filter by days
    if args.days is not None:
        cutoff = datetime.date.today() - datetime.timedelta(days=args.days)
        entries = [(d, e) for d, e in entries if datetime.date.fromisoformat(d) >= cutoff]

    # filter by category
    if args.category:
        category_map = {
            'tech-decision': '技术决策',
            'project-status': '项目状态',
            'preference': '用户偏好',
            'issue': '问题记录',
        }
        cat_label = category_map.get(args.category, args.category)
        entries = [(d, e) for d, e in entries if f'### {cat_label}' in e]

    # filter by keyword
    if args.keyword:
        keywords = [k.lower() for k in args.keyword]
        filtered = []
        for d, e in entries:
            lower_e = e.lower()
            if any(k in lower_e for k in keywords):
                filtered.append((d, e))
        entries = filtered

    if not entries:
        # show recent 5 if no args
        if not args.keyword and not args.category and not args.days:
            entries = entries[-5:]
        if not entries:
            print("No matching memory found")
            return

    for date, entry in entries:
        print(f"[{date}]")
        # extract bullet points
        for line in entry.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                print(f"  {line}")
        print()

if __name__ == '__main__':
    main()
