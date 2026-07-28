# Authorized access and user handoff

<!-- Modified from Yuan1z0825/nature-skills; see ../../../NOTICE. -->

Load this file only for institutional, CNKI, or browser-authenticated access.

## Authorization boundary

- Use the user's lawful open-access, publisher entitlement, or institutional
  access only for the confirmed paper list.
- Reuse an already authorized browser context without inspecting cookies,
  passwords, local storage, session files, or the browser profile.
- A new or blank browser profile is evidence about that profile, not evidence
  that the user or institution lacks access.
- Do not automate or bypass CAPTCHA, slider, robot, Turnstile, reCAPTCHA, OTP,
  QR, passkey, hardware-key, or two-factor challenges.
- It is acceptable to click an ordinary, unambiguous `Continue` or institutional
  selection once when the user has authorized the route and no secret or
  security warning is involved.

## Handoff

When authentication or a security challenge appears:

1. Keep the exact tab and current route open.
2. State which site and stage require user interaction without exposing page
   secrets.
3. Ask the user to finish the step in the browser.
4. Resume once from the same tab after confirmation.
5. If the same challenge recurs, record a typed handoff/failure and stop retrying.

Never ask the user to paste institutional credentials, OTPs, recovery codes,
cookies, or session tokens into chat or a command. If such a secret is supplied,
do not repeat or store it.

## Publisher API keys

Prefer the hidden-input path in `scripts/configure_credentials.py`. If the user
has already supplied a publisher API key and explicitly wants it configured,
pipe the exact value through the script's secret-input mode. Keep it out of
arguments, logs, replies, manifests, and shell history. Report only the provider,
masked confirmation, and validation outcome.

An API key does not imply full-text entitlement. Record `api_not_entitled` or
`api_fulltext_unavailable` and continue only through lawful fallback routes.

## Institutional outcomes

Use a status defined by `scripts/lib/status-codes.mjs`. Distinguish:

- user authentication still required;
- session or resolver failure;
- institution has no entitlement;
- readable HTML exists but no authorized PDF exists;
- browser or publisher verification blocks the route;
- retry is safe after user handoff;
- repeated challenge or security warning means no automatic retry.

Never recast lack of entitlement as a transient network error.
