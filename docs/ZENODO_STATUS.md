# Zenodo archival status of the register assurance family

Checked 17 August 2026. Zenodo mints a DOI for a GitHub repository only when
that repository is switched on individually at
https://zenodo.org/account/settings/github/ , and only for releases created
after the switch is enabled. Connecting the Zenodo account to GitHub is not
sufficient on its own.

| Repository | Release published | Zenodo webhook | DOI |
|---|---|---|---|
| bank-register-ontology | v0.2.1 | enabled | 10.5281/zenodo.21970544 (concept 21970543) |
| investment-fund-ontology | v0.2.1 | enabled | 10.5281/zenodo.21970555 (concept 21970554) |
| insurance-register-ontology | v0.1.0 | enabled | 10.5281/zenodo.21970557 (concept 21970556) |
| scholarly-record-ontology | v0.1.0 | not enabled | none |
| learning-standards-ontology | v0.1.0 | not enabled | none |
| enterprise-knowledge-ontology | v0.1.0 | not enabled | none |
| securities-register-ontology | v0.1.0 | not enabled | none |
| uk-register-ontology | v0.1.0 | not enabled | none |
| italy-register-ontology | v0.1.0 | not enabled | none |
| register-integrity-index | v0.1.0 | not enabled | none |

Every repository in the table carries both a `.zenodo.json` and a
`CITATION.cff`. Zenodo reads `.zenodo.json` and ignores `CITATION.cff`
whenever both are present, so the two files must be kept in step on every
release.

## What has to happen next

Seven repositories need their switch enabled at
https://zenodo.org/account/settings/github/ : scholarly-record-ontology,
learning-standards-ontology, enterprise-knowledge-ontology,
securities-register-ontology, uk-register-ontology, italy-register-ontology,
and register-integrity-index. The switch does not reach backwards, so the
v0.1.0 releases already published will stay unarchived. Once the switches are
on, deleting and recreating each release against the same tag fires the
webhook again and mints the DOI without disturbing the version numbers.

The DOIs matter beyond citation hygiene. Semantic Web Journal requires a
stable archived artifact URL before it will consider a descriptive paper, and
the cross-domain paper deposits its DOIs before the arXiv preprint so that the
preprint can cite them.
