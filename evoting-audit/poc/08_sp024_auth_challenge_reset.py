#!/usr/bin/env python3
"""
PoC: SP-024 — Authentication Challenge List Reset

The VerificationCardStateService reinitializes the authentication
challenge list when a time step gap is detected, discarding all
previously tracked challenges. This allows an attacker to reset
the authentication state by waiting.

Source: e-voting/voting-server/.../VerificationCardStateService.java:69-89
  Line 77: if (lastSuccessfulAuthenticationTimeStep + 1 < previousTimeStep)
  Line 79:   → reinitializes the challenge list (discards history)
"""
import json

def demonstrate():
    print("=" * 60)
    print("SP-024: Authentication Challenge List Reset PoC")
    print("=" * 60)
    print()
    print("Vulnerable logic (VerificationCardStateService.java:77):")
    print()
    print("  if (lastSuccessfulAuthenticationTimeStep + 1 < previousTimeStep) {")
    print("      // REINITIALIZE — discards all tracked challenges")
    print("      challenges = new SuccessfulAuthenticationAttempts(ImmutableList.of(challenge));")
    print("  } else {")
    print("      // ADD to existing list")
    print("      challenges = existingChallenges.addChallenge(challenge);")
    print("  }")
    print()

    steps = [
        {"time_step": 1, "action": "Auth attempt 1", "challenge_list": ["c1"], "note": "Normal"},
        {"time_step": 2, "action": "Auth attempt 2", "challenge_list": ["c1", "c2"], "note": "Normal"},
        {"time_step": 3, "action": "Auth attempt 3", "challenge_list": ["c1", "c2", "c3"], "note": "Normal"},
        {"time_step": 3, "action": "WAIT for time step gap", "challenge_list": ["c1", "c2", "c3"], "note": "Attacker waits..."},
        {"time_step": 10, "action": "Auth attempt 4 (after gap)", "challenge_list": ["c4"], "note": "LIST RESET! All history lost"},
        {"time_step": 11, "action": "Auth attempt 5", "challenge_list": ["c4", "c5"], "note": "Starts fresh"},
    ]

    print("Attack timeline:")
    print("-" * 60)
    for s in steps:
        status = "⚠ RESET" if "RESET" in s["note"] else "  OK   "
        print(f"  T={s['time_step']:2d} | {s['action']:<35s} | Challenges: {s['challenge_list']}")
        if "RESET" in s["note"]:
            print(f"        | → {s['note']}")
    print()
    print("Impact: Authentication replay protection is defeated.")
    print("An attacker can reuse previously-valid challenges after")
    print("the time step gap causes the list to be reinitialized.")

if __name__ == "__main__":
    demonstrate()
