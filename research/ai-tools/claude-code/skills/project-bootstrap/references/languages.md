# Bootstrap — per-language specifics

Pick the section that matches the project. Each lists the concrete tools and files for the
Stage-1 foundations. Defaults favor modern, low-config tooling.

---

## Python  *(default for AI/ML work)*

- **Environment + deps:** prefer **uv** (`uv init`, `uv add <pkg>`) or Poetry; otherwise
  `python -m venv .venv` + `pip` with a pinned `requirements.txt` (`pip freeze` or `pip-tools`).
  Use a `pyproject.toml` as the project manifest. Pin a Python version (`.python-version`).
- **Lint + format:** **ruff** (linter *and* formatter — one tool, fast, near-zero-config).
  Config in `pyproject.toml`:
  ```toml
  [tool.ruff]
  line-length = 100
  [tool.ruff.lint]
  select = ["E", "F", "I", "B", "UP"]
  ```
- **Test:** `pytest` (+ a `tests/` dir and one trivial `test_smoke.py`).
- **.gitignore essentials:** `.venv/`, `__pycache__/`, `*.pyc`, `.env`, `.pytest_cache/`,
  `.ruff_cache/`, `dist/`, `*.egg-info/`, and for ML: `data/`, `*.ckpt`, `*.pt`, `wandb/`,
  `.ipynb_checkpoints/`.
- **Structure:** `src/<package>/`, `tests/`, `pyproject.toml`, `.env.example`, `README.md`.
- **AI/ML extras (when relevant):** keep secrets (`OPENAI_API_KEY`, etc.) in `.env`, list them in
  `.env.example`; separate `notebooks/` from library code; never commit datasets or model
  weights — git-ignore them and document where they live.

## Node / TypeScript

- **Deps:** `npm init -y` (or pnpm/yarn); commit the lockfile. For TS: `typescript` + a
  `tsconfig.json` with `"strict": true`.
- **Lint + format:** **Prettier** (formatting) + **ESLint** (linting); `.prettierrc` + an ESLint
  config. For greenfield, **Biome** is a fast one-tool alternative.
- **Test:** **Vitest** or Jest, plus one smoke test.
- **.gitignore essentials:** `node_modules/`, `dist/`, `.env`, `coverage/`, `*.log`.
- **Scripts:** wire `dev`, `build`, `test`, `lint`, `format` into `package.json` `"scripts"`.
- **Structure:** `src/`, `tests/`, `package.json`, `tsconfig.json`, `.env.example`, `README.md`.

## Go

- **Deps:** `go mod init <module-path>`; `go.sum` is the lockfile.
- **Lint + format:** `gofmt`/`goimports` (formatting is settled by the language) + **golangci-lint**
  (`.golangci.yml`).
- **Test:** built-in `go test ./...`; add one `_test.go` smoke test.
- **.gitignore essentials:** compiled binaries, `.env`, `vendor/` (if not vendoring).
- **Structure:** idiomatic layout — `cmd/<app>/main.go`, `internal/`, `go.mod`, `.env.example`,
  `README.md`.

## Rust

- **Deps:** `cargo init`; `Cargo.lock` is the lockfile.
- **Lint + format:** `rustfmt` + `clippy` (`cargo clippy`).
- **Test:** built-in `cargo test`.
- **.gitignore essentials:** `/target`, `.env`.

---

## If the language isn't listed

Apply the same Stage-1 checklist with that ecosystem's idiomatic equivalents: a pinned dependency
manifest + lockfile, an isolated environment, the community-standard formatter and linter (prefer
the least-configurable one), a `.gitignore` that excludes build output and `.env`, an `.env.example`,
a README, and a runnable entry point with one passing smoke test. The principles are
language-independent; only the tool names change.
