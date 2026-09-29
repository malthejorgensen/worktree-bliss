worktree-bliss
==============

**The problem**  
You're developing your web application locally, probably using coding agents.
You spin up 4-6 worktrees, each one for a different feature or bugfix.

Now how do you easily try out the application in each of those worktrees?

**The solution**  
worktree-bliss

_Warning:_ For demonstration purposes this repo has committed the `.env` and
`.env.worktree` files. In a real repo, you shouldn't commit anything that
contains actual secrets, which `.env` may have. What you **can** do is commit
the symlinks in `backend/` and `frontend/`.
Do this while there are no `.env` and `.env.worktree` files at the root, to
ensure you're only committing the symlinks themselves.


What is `worktree-bliss`?
-------------------------
`worktree-bliss` is a template separating worktrees of local web applications running:

- a backend (e.g. Flask)
- a frontend (e.g. Vite with auto-reload)
- Postgres
- Redis

It gives each frontend and backend their own port, and for Postgres and Redis
it uses just a single Postgres and Redis instance and separates the
worktree data into separate Postgres and Redis databases (yes, Redis has
databases).

How does it work?
------------------

In `.env` you have your generic setup, where `DATABASE_URL` and `REDIS_URL` use
variables loaded from `.env.worktree`.

```
DATABASE_URL=postgres://localhost:5432/${WORKTREE_POSTGRES_DB}
REDIS_URL=redis://localhost:6379/${WORKTREE_REDIS_DB}
```

We then have the following symlinks:

```
backend/.env -> /.env
backend/.env.worktree -> /.env.worktree
frontend/.env -> /.env
frontend/.env.local -> /.env.worktree  # Vite loads `.env.local` automatically
```

We then pass multiple `--env-file` flags to `uv` which overlays the env-files
on top of each other while allowing variable interpolation as well.


The tools
---------

### uv
`uv` doesn't automatically load `.env` files, but can be passed one or more
`--env-file`-args which will overlay. The `.env`-files are overlaid from 
"left-to-right" -- a var in the first env file passed is overwritten by
ones written later.

### honcho
`honcho` automatically loads any `.env`-file present (with that exact name),
and allows an `--env`-arg with multiple files passed comma-separated and
overlaid.
It doesn't allow for variables.

### vite
Automatically loads `.env` and `.env.local` where variables in `.env.local`
override ones in `.env`. And it allows variables.

### npm
Doesn't have a built-in mechanism to load `.env`-files.

### node
`node` has the `--env-file`-arg but there's no overlay and variable interpolation,
and last file passed wins.

|           | `uv`         | `honcho`    | `vite`                       | `npm` | `node`       |
|-----------|--------------|-------------|------------------------------|-------|--------------|
| Automatic | No           | Yes, `.env` | Yes, `.env` and `.env.local` | No    | No           |
| CLI arg   | `--env-file` | `--env`     | No                           | No    | `--env-file` |
| Overlay   | Yes          | Yes         | Yes                          | No    | No           |
| Variables | Yes          | No          | Yes                          | No    | No           |
