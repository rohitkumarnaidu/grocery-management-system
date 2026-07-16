# Contributing to Grocery Management System 🛒

Thanks for your interest in contributing! Please read this guide carefully before opening a PR.

For local setup, refer to the **[Getting Started](README.md#getting-started)** section in the README.

---

## 1. Getting Assigned

- **Comment on the issue** you want to work on and wait to be assigned — do not start work before assignment.
- **Only work on issues assigned to you.** PRs for unassigned issues will be closed without review.
- If you go inactive for **7 days** after assignment with no progress, the issue may be reassigned.

---

## 2. Difficulty Labels & XP

| Label | XP |
|-------|----|
| `newbie` | 10 XP |
| `adventurer` | 25 XP |
| `veteran` | 50 XP |

---

## 3. Branch Naming

Create a fresh branch off the latest `main` using one of these prefixes:

| Type | Pattern |
|------|---------|
| New feature | `feat/*` |
| Bug fix | `fix/*` |
| Documentation | `docs/*` |
| Refactor | `refactor/*` |
| UI changes | `ui/*` |

Example: `docs/contributing-md`, `feat/search-filter`, `fix/cart-quantity-bug`

> Never commit directly to `main`.

---

## 4. PR Title Format

All PR titles must follow this format:

```
[ELUSoC'26] Brief description of the change
```

Example: `[ELUSoC'26] Add CONTRIBUTING.md`

---

## 5. PR Description Requirements

Your PR description must include:

- **Fixes #X** — link to the issue this PR closes
- **Summary** — what was changed and why
- **Screenshots** — required for any UI changes
- **Testing performed** — how you verified the change works

---

## 6. PR Checklist

Before submitting, confirm all of the following:

- [ ] I am assigned to the issue this PR addresses
- [ ] Branch follows the naming convention (e.g. `feat/*`, `fix/*`)
- [ ] Backend runs without errors — `python app.py`
- [ ] Frontend builds without errors — `npm run build` (inside `frontend/`)
- [ ] `data.json` is not corrupted or unintentionally modified

---

## 7. What Not To Do

- ❌ Do not open a PR without being assigned to an issue
- ❌ Do not bundle unrelated changes in a single PR
- ❌ Do not submit AI-generated spam — all contributions must be your own work

---

Issues and PRs are welcome. Please open an issue first to discuss any significant change.
