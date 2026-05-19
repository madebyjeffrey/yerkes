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
02:37:47 [INFO    ] yerkes.__main__: After turn, year=2501
02:37:47 [INFO    ] yerkes.__main__: NEWS [2501] Year 2501 begins
02:37:47 [INFO    ] yerkes.__main__: NEWS [2501] Population increased on Kaugon: 46451 -> 53337 (+6886)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2501] Population increased on Veilia: 35817 -> 41141 (+5324)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2501] Population increased on Aroolon: 42505 -> 48812 (+6307)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2501] Population increased on Faomar: 39160 -> 44976 (+5816)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2501] Population increased on Oroumus: 34047 -> 39110 (+5063)
02:37:47 [INFO    ] yerkes.game: News published [2502]: Year 2502 begins
02:37:47 [INFO    ] yerkes.game: Year advanced to 2502  [game=A quiet drift in the void]
02:37:47 [INFO    ] yerkes.__main__: After turn, year=2502
02:37:47 [INFO    ] yerkes.__main__: NEWS [2502] Year 2502 begins
02:37:47 [INFO    ] yerkes.__main__: NEWS [2502] Population increased on Kaugon: 53337 -> 61230 (+7893)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2502] Population increased on Veilia: 41141 -> 47248 (+6107)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2502] Population increased on Aroolon: 48812 -> 56044 (+7232)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2502] Population increased on Faomar: 44976 -> 51646 (+6670)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2502] Population increased on Oroumus: 39110 -> 44919 (+5809)
02:37:47 [INFO    ] yerkes.game: News published [2503]: Year 2503 begins
02:37:47 [INFO    ] yerkes.game: Year advanced to 2503  [game=A quiet drift in the void]
02:37:47 [INFO    ] yerkes.__main__: After turn, year=2503
02:37:47 [INFO    ] yerkes.__main__: NEWS [2503] Year 2503 begins
02:37:47 [INFO    ] yerkes.__main__: NEWS [2503] Population increased on Kaugon: 61230 -> 70273 (+9043)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2503] Population increased on Veilia: 47248 -> 54251 (+7003)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2503] Population increased on Aroolon: 56044 -> 64332 (+8288)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2503] Population increased on Faomar: 51646 -> 59292 (+7646)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2503] Population increased on Oroumus: 44919 -> 51581 (+6662)
02:37:47 [INFO    ] yerkes.game: News published [2504]: Year 2504 begins
02:37:47 [INFO    ] yerkes.game: Year advanced to 2504  [game=A quiet drift in the void]
02:37:47 [INFO    ] yerkes.__main__: After turn, year=2504
02:37:47 [INFO    ] yerkes.__main__: NEWS [2504] Year 2504 begins
02:37:47 [INFO    ] yerkes.__main__: NEWS [2504] Population increased on Kaugon: 70273 -> 80628 (+10355)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2504] Population increased on Veilia: 54251 -> 62278 (+8027)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2504] Population increased on Aroolon: 64332 -> 73826 (+9494)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2504] Population increased on Faomar: 59292 -> 68053 (+8761)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2504] Population increased on Oroumus: 51581 -> 59218 (+7637)
02:37:47 [INFO    ] yerkes.game: News published [2505]: Year 2505 begins
02:37:47 [INFO    ] yerkes.game: Year advanced to 2505  [game=A quiet drift in the void]
02:37:47 [INFO    ] yerkes.__main__: After turn, year=2505
02:37:47 [INFO    ] yerkes.__main__: NEWS [2505] Year 2505 begins
02:37:47 [INFO    ] yerkes.__main__: NEWS [2505] Population increased on Kaugon: 80628 -> 92478 (+11850)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2505] Population increased on Veilia: 62278 -> 71474 (+9196)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2505] Population increased on Aroolon: 73826 -> 84695 (+10869)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2505] Population increased on Faomar: 68053 -> 78087 (+10034)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2505] Population increased on Oroumus: 59218 -> 67969 (+8751)
02:37:47 [INFO    ] yerkes.game: News published [2506]: Year 2506 begins
02:37:47 [INFO    ] yerkes.game: Year advanced to 2506  [game=A quiet drift in the void]
02:37:47 [INFO    ] yerkes.__main__: After turn, year=2506
02:37:47 [INFO    ] yerkes.__main__: NEWS [2506] Year 2506 begins
02:37:47 [INFO    ] yerkes.__main__: NEWS [2506] Population increased on Kaugon: 92478 -> 106028 (+13550)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2506] Population increased on Veilia: 71474 -> 82003 (+10529)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2506] Population increased on Aroolon: 84695 -> 97130 (+12435)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2506] Population increased on Faomar: 78087 -> 89571 (+11484)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2506] Population increased on Oroumus: 67969 -> 77991 (+10022)
02:37:47 [INFO    ] yerkes.game: News published [2507]: Year 2507 begins
02:37:47 [INFO    ] yerkes.game: Year advanced to 2507  [game=A quiet drift in the void]
02:37:47 [INFO    ] yerkes.__main__: After turn, year=2507
02:37:47 [INFO    ] yerkes.__main__: NEWS [2507] Year 2507 begins
02:37:47 [INFO    ] yerkes.__main__: NEWS [2507] Population increased on Kaugon: 106028 -> 121510 (+15482)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2507] Population increased on Veilia: 82003 -> 94051 (+12048)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2507] Population increased on Aroolon: 97130 -> 111345 (+14215)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2507] Population increased on Faomar: 89571 -> 102705 (+13134)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2507] Population increased on Oroumus: 77991 -> 89461 (+11470)
02:37:47 [INFO    ] yerkes.game: News published [2508]: Year 2508 begins
02:37:47 [INFO    ] yerkes.game: Year advanced to 2508  [game=A quiet drift in the void]
02:37:47 [INFO    ] yerkes.__main__: After turn, year=2508
02:37:47 [INFO    ] yerkes.__main__: NEWS [2508] Year 2508 begins
02:37:47 [INFO    ] yerkes.__main__: NEWS [2508] Population increased on Kaugon: 121510 -> 139182 (+17672)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2508] Population increased on Veilia: 94051 -> 107826 (+13775)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2508] Population increased on Aroolon: 111345 -> 127581 (+16236)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2508] Population increased on Faomar: 102705 -> 117715 (+15010)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2508] Population increased on Oroumus: 89461 -> 102580 (+13119)
02:37:47 [INFO    ] yerkes.game: News published [2509]: Year 2509 begins
02:37:47 [INFO    ] yerkes.game: Year advanced to 2509  [game=A quiet drift in the void]
02:37:47 [INFO    ] yerkes.__main__: After turn, year=2509
02:37:47 [INFO    ] yerkes.__main__: NEWS [2509] Year 2509 begins
02:37:47 [INFO    ] yerkes.__main__: NEWS [2509] Population increased on Kaugon: 139182 -> 159332 (+20150)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2509] Population increased on Veilia: 107826 -> 123563 (+15737)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2509] Population increased on Aroolon: 127581 -> 146107 (+18526)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2509] Population increased on Faomar: 117715 -> 134852 (+17137)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2509] Population increased on Oroumus: 102580 -> 117572 (+14992)
02:37:47 [INFO    ] yerkes.game: News published [2510]: Year 2510 begins
02:37:47 [INFO    ] yerkes.game: Year advanced to 2510  [game=A quiet drift in the void]
02:37:47 [INFO    ] yerkes.__main__: After turn, year=2510
02:37:47 [INFO    ] yerkes.__main__: NEWS [2510] Year 2510 begins
02:37:47 [INFO    ] yerkes.__main__: NEWS [2510] Population increased on Kaugon: 159332 -> 182279 (+22947)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2510] Population increased on Veilia: 123563 -> 141524 (+17961)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2510] Population increased on Aroolon: 146107 -> 167222 (+21115)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2510] Population increased on Faomar: 134852 -> 154397 (+19545)
02:37:47 [INFO    ] yerkes.__main__: NEWS [2510] Population increased on Oroumus: 117572 -> 134689 (+17117)
```