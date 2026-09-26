# Independent evaluation preservation

The complete evaluation directory and its original ZIP were copied here without
rewriting any evaluation file. The evaluated Groundwork commit remains
`52e6d91eebdb0973bc18dfcdc0deb0b97f4a16e3`.

- [Independent report](2026-09-26-frozen-v1/REPORT.md)
- [Evaluation method](2026-09-26-frozen-v1/METHOD.md)
- [Original artifact checksums](2026-09-26-frozen-v1/ARTIFACTS.sha256)
- [Frozen-skill verification](2026-09-26-frozen-v1/freeze-verification.json)
- [Original ZIP](groundwork-frozen-v1-independent-evaluation-2026-09-26.zip)
- [Copy inventory and preservation checks](PRESERVATION.json)

Preservation verified all 3,547 source files byte for byte, all 3,545 original
artifact checksums, the sealed independent judgment, and all 3,546 ZIP entries
against the source directory. The ZIP SHA-256 is
`2a8fdc26779b3f857a2d6555a91c54e8d91886dfaba7914eeb76d0bf8397945a`.
The nine frozen skill hashes also matched their committed bytes.

The copy includes raw logs, prompts, generated artifacts, pristine fixtures,
intermediate states, helper results, supplemental checks, failures, and limitations.
No evaluation was rerun during preservation. Historical absolute paths remain as
recorded. The original source directory was left untouched.

`PRESERVATION.json` and this README are new preservation metadata, separate from
the unchanged evaluation directory and archive. Git does not store empty
directories; their inventory is recorded in `PRESERVATION.json` without inserting
marker files into the evaluation. Even the two original Python cache files are
retained to preserve the complete file set.
