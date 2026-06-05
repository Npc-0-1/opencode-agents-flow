---
name: skill-installer
description: Install opencode skills into the local skills directory from a user-provided GitHub repo/path or URL. Use when a user asks to install a skill from another repo or supplied URL. Uses download/API methods only; never runs git commands.
metadata:
  short-description: Install skills from supplied sources
---

# Skill Installer

Helps install skills from a user-provided GitHub repo/path or URL. There is no maintained default curated source; require the user to provide a GitHub repo/path or URL.

Use the helper scripts based on the task:
- List skills only when the user provides a GitHub repo/path.
- Install from another repo when the user provides a GitHub repo/path, including private repos.
- Install from URL when the user provides a supported GitHub URL.

Install skills with the helper scripts.

## Communication

When listing skills, output approximately as follows, depending on the context of the user's request:
"""
Skills from {repo}:
1. skill-1
2. skill-2 (already installed)
3. ...
Which ones would you like installed?
"""

After installing a skill, tell the user: "Restart opencode to pick up new skills."

## Scripts

All of these scripts use network. Run network operations only after the user explicitly authorizes them. If the current runtime cannot request authorization or cannot access the network, report the blocker and provide the exact manual command for the user to run. Continue to use download/API methods only; never use git fallback.

- `scripts/list-skills.py` (prints skills list with installed annotations)
- `scripts/list-skills.py --repo <owner>/<repo> --path <path/to/skills>`
- `scripts/list-skills.py --repo <owner>/<repo> --path <path/to/skills> --format json`
- `scripts/install-skill-from-github.py --repo <owner>/<repo> --path <path/to/skill> [<path/to/skill> ...]`
- `scripts/install-skill-from-github.py --url https://github.com/<owner>/<repo>/tree/<ref>/<path>`

## Behavior and Options

- Defaults to direct download for public GitHub repos.
- If download fails with auth/permission errors, report the gap and ask the user to provide a token or manually supply the files. Do not use git fallback.
- Aborts if the destination skill directory already exists.
- Installs into the local opencode skills directory by default: `~/.config/opencode/skills/<skill-name>`.
- Multiple `--path` values install multiple skills in one run, each named from the path basename unless `--name` is supplied.
- Options: `--ref <ref>` (default `main`), `--dest <path>`, `--method download`.

## Notes

- Default curated listing is no longer maintained. If the user asks to list skills, ask for a compatible repo/path unless they already provided one.
- Private GitHub repos require `GITHUB_TOKEN`/`GH_TOKEN` or user-supplied files. Do not rely on git credentials or git fallback.
- 本地文件需要手动复制/人工校验；不要把本地路径描述为 helper scripts 支持的安装来源。
- Installed annotations come from the configured local skills directory.
