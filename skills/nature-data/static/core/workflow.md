<!-- Modified in the context-engineered edition; see repository NOTICE. -->

# Workflow and output format

## Workflow

1. Identify the target journal and article type. If journal-specific instructions conflict with this skill, follow the journal.
2. Inventory every dataset needed to support the main and supplementary results: generated raw data, processed data, figure source data, secondary data, software outputs, models, tables, images, and files underlying statistical analysis.
3. Classify each dataset into one access route: `public repository`, `controlled access repository`, `within paper or supplement`, `reused public source`, `third-party restricted`, `available on justified request`, or `not applicable`.
4. Choose repository and identifier strategy before drafting text. Prefer DOI, accession number, Handle, ARK, or stable repository record over personal websites and temporary cloud links.
5. Draft the Data Availability statement using explicit dataset-to-location mapping.
6. Add formal dataset citations for public data that support conclusions.
7. Run the FAIR and metadata audit before finalizing.
8. Return ready-to-paste statement text plus any unresolved fields the author must confirm.

## External mutation gate

Default to a local staging package. Do not create a deposit, upload or publish
files, mint a DOI, or change licence, embargo, visibility, access, or metadata
until the user has confirmed:

- repository and account;
- exact files and hashes;
- public/private/controlled visibility and embargo;
- licence and authority to grant it;
- consent, ethics, third-party, and sensitive-data restrictions;
- metadata preview and DOI-mint timing;
- whether the action is reversible or versioned.

Do not upload raw sensitive data by default. Keep reviewer-only URLs/tokens out
of prose, logs, manifests, and screenshots.

## Output format

Unless the user asks for another format, return:

```text
Data Availability
[ready-to-paste statement]

Repository and citation actions
- [specific actions or "None"]

Missing information / risk flags
- [specific flags or "None"]

中文核对
- [用中文列出作者需要确认的字段或 "无"]
```

When auditing an existing statement, lead with blocking issues first, then provide a revised version.
