# Verification report and writeback

<!-- New in this derivative; see ../../../NOTICE. -->

## Report schema

```text
entry_id
status
severity
field
original_value
suggested_value
source
accessed_at
version_or_conflict_note
confidence
```

Keep one row per field difference and a summary per entry. Include counts by
status, but do not let the aggregate hide unverifiable records.

## Authorized writeback

Write only after the user confirms the exact library/export, entry set, and
fields that may change. Create a timestamped backup or a sibling corrected
export before changing data. Apply only
evidence-backed fields, preserve citation keys unless requested, and emit a
machine-readable change log.

For Zotero, use an authenticated supported API or export/import route. Do not
edit `zotero.sqlite` directly. If only a read-only local endpoint is available,
produce a patch report instead of claiming that the library was updated.
