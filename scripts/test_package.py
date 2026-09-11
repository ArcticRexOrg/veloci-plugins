import hashlib
import json
from unittest.mock import patch
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

from package import package


class PackageTest(unittest.TestCase):
    def test_exact_committed_contents_and_reproducibility(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = package(Path(tmp) / 'first')
            second = package(Path(tmp) / 'second')
            self.assertEqual(first.read_bytes(), second.read_bytes())
            expected = subprocess.check_output([
                'git', 'ls-tree', '-r', '--name-only', 'HEAD', '--', 'plugins/veloci/'
            ]).decode().splitlines()
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(archive.namelist(), sorted(
                    path.removeprefix('plugins/veloci/') for path in expected))
                for path in ('.mcp.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
                    self.assertIn(path, archive.namelist())
                for info in archive.infolist():
                    self.assertEqual(archive.read(info), subprocess.check_output([
                        'git', 'show', f'HEAD:plugins/veloci/{info.filename}']))
                    mode = subprocess.check_output([
                        'git', 'ls-tree', 'HEAD', '--', f'plugins/veloci/{info.filename}'
                    ]).decode().split()[0]
                    self.assertEqual(info.external_attr >> 16, int(mode, 8))
            self.assertEqual(first.with_suffix('.zip.sha256').read_text(),
                             f'{hashlib.sha256(first.read_bytes()).hexdigest()}  {first.name}\n')

    def test_manifest_mismatch_creates_no_artifact(self):
        import package as module
        original = module.git
        def inconsistent_git(*args):
            data = original(*args)
            if args[:2] == ("cat-file", "blob"):
                try:
                    manifest = json.loads(data)
                except (ValueError, UnicodeDecodeError):
                    return data
                if isinstance(manifest, dict) and "interface" in manifest:
                    manifest["version"] = "999.999.999"
                    return json.dumps(manifest).encode()
            return data
        with tempfile.TemporaryDirectory() as tmp, patch.object(module, "git", inconsistent_git):
            output = Path(tmp) / "dist"
            with self.assertRaisesRegex(ValueError, "same numeric release version"):
                package(output)
            self.assertFalse(output.exists())

    def test_tag_mismatch_creates_no_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'dist'
            with self.assertRaisesRegex(ValueError, 'must match plugin version'):
                package(output, 'v999.999.999')
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
