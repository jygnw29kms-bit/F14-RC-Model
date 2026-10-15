import argparse, json
from pathlib import Path

def resolve(profile_path: Path, root: Path, stack=None):
    stack = [] if stack is None else stack
    data = json.loads(profile_path.read_text(encoding='utf-8-sig'))
    name = data.get('name', profile_path.stem)
    if name in stack:
        raise RuntimeError('inheritance cycle: ' + ' -> '.join(stack + [name]))
    parent_name = data.get('inherits')
    if parent_name:
        parent_path = root / f'{parent_name}.json'
        if not parent_path.exists():
            raise FileNotFoundError(f'parent {parent_name!r} not found for {profile_path}')
        merged = resolve(parent_path, root, stack + [name])
        merged.update(data)
    else:
        merged = dict(data)
    merged.pop('inherits', None)
    return merged

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('profile')
    ap.add_argument('output')
    args = ap.parse_args()
    src = Path(args.profile)
    resolved = resolve(src, src.parent)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(resolved, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({
        'source': str(src), 'output': str(out), 'name': resolved.get('name'),
        'type': resolved.get('type'), 'printer_model': resolved.get('printer_model'),
        'nozzle_diameter': resolved.get('nozzle_diameter'),
        'filament_type': resolved.get('filament_type'),
        'filament_density': resolved.get('filament_density'),
        'layer_height': resolved.get('layer_height')
    }, indent=2))

if __name__ == '__main__':
    main()
