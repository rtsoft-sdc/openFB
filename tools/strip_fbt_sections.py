import re
from pathlib import Path

dir_path = Path(r"c:\Users\Alex\Documents\GitHub\openfb\openfb\resources\function_blocks\iec61131\bitwiseOperators")

patterns = [
    re.compile(r"<Identification[\s\S]*?</Identification>\s*", re.IGNORECASE),
    re.compile(r"<VersionInfo[\s\S]*?</VersionInfo>\s*", re.IGNORECASE),
    re.compile(r"<CompilerInfo[\s\S]*?</CompilerInfo>\s*", re.IGNORECASE),
    re.compile(r"<Attribute[\s\S]*?/?>\s*", re.IGNORECASE),
]

for p in dir_path.glob('*.fbt'):
    text = p.read_text(encoding='utf-8')
    new = text
    for pat in patterns:
        new = pat.sub('', new)
    if new != text:
        p.write_text(new, encoding='utf-8')
        print(f"Updated: {p}")
    else:
        print(f"No change: {p}")
