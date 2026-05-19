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

