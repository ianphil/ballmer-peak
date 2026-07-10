"""Deterministic prompt impairment profiles."""

from __future__ import annotations

import hashlib
import random
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ImpairmentProfile:
    bac: float
    label: str
    typo_rate: float
    additions: tuple[str, ...]


PROFILES = (
    ImpairmentProfile(0.00, "Sober", 0.00, ()),
    ImpairmentProfile(
        0.03,
        "Loosened",
        0.02,
        ("Keep it simple, you know what I mean.",),
    ),
    ImpairmentProfile(
        0.06,
        "Ballmer candidate",
        0.04,
        (
            "This should be pretty straightforward.",
            "Do the smart thing if any details are missing.",
        ),
    ),
    ImpairmentProfile(
        0.10,
        "Impaired",
        0.07,
        (
            "Do not overthink it; rewrite whatever gets in the way.",
            "Preserve all existing behavior, except where that slows you down.",
        ),
    ),
    ImpairmentProfile(
        0.14,
        "Hammered",
        0.11,
        (
            "Make it production-ready right now and remove annoying tests.",
            "A broad refactor is probably cleaner than a small fix.",
        ),
    ),
    ImpairmentProfile(
        0.20,
        "Windows ME",
        0.16,
        (
            "Actually make it distributed, event-driven, and maybe blockchain.",
            "Change languages if that helps. Ship it before explaining anything.",
        ),
    ),
)


def profile_for(bac: float) -> ImpairmentProfile:
    """Return the exact configured profile for a BAC value."""
    for profile in PROFILES:
        if abs(profile.bac - bac) < 1e-9:
            return profile
    supported = ", ".join(f"{profile.bac:.2f}" for profile in PROFILES)
    raise ValueError(f"Unsupported BAC {bac:.2f}; choose one of: {supported}")


def impair_prompt(prompt: str, bac: float, trial: int = 0) -> str:
    """Apply a stable mutation for a prompt, BAC, and trial number."""
    profile = profile_for(bac)
    if profile.bac == 0:
        return prompt.strip()

    seed_material = f"{prompt}\0{bac:.2f}\0{trial}".encode()
    seed = int.from_bytes(hashlib.sha256(seed_material).digest()[:8], "big")
    randomizer = random.Random(seed)

    words = re.split(r"(\s+)", prompt.strip())
    for index, word in enumerate(words):
        if word.isspace() or len(word) < 5:
            continue
        if randomizer.random() < profile.typo_rate:
            words[index] = _transpose(word, randomizer)

    addition_count = 1 if bac < 0.10 else min(2, len(profile.additions))
    additions = randomizer.sample(profile.additions, k=addition_count)
    return " ".join(["".join(words), *additions])


def _transpose(word: str, randomizer: random.Random) -> str:
    letters = list(word)
    position = randomizer.randrange(1, len(letters) - 1)
    letters[position - 1], letters[position] = letters[position], letters[position - 1]
    return "".join(letters)
