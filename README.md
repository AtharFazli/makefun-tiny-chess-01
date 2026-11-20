# tiny-chess-01

Chess engine in 4 KB of Python. Each trial it plays 8 games against the house
gauntlet through the make.fun env and scores its Elo.

## Run

`main.py` is the whole engine (Python 3.13, standard library only, no clock).

The make.fun harness sets `MAKEFUN_ENV_URL`; the engine plays
`POST /game`, `/move` and `/resign` routes itself and exits when the trial is
done. It uses iterative deepening alpha-beta with a transposition table,
move ordering (captures by MVV-LVA, history and killer heuristics), and
quiescence search.

## License

MIT (see LICENSE).
