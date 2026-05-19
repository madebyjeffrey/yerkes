import logging
from math import gcd
from typing import Iterator, List, Tuple

from log import get_logger

_logger = get_logger(__name__)


_ONSETS = (
    "al",
    "an",
    "ar",
    "ba",
    "be",
    "ca",
    "da",
    "el",
    "fa",
    "ga",
    "ha",
    "io",
    "ka",
    "la",
    "ma",
    "na",
    "or",
    "ra",
    "ta",
    "ve",
)

_NUCLEI = (
    "a",
    "ae",
    "ai",
    "e",
    "ei",
    "i",
    "ia",
    "io",
    "o",
    "oi",
    "oo",
    "ou",
    "u",
    "ua",
    "ue",
)

_CODAS = (
    "dor",
    "dra",
    "gon",
    "lia",
    "lon",
    "mar",
    "mus",
    "nar",
    "nus",
    "phos",
    "ria",
    "ron",
    "rus",
    "th",
    "tor",
)

_BASE_SYMBOLS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_VOWELS = frozenset("aeiou")
_DISALLOWED_FRAGMENTS = (
    "eii",
    "iio",
    "ioo",
    "oou",
    "ouu",
    "uua",
)


def _has_three_consecutive_vowels(value: str) -> bool:
    streak = 0
    for char in value:
        if char in _VOWELS:
            streak += 1
            if streak >= 3:
                return True
        else:
            streak = 0
    return False


def _is_pronounceable(core: str) -> bool:
    if _has_three_consecutive_vowels(core):
        return False
    if core.startswith("io"):
        return False
    return not any(fragment in core for fragment in _DISALLOWED_FRAGMENTS)


_VALID_CORES: Tuple[Tuple[str, str, str], ...] = tuple(
    (onset, nucleus, coda)
    for onset in _ONSETS
    for nucleus in _NUCLEI
    for coda in _CODAS
    if _is_pronounceable(f"{onset}{nucleus}{coda}")
)

_NAME_COMBINATIONS = len(_VALID_CORES)
_PREFERRED_MULTIPLIER = 2_821
_CORE_OFFSET = 1_487 % _NAME_COMBINATIONS


def _pick_coprime_multiplier(preferred: int, modulus: int) -> int:
    candidate = preferred % modulus
    if candidate == 0:
        candidate = 1
    while gcd(candidate, modulus) != 1:
        candidate = (candidate + 1) % modulus
        if candidate == 0:
            candidate = 1
    return candidate


_CORE_MULTIPLIER = _pick_coprime_multiplier(_PREFERRED_MULTIPLIER, _NAME_COMBINATIONS)


def _to_base36(value: int) -> str:
    if value < 0:
        raise ValueError("Base-36 encoding only supports non-negative integers.")
    if value == 0:
        return "0"

    result: List[str] = []
    while value > 0:
        value, remainder = divmod(value, 36)
        result.append(_BASE_SYMBOLS[remainder])
    return "".join(reversed(result))


def generate_planet_name(index: int) -> str:
    """Generate a deterministic planet name for a given index.

    The base syllable space creates thousands of names. If the index exceeds
    that space, a base-36 suffix is appended so the naming space is unbounded.
    """
    if index < 0:
        raise ValueError("Planet name index must be at least 0.")

    # Jump around the syllable space so neighboring indices sound less alike.
    core_index = ((index * _CORE_MULTIPLIER) + _CORE_OFFSET) % _NAME_COMBINATIONS
    suffix_index = index // _NAME_COMBINATIONS

    onset, nucleus, coda = _VALID_CORES[core_index]

    name = f"{onset}{nucleus}{coda}".capitalize()
    if suffix_index == 0:
        result = name
    else:
        result = f"{name}-{_to_base36(suffix_index)}"
    _logger.debug("Generated planet name [index=%d]: %s", index, result)
    return result


def iter_planet_names(start_index: int = 0) -> Iterator[str]:
    """Yield unique planet names forever, starting at the given index."""
    if start_index < 0:
        raise ValueError("start_index must be at least 0.")

    index = start_index
    while True:
        yield generate_planet_name(index)
        index += 1

