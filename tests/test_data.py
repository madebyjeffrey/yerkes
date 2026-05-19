import unittest
import math

from data import (
    MAX_PLANET_POPULATION,
    Planet,
    Starmap,
)
from game import Game, STARTING_YEAR
from news import NewsItem, PopulationChangeNews
from planet_names import generate_planet_name, iter_planet_names


class DataTests(unittest.TestCase):
    _DISALLOWED_FRAGMENTS = ("eii", "iio", "ioo", "oou", "ouu", "uua")

    def test_planet_population_validation(self) -> None:
        with self.assertRaises(ValueError):
            Planet(name="TooMany", population=MAX_PLANET_POPULATION + 1, x=0, y=0)

    def test_generate_planet_name_rejects_negative_index(self) -> None:
        with self.assertRaises(ValueError):
            generate_planet_name(-1)

    def test_planet_name_generation_is_unique_for_first_500(self) -> None:
        names = [generate_planet_name(i) for i in range(500)]
        self.assertEqual(len(names), len(set(names)))

    def test_early_planet_names_are_spread_out(self) -> None:
        names = [generate_planet_name(i) for i in range(12)]
        prefixes = {name[:2] for name in names}
        self.assertGreaterEqual(len(prefixes), 6)

    def test_planet_names_avoid_triple_vowels(self) -> None:
        vowels = set("aeiou")
        names = [generate_planet_name(i).split("-", 1)[0].lower() for i in range(2_000)]
        for name in names:
            max_streak = 0
            streak = 0
            for char in name:
                if char in vowels:
                    streak += 1
                    max_streak = max(max_streak, streak)
                else:
                    streak = 0
            self.assertLessEqual(max_streak, 2)

    def test_planet_names_avoid_awkward_fragments(self) -> None:
        names = [generate_planet_name(i).split("-", 1)[0].lower() for i in range(2_000)]
        for name in names:
            self.assertFalse(name.startswith("io"))
            for fragment in self._DISALLOWED_FRAGMENTS:
                self.assertNotIn(fragment, name)

    def test_iter_planet_names_can_start_late(self) -> None:
        generator = iter_planet_names(start_index=4_500)
        first = next(generator)
        second = next(generator)
        self.assertNotEqual(first, second)

    def test_starmap_maximum_size_enforced(self) -> None:
        starmap = Starmap(maximum_size=1)
        starmap.add_planet(Planet(name="One", population=1, x=0, y=0))
        with self.assertRaises(ValueError):
            starmap.add_planet(Planet(name="Two", population=1, x=1, y=1))

    def test_game_generate_uses_provided_name(self) -> None:
        game = Game.generate(number_of_planets=5, game_name="A walk in the park", seed=1)
        self.assertEqual(game.name, "A walk in the park")
        self.assertEqual(len(game.starmap.planets), 5)

    def test_game_generate_initial_populations_are_under_50000(self) -> None:
        game = Game.generate(number_of_planets=30, seed=7)
        for planet in game.starmap.planets:
            self.assertLess(planet.population, 50_000)

    def test_game_generate_creates_default_name_when_missing(self) -> None:
        game = Game.generate(number_of_planets=3, seed=2)
        self.assertTrue(game.name.startswith("A "))
        self.assertIn(" in the ", game.name)

    def test_game_generate_planets_not_too_close(self) -> None:
        game = Game.generate(number_of_planets=20, seed=3)
        planets = game.starmap.planets
        minimum = min(
            math.hypot(a.x - b.x, a.y - b.y)
            for i, a in enumerate(planets)
            for b in planets[i + 1 :]
        )
        self.assertGreaterEqual(minimum, 3.0)

    def test_game_generate_honors_optional_map_size(self) -> None:
        game = Game.generate(number_of_planets=8, map_size=15.0, seed=4)
        for planet in game.starmap.planets:
            self.assertGreaterEqual(planet.x, 0)
            self.assertGreaterEqual(planet.y, 0)
            self.assertLessEqual(planet.x, 15)
            self.assertLessEqual(planet.y, 15)
            self.assertIsInstance(planet.x, int)
            self.assertIsInstance(planet.y, int)

    def test_game_generate_honors_optional_min_distance(self) -> None:
        game = Game.generate(number_of_planets=10, map_size=30.0, min_distance=5.0, seed=9)
        planets = game.starmap.planets
        minimum = min(
            math.hypot(a.x - b.x, a.y - b.y)
            for i, a in enumerate(planets)
            for b in planets[i + 1 :]
        )
        self.assertGreaterEqual(minimum, 4.0)

    def test_game_starts_at_year_2500(self) -> None:
        game = Game.generate(number_of_planets=3, seed=1)
        self.assertEqual(game.year, STARTING_YEAR)
        self.assertEqual(game.year, 2500)

    def test_game_advance_year_increments(self) -> None:
        game = Game.generate(number_of_planets=3, seed=1)
        game.advance_year()
        self.assertEqual(game.year, 2501)
        game.advance_year()
        self.assertEqual(game.year, 2502)

    def test_advance_turn_ten_times_advances_ten_years(self) -> None:
        game = Game.generate(number_of_planets=3, seed=1)
        for _ in range(10):
            game.advance_turn()
            game.consume_news()
        self.assertEqual(game.year, STARTING_YEAR + 10)

    def test_advance_turn_runs_population_phase(self) -> None:
        planet = Planet(name="Terra", population=100, x=0, y=0)
        game = Game(name="Test", starmap=Starmap(maximum_size=1, planets=[planet]))
        game.advance_turn()
        self.assertEqual(game.year, 2501)
        self.assertGreater(planet.population, 100)

    def test_advance_turn_generates_population_news(self) -> None:
        planet = Planet(name="Terra", population=100, x=0, y=0)
        game = Game(name="Test", starmap=Starmap(maximum_size=1, planets=[planet]))
        game.advance_turn()
        items = game.news.peek()
        self.assertGreaterEqual(len(items), 2)
        population_items = [item for item in items if isinstance(item, PopulationChangeNews)]
        self.assertEqual(len(population_items), 1)
        self.assertEqual(population_items[0].planet_name, "Terra")

    def test_game_starts_with_empty_news(self) -> None:
        game = Game.generate(number_of_planets=3, seed=1)
        self.assertEqual(game.news.peek(), [])

    def test_advance_year_publishes_news(self) -> None:
        game = Game.generate(number_of_planets=3, seed=1)
        game.advance_year()
        items = game.news.peek()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].year, 2501)
        self.assertIn("begins", items[0].headline)

    def test_consume_news_clears_accumulator(self) -> None:
        game = Game.generate(number_of_planets=3, seed=1)
        game.publish_news("Test bulletin", "Something happened")
        consumed = game.consume_news()
        self.assertEqual(len(consumed), 1)
        self.assertEqual(consumed[0].headline, "Test bulletin")
        self.assertEqual(game.news.peek(), [])

    def test_population_change_news_is_typed(self) -> None:
        game = Game.generate(number_of_planets=3, seed=1)
        item = game.publish_population_change(
            planet_name="Kaugon",
            previous_population=100,
            new_population=130,
        )
        self.assertIsInstance(item, PopulationChangeNews)
        self.assertEqual(item.delta, 30)
        self.assertIn("Population increased", item.headline)

    def test_population_change_news_round_trips_through_accumulator(self) -> None:
        game = Game.generate(number_of_planets=3, seed=1)
        game.publish_population_change(
            planet_name="Veilia",
            previous_population=250,
            new_population=200,
        )
        consumed = game.consume_news()
        self.assertEqual(len(consumed), 1)
        self.assertIsInstance(consumed[0], PopulationChangeNews)
        self.assertEqual(consumed[0].details, "250 -> 200 (-50)")

    def test_news_item_string_conversion(self) -> None:
        item = NewsItem(year=2501, headline="Scout report", details="Signals detected")
        self.assertEqual(str(item), "[2501] Scout report - Signals detected")

    def test_population_change_news_string_conversion(self) -> None:
        item = PopulationChangeNews.create(
            year=2502,
            planet_name="Kaugon",
            previous_population=100,
            new_population=150,
        )
        self.assertEqual(
            str(item),
            "[2502] Population increased on Kaugon: 100 -> 150 (+50)",
        )

    def test_game_generate_rejects_invalid_planet_count(self) -> None:
        with self.assertRaises(ValueError):
            Game.generate(number_of_planets=0)

    def test_game_generate_rejects_invalid_map_size(self) -> None:
        with self.assertRaises(ValueError):
            Game.generate(number_of_planets=2, map_size=0.0)

    def test_game_generate_rejects_invalid_min_distance(self) -> None:
        with self.assertRaises(ValueError):
            Game.generate(number_of_planets=2, min_distance=-1.0)


if __name__ == "__main__":
    unittest.main()

