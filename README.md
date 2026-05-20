# Yerkes Data Module

This project includes a `data` module for validated game data structures and a `planet_names` module for unbounded planet-name generation.

## What is included

- `Planet` with validation for name and population (`0..1_000_000`)
- `Starmap` with validation for capacity and planet list contents
- `Game` that owns the game name and a generated `Starmap` (see `game` module)
- `Game.generate(number_of_planets, game_name=None, min_distance=None, map_size=None, seed=None)` to build a random game
- `Game.news` accumulator for turn events, with `publish_news(...)` and `consume_news()`
- `news` module with typed news classes (`NewsItem`, `PopulationChangeNews`) and accumulator
- News objects implement `__str__` for friendly automatic string conversion
- `Game.advance_turn()` runs turn generation phases including yearly population updates
- `planet_names.generate_planet_name(index)` for deterministic, pronounceability-filtered name generation
- `planet_names.iter_planet_names(start_index=0)` for infinite unique name generation

## Game generation

- Provide `game_name` to set a title directly.
- Omit `game_name` to auto-generate a title in the style of "A walk in the park".
- Use optional `map_size` to control map bounds and overall density.
- Use optional `min_distance` to control how close planets may be.
- Defaults are tuned for a denser map than before while still spacing planets apart.
- Generated starting planet populations are seeded below `50,000`.

## Quick run

```bash
python3 main.py
```

## Run tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## Example output:
```
% python3 /Users/jdrake/PycharmProjects/yerkes/main.py                                     
02:37:47 [INFO    ] yerkes.game: Generating game 'A quiet drift in the void': 5 planets, map_size=24.6, min_distance=4.23
02:37:47 [INFO    ] yerkes.game: Game 'A quiet drift in the void' ready — 5 planets placed.
02:37:47 [INFO    ] yerkes.__main__: Game: A quiet drift in the void  (Year 2500)
02:37:47 [INFO    ] yerkes.__main__: Planets (5):
02:37:47 [INFO    ] yerkes.__main__:   - Kaugon  population=46451  x=23  y=0
02:37:47 [INFO    ] yerkes.__main__:   - Veilia  population=35817  x=15  y=10
02:37:47 [INFO    ] yerkes.__main__:   - Aroolon  population=42505  x=6  y=11
02:37:47 [INFO    ] yerkes.__main__:   - Faomar  population=39160  x=24  y=15
02:37:47 [INFO    ] yerkes.__main__:   - Oroumus  population=34047  x=0  y=8
02:37:47 [INFO    ] yerkes.game: News published [2501]: Year 2501 begins
02:37:47 [INFO    ] yerkes.game: Year advanced to 2501  [game=A quiet drift in the void]
# Yerkes

Turn-based space game sandbox with validated data models, deterministic name generation, typed news events, and both CLI + pygame demo paths.

## Modules

- `data.py`: `Planet`, `Starmap`, population model/validation
- `game.py`: `Game`, random game generation, turn advancement phases
- `news.py`: `NewsItem`, `PopulationChangeNews`, `NewsAccumulator`
- `planet_names.py`: deterministic, pronounceable, effectively unbounded planet names
- `log.py`: opt-in logging configuration under the `yerkes.*` logger tree
- `main.py`: CLI demo (generates a game and advances 10 turns)
- `pygame_ui.py`: GUI demo (click planets to inspect population/location)

## Requirements

- Python `>=3.14` (per `pyproject.toml`)
- `uv` installed: <https://docs.astral.sh/uv/>

## Setup with uv

Create/sync the project environment:

```bash
uv sync
```

If you want GUI support, include optional GUI dependencies:

```bash
uv sync --extra gui
```

## Run the CLI demo

```bash
uv run python main.py
```

## Run the pygame GUI

Install GUI extras first (one time):

```bash
uv sync --extra gui
```

Then launch:

```bash
uv run python pygame_ui.py
```

GUI controls:

- `SPACE`: advance one turn/year
- Left click a planet: show selected planet population and coordinates

## Run tests

```bash
uv run python -m unittest discover -s tests -p "test_*.py"
```

## Notes

- Logging is disabled by default until `configure_logging(...)` is called.
- `Game.generate(...)` accepts optional `map_size`, `min_distance`, and `seed`.
- Generated starting planet populations are below `50,000`.
