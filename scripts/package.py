#!/usr/bin/env python3
"""Package only committed plugin files; CI publishes the resulting release assets."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

PREFIX = 'plugins/veloci/'


def git(*args):
    return subprocess.check_output(['git', *args])


def package(output, tag=None):
    commit = git('rev-parse', 'HEAD').decode().strip()
    entries = {}
    for entry in git('ls-tree', '-rz', commit, '--', PREFIX).split(b'\0'):
        if not entry:
            continue
        metadata, raw_path = entry.split(b'\t', 1)
        mode, kind, object_id = metadata.decode().split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Plugin must contain only regular files')
        name = raw_path.decode().removeprefix(PREFIX)
        entries[name] = (int(mode, 8), git('cat-file', 'blob', object_id))
    versions = [json.loads(entries[f'{host}/plugin.json'][1])['version']
                for host in ('.claude-plugin', '.codex-plugin')]
    version = versions[0]
    if versions != [version, version] or not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Plugin manifests must have the same numeric release version')
    if tag is not None and tag != f'v{version}':
        raise ValueError(f'Tag {tag!r} must match plugin version v{version}')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f'veloci-{version}.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, (mode, data) in sorted(entries.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = mode << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, data)
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix('.zip.sha256').write_text(f'{checksum}  {archive.name}\n')
    print(f'Packaged {len(entries)} files from {commit}: {archive}')
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='dist')
    parser.add_argument('--tag', help='Require this release tag to match both manifests')
    args = parser.parse_args()
    package(args.output, args.tag)
