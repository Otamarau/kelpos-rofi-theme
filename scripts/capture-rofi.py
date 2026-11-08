#!/usr/bin/env python3
"""Delay, then capture Rofi on one Hyprland monitor without the surrounding desktop."""
import argparse
import json
from pathlib import Path
import subprocess
import time


def query(command):
    return json.loads(subprocess.check_output(['hyprctl', '-j', command], text=True))


def layers(value):
    if isinstance(value, dict):
        if 'rofi' in str(value.get('namespace', '')).lower():
            yield value
        for child in value.values():
            yield from layers(child)
    elif isinstance(value, list):
        for child in value:
            yield from layers(child)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name', help='Screenshot name, e.g. launcher or wifi')
    parser.add_argument('--monitor', default='DP-1')
    parser.add_argument('--delay', type=float, default=20)
    parser.add_argument('--full-monitor', action='store_true')
    args = parser.parse_args()
    if args.delay < 0 or not args.name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.name):
        parser.error('Use a nonnegative delay and a name containing only letters, numbers, - or _.')
    output = Path(__file__).resolve().parents[1] / 'screenshots' / (args.name + '.png')
    if output.exists():
        parser.error(f'{output} already exists; choose a new name.')
    print(f'Capturing {args.monitor} in {args.delay:g} seconds. Open the desired Rofi tab there.', flush=True)
    time.sleep(args.delay)
    monitors = query('monitors')
    monitor = next((m for m in monitors if m['name'] == args.monitor), None)
    if monitor is None:
        raise SystemExit(f'Monitor {args.monitor} not found; run hyprctl monitors to check its name.')
    command = ['grim', '-o', args.monitor]
    if not args.full_monitor:
        candidates = [(int(v['x']), int(v['y']), int(v['w']), int(v['h']))
                      for v in layers(query('layers').get(args.monitor, {}))]
        if not candidates:
            for client in query('clients'):
                if client.get('monitor') == monitor['id'] and client.get('mapped', True) and 'rofi' in str(client.get('class', '')).lower():
                    candidates.append((*client['at'], *client['size']))
        if len(candidates) != 1:
            raise SystemExit('Expected one Rofi window on this monitor. Open it there and retry; no screenshot taken.')
        x, y, width, height = candidates[0]
        mw, mh = monitor['width'], monitor['height']
        if monitor.get('transform', 0) % 2:
            mw, mh = mh, mw
        scale = monitor.get('scale', 1)
        if not (width > 0 and height > 0 and x >= monitor['x'] and y >= monitor['y']
                and x + width <= monitor['x'] + mw / scale
                and y + height <= monitor['y'] + mh / scale):
            raise SystemExit('Rofi bounds are outside the selected monitor; no screenshot taken.')
        command += ['-g', f'{x},{y} {width}x{height}']
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(command + [str(output)], check=True)
    print(f'Saved {output}')


if __name__ == '__main__':
    main()
