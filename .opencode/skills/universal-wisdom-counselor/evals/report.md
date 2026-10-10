# Eval Report — 20-prompt hallucination set (2026-10-10)

- Set: `.opencode/skills/universal-wisdom-counselor/evals/eval_set.json` (4 Gita, 4 Ramayana, 4 Dhammapada, 4 Bible, 4 Qur'an; 15 valid + 5 invalid).
- Validator: `scripts/validate.py` with full Quran 114, Bible 66 ch-max, Ramayana sarga-max tables.

## Results (after fix)

- Citation: TP=15 TN=5 FP=0 FN=0, accuracy 20/20 = 1.00, hallucination-pass 0.00, false-reject 0.00.
- Routing: 20/20 = 1.00 (expected tradition matches).
- Samples: 5/5 pass.

## Bug found + fixed

- Initial run: 19/20 (FP leak E07 `RAM_YUD_999_1` passed — sarga-max not enforced).
- Fix: added `RAM_SARGA_MAX` check in `validate.py:ramayana` branch. Re-run: 20/20.

## Residual gaps

- Bible verse-level max not bundled (only ch-max + spot ceilings); ±1 versification variance = flag not hard-fail.
- Qur'an school variance (Kufi vs Basran/Shami) documented in boundaries.md.
- Fallback behavior (uncertain -> episode summary, no fake numbers) is prompt-rule only, not auto-tested — spot-check in demo.
