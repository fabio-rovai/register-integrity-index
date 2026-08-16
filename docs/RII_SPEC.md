# The Register Integrity Index

**Version 1.0. A measurement instrument for the identifier and record governance of public registers.**

## Why this exists

Every sector runs on registers. Banks are looked up in BankFind, insurers in the EIOPA register, funds in the SEC series/class register, retractions in Crossref and Retraction Watch, curriculum standards in the Common Standards Project, government guidance in the GOV.UK Content API. Each register assures its own records to some standard. Almost none of them assures the identifiers it embeds from other registers, and no published instrument measures the difference.

The Register Integrity Index is that instrument. It is a set of five measurements that can be computed from a register's own published data plus the registers it points into, with no cooperation from the register operator. It generalises the Corpus Readiness Index (CRI), the measurement instrument built for organisational knowledge corpora in the [enterprise-knowledge-ontology](https://github.com/fabio-rovai/enterprise-knowledge-ontology) repository, from documents to registers.

## The thesis the instrument encodes

**Assurance stops at the register boundary.**

A register that validates its own records to a high standard will still publish, unchecked, the identifiers it borrows from other schemes. The FDIC validates its certificate numbers and publishes every one of its 2,252 LEI values truncated below the length the LEI standard requires. EIOPA maintains registration end dates rigorously and carries four LEI values that cannot exist in the global LEI system, including a letter O typed where a zero belongs. GOV.UK's curated search index excludes every withdrawn page while the sitemap and Content API keep serving them in full. The pattern is the same in every vertical measured so far: the checks a register runs on its own keys are never extended to the foreign keys it republishes, and nothing in the publishing pipeline notices.

The index therefore measures boundary assurance. It asks, of each register, how well governed the whole published record is, including the parts the register merely carries.

## The five dimensions

Each dimension yields a score from 0 to 100. Higher is better. Each dimension score is the unweighted arithmetic mean of one or more measured components, and every component must carry its raw recorded metric, its source artifact, and the mapping formula from that metric to the score. **The counts matter more than the score.** A single number is useful for ranking and useless for deciding what to fix.

### D1: Scheme conformance

*Do the identifiers the register publishes conform to the rules their scheme declares?*

This covers the register's own identifiers and, critically, the embedded foreign ones. A published LEI must be 20 characters of the permitted alphabet with valid ISO 7064 check digits regardless of who republishes it. A value in a closed enumeration must be one of the enumerated values. A record typed into a category must belong to that category, so a retraction notice recorded as retracted research is a conformance failure even though the string parses.

The typical mapping is 100 times one minus the defect rate over the checked population. Where a register scores a validated zero-defect result at full scale, that is a positive finding and is scored 100 with the null result stated, not treated as untested.

### D2: Resolution

*Do the published identifiers dereference or resolve to the thing they name?*

An identifier that promises dereferenceability and returns 404 has failed regardless of how well formed it is. An identifier that resolves to more than one candidate, or to a different entity than the record describes, has also failed, though wrong-entity resolution is scored under D3 where it is confirmed against a second register. The mapping is the resolution rate over a censused or sampled population, with censuses preferred and samples labelled.

### D3: Cross-register agreement

*Where two registers assert the same fact, do they agree?*

Agreement is measured over the population where both registers actually assert, typically as intersection over union or as one minus the disagreement rate. Silence is not disagreement and is scored under D4 as a coverage gap. Some agreement measures are symmetric and appear on both registers' rows with the same value; that is stated in the provenance rather than hidden.

### D4: Coverage

*What fraction of records carry the identifiers and status fields the register's purpose implies?*

A bank register implies an entity identifier per bank. A retraction register implies a DOI per retraction. A standards register implies a licence and an in-force status per standard set. A data dictionary implies a definition per term. Coverage failures are not errors in individual records; they are governance decisions waiting to happen, and they are scored on the fraction of the population covered.

### D5: Governance metadata

*Does the register publish the metadata that lets a consumer trust it: ownership, freshness, licence, review and withdrawal signalling?*

D5 is scored as a checklist over recorded signals only. Each signal recorded in the source artifacts is classed as a pass or a fail, and the score is 100 times passes over passes plus fails. Signals that were never measured are omitted from both numerator and denominator rather than counted against the register, because an unmeasured signal is not evidence of absence.

## Scoring

**Per dimension.** The dimension score is the unweighted arithmetic mean of its component scores, rounded to one decimal place.

**Composite.** The headline RII is the **geometric mean of the measured dimension scores**, rounded to one decimal place. The geometric mean is deliberate. An arithmetic mean lets a strong dimension conceal a fatal one, and a register is only as trustworthy as its worst governed dimension. A register whose every published LEI is invalid as published is not 64% trustworthy because its other dimensions average 80.

**Flooring.** For the composite only, any dimension score below 1.0 is floored at 1.0 before the geometric mean is taken. A true zero would force every composite containing it to exactly 0 and destroy the ordering among badly failing registers, which is the one region of the table where ordering carries the most information. A floored dimension is a fatal finding and the league table shows its true value.

**N/A is first class and is not zero.** A dimension is scored only where the source repositories recorded a finding that measures it. An unmeasured dimension is excluded from the geometric mean entirely, and every composite is published alongside its **coverage fraction**, the number of dimensions measured out of five. A register at 79.6 on three dimensions and a register at 78.0 on four are not directly comparable, and the table says so. No register is published with fewer than three measured dimensions.

**Fairness.** The index is a measurement, not a hit list. Null results are scored positively and stated as such: GLEIF's mapping file is checksum-clean across all 9,119,948 pairs and scores 100 on D1 for it; OpenAlex almost never fails to flag a retracted paper it actually holds and scores 99.9 on that component for it. Where a register's worst number has an innocent structural explanation, the explanation is carried in the provenance text.

## Provenance requirements

Every scored cell in `data/rii_v1.csv` carries five things: the source repository, the artifact file the number was recorded in, the raw recorded metric in words, the mapping formula from the metric to the 0 to 100 score, and the score. The validation script `scripts/validate.py` recomputes every dimension mean and every geometric mean from the CSV and compares them against the README league table, exiting non-zero on any mismatch. A number that cannot be traced from README to CSV to a named artifact in a source repository does not belong in the index.

## Inputs and the no-reharvest rule

Version 1 is computed **only** from findings already recorded in six shipped ontology repositories, all built between 14 and 16 August 2026:

| Repository | Registers measured through it |
|---|---|
| [investment-fund-ontology](https://github.com/fabio-rovai/investment-fund-ontology) | SEC series/class + N-CEN, GLEIF ISIN-LEI mapping |
| [insurance-register-ontology](https://github.com/fabio-rovai/insurance-register-ontology) | EIOPA register, BaFin register, GLEIF API |
| [scholarly-record-ontology](https://github.com/fabio-rovai/scholarly-record-ontology) | Crossref, Retraction Watch, OpenAlex, Europe PMC |
| [bank-register-ontology](https://github.com/fabio-rovai/bank-register-ontology) | FDIC BankFind, GLEIF golden copy, Federal Reserve MDRM |
| [learning-standards-ontology](https://github.com/fabio-rovai/learning-standards-ontology) | ASN, Common Standards Project, CEDS Ontology |
| [enterprise-knowledge-ontology](https://github.com/fabio-rovai/enterprise-knowledge-ontology) | GOV.UK Content API and Search (and the CRI design this index generalises) |

No external source was re-harvested for this index. That is a feature, not a shortcut: every number here was produced by a reproducible pipeline in one of those repositories, with its own build report and caveats, and this index adds a comparison layer, not new measurement error.

## Point in time

All metrics are as recorded on 14 to 16 August 2026 and will drift. Several of the underlying sources are fetched as current rather than pinned, and the source repositories say so explicitly. The index is versioned; a v2 recomputed from fresh builds is a different set of numbers, not a correction to these.

## Applying it to another register

The instrument needs, per register: one or more conformance censuses over published identifier values (D1), a dereference census or labelled sample (D2), at least one two-register comparison over a shared assertion (D3), coverage counts for the purpose-implied fields (D4), and a recorded pass/fail sweep of the governance signals (D5). The hard part is never the arithmetic. It is that most registers publish no field for the things D5 asks about, which is the same finding the CRI made about content estates, one layer down.
