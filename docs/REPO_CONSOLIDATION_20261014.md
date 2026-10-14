# F14 repository consolidation - 2026-10-14

`F14-RC-Model` is the sole Git repository for the RC F-14 project.

Imported from the foreign `135er-Spandau-Defeat` repository before cleanup:

- `origin/codex/f14-cad-v05` - historical `side-projects/F14_TOMCAT_RC` snapshot.
- `origin/codex/f14-engineering-audit-20261004` - earlier engineering-audit snapshot.
- `origin/lyra-ue5-gis` - historical `side-projects/F14_RC_FDM` / R3 snapshot and F14 workflows.
- `origin/publish-main-fix` - alternate R3 snapshot and F14 workflows.
- two untracked spar-analysis files recovered from the old Codex F14 worktree.

Exact source commit/tree IDs are stored in each imported snapshot `SOURCE.txt`.

Policy from this checkpoint forward:

- no F14/Tomcat project source, CAD, analysis, print files, docs, or CI workflows belong in Spandau Strike or any other project repository;
- new F14 work is committed only to `F14-RC-Model`;
- foreign historical snapshots live under `legacy/` and are retained only for traceability/recovery;
- active development stays in the normal top-level `analysis/`, `cad/`, `docs/`, `hardware/`, `manufacturing/`, `references/`, `test/`, and `workspace/` trees.
