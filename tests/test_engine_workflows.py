"""Version and source-selection regressions for the shipped desktop reader."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1] / "plugins" / "codex-unreal-engine-skills"
SKILL = PACKAGE / "skills" / "unreal-engine-workflows"


def lookup(*args):
    return subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "engine_workflows.py"), *map(str, args)],
        capture_output=True, encoding="utf-8", check=False,
    )


class EngineWorkflowsTest(unittest.TestCase):
    def test_entry_selection_by_version(self):
        common = "BlueprintBasicsSkill"
        extra = "/Skills/Engine/unreal-log-triage"
        for version in ("5.8.4", "5.9.0"):
            self.assertEqual(lookup("--version", version, "--show", common).returncode, 0)
        self.assertNotEqual(lookup("--version", "5.8", "--show", extra).returncode, 0)
        self.assertEqual(lookup("--version", "5.9", "--show", extra).returncode, 0)
        self.assertNotEqual(lookup("--version", "5.10", "--show", common).returncode, 0)
        self.assertNotEqual(lookup("--show", common).returncode, 0)

    def test_selected_installation_controls_the_source(self):
        with tempfile.TemporaryDirectory() as sandbox:
            # A misleading directory name must never select the other series.
            installation = Path(sandbox) / "UE_5.9"
            engine = installation / "Engine"
            (engine / "Build").mkdir(parents=True)
            (engine / "Build/Build.version").write_text(
                json.dumps({"MajorVersion": 5, "MinorVersion": 8}), encoding="utf-8"
            )
            path = engine / "Plugins/Experimental/Toolsets/EditorToolset/Content/Python/editor_toolset/skills/blueprint_basics.py"
            path.parent.mkdir(parents=True)
            path.write_text(
                "raise AssertionError('engine files must not execute')\n"
                "GUIDE = 'Local 5.8 instructions'\n"
                "class BlueprintBasicsSkill:\n    instructions = GUIDE\n", encoding="utf-8",
            )
            for root in (installation, engine):
                result = lookup("--engine", root, "--show", "BlueprintBasicsSkill", "--source")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("UE 5.8", result.stdout)
                self.assertIn("Local 5.8 instructions", result.stdout)
                self.assertNotIn("AssertionError", result.stdout)
            mismatch = lookup("--engine", engine, "--version", "5.9", "--show", "BlueprintBasicsSkill")
            self.assertNotEqual(mismatch.returncode, 0)
            self.assertNotIn("Local 5.8 instructions", mismatch.stdout)


if __name__ == "__main__":
    unittest.main()
