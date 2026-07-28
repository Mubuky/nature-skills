<!-- Modified in the context-engineered edition; see repository NOTICE. -->

# Journal scope

Strict scope uses exact normalized journal titles, not prefixes. A title that
starts with `Nature`, `Communications`, `npj`, `Science`, or `Trends` is not
automatically in the requested family.

The bundled allowlists are a discovery snapshot checked on 2026-07-28 against:

- Nature Portfolio's official research, reviews, progress, Communications,
  npj, and scientific-series pages;
- AAAS Science-family journal pages;
- Cell Press journal pages.

When journal identity affects a manuscript-facing result:

1. Resolve the publication identity and ISSN from the version being cited.
2. Compare the exact normalized title with the bundled allowlist.
3. If absent or ambiguous, return `journal_identity_unverified`.
4. Verify the current official portfolio page before adding a new title.

`Nature and Culture` and invented titles such as
`Nature Reviews Imaginary Systems` must fail closed. A Crossref venue string is
metadata evidence, not proof of current publisher portfolio membership.

`flagship` includes only `Nature`, `Science`, and `Cell`. Partner journals,
transferred titles, renamed journals, and predecessor/successor publications
require explicit version-aware verification.
