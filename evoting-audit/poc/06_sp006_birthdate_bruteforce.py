#!/usr/bin/env python3
"""
PoC: SP-006 — Year-of-Birth Authentication Brute Force

The voting system supports a "year of birth" authentication challenge
mode where voters prove identity by entering their birth year.

With ~100 realistic values (1924-2024), there is a ~1% chance per guess.
An attacker who obtains a voter's start voting key (SVK) or
voting card but lacks the challenge response can brute-force it.

The system limits confirmation attempts (SP-035 was verified to have
a 5-attempt MAX), but the START VOTING KEY authentication may not
share this limiter depending on configuration.

Source:
  ChallengeInformationExtensions.java — year-of-birth mode
  AuthenticationService — challenge validation
"""

import random
from datetime import datetime

CURRENT_YEAR = datetime.now().year
MIN_VOTER_AGE = 18
MAX_VOTER_AGE = 120

MIN_BIRTH_YEAR = CURRENT_YEAR - MAX_VOTER_AGE
MAX_BIRTH_YEAR = CURRENT_YEAR - MIN_VOTER_AGE

YEAR_RANGE = list(range(MIN_BIRTH_YEAR, MAX_BIRTH_YEAR + 1))

print("=" * 60)
print("SP-006: Year-of-Birth Challenge Brute Force Analysis")
print("=" * 60)
print()
print(f"Authentication mode: YEAR_OF_BIRTH")
print(f"Current year: {CURRENT_YEAR}")
print(f"Eligible voter birth years: {MIN_BIRTH_YEAR}-{MAX_BIRTH_YEAR}")
print(f"Total possible values: {len(YEAR_RANGE)}")
print()

prob_single = 1.0 / len(YEAR_RANGE)
print(f"Probability per guess: {prob_single:.4f} ({prob_single*100:.2f}%)")
print()

# Age distribution weighting (realistic voter demographics)
# Most voters are 25-75, with peak around 40-60
AGE_WEIGHTS = {}
for year in YEAR_RANGE:
    age = CURRENT_YEAR - year
    if 30 <= age <= 65:
        AGE_WEIGHTS[year] = 3.0  # most likely
    elif 18 <= age <= 29 or 66 <= age <= 80:
        AGE_WEIGHTS[year] = 1.5
    else:
        AGE_WEIGHTS[year] = 0.3

total_weight = sum(AGE_WEIGHTS.values())
for y in AGE_WEIGHTS:
    AGE_WEIGHTS[y] /= total_weight

print("--- Demographic-Weighted Attack ---")
print()
print("If attacker knows approximate age bracket:")
print()

brackets = {
    "Young (18-29)": range(CURRENT_YEAR - 29, CURRENT_YEAR - 17),
    "Middle (30-55)": range(CURRENT_YEAR - 55, CURRENT_YEAR - 29),
    "Senior (56-80)": range(CURRENT_YEAR - 80, CURRENT_YEAR - 55),
}

for name, year_range in brackets.items():
    count = len(list(year_range))
    p = 1.0 / count if count > 0 else 0
    print(f"  {name}: {count} values -> {p*100:.1f}% per guess")
    # Probability of success in N attempts
    for n in [1, 3, 5, 10]:
        p_success = 1.0 - (1.0 - p) ** n
        print(f"    {n} attempts: {p_success*100:.1f}% success")
    print()

print("--- Brute Force Simulation (1000 trials) ---")
print()

# Simulate brute-force attacks
TARGET_YEAR = 1975  # example target
successes_by_attempt = {1: 0, 3: 0, 5: 0, 10: 0, 20: 0}
TRIALS = 10000

for _ in range(TRIALS):
    # Attacker guesses in demographic-weighted order
    sorted_years = sorted(YEAR_RANGE,
                         key=lambda y: AGE_WEIGHTS.get(y, 0),
                         reverse=True)
    for attempt_num, guess in enumerate(sorted_years, 1):
        if guess == TARGET_YEAR:
            for threshold in successes_by_attempt:
                if attempt_num <= threshold:
                    successes_by_attempt[threshold] += 1
            break

print(f"Target birth year: {TARGET_YEAR}")
print(f"Trials: {TRIALS}")
print()
for attempts, successes in sorted(successes_by_attempt.items()):
    rate = successes / TRIALS * 100
    print(f"  Success within {attempts:2d} attempts: {rate:.1f}%")

print()
print("--- Attack Scenario ---")
print()
print("1. Attacker intercepts/steals voter's Start Voting Key (SVK)")
print("2. SVK alone is insufficient — needs challenge response")
print("3. Challenge mode = YEAR_OF_BIRTH")
print("4. Attacker knows voter is ~40-50 years old (public info)")
print("5. Only 10 possible years to try -> 10% per guess")
print("6. With 5 attempts: ~41% chance of casting fraudulent vote")
print()
print("Severity: HIGH — entropy of authentication challenge is")
print(f"          only {len(YEAR_RANGE)} values (~6.6 bits)")
print("          vs recommended minimum of 2^20+ for auth factors")
