# Zenodo archival status of the register assurance family

Complete as of 17 August 2026. Every repository in the family is now archived
on Zenodo with a citable DOI.

| Repository | Release | Version DOI | Concept DOI |
|---|---|---|---|
| investment-fund-ontology | v0.2.1 | 10.5281/zenodo.21970555 | 10.5281/zenodo.21970554 |
| insurance-register-ontology | v0.1.0 | 10.5281/zenodo.21970557 | 10.5281/zenodo.21970556 |
| bank-register-ontology | v0.2.1 | 10.5281/zenodo.21970544 | 10.5281/zenodo.21970543 |
| scholarly-record-ontology | v0.1.0 | 10.5281/zenodo.21983123 | 10.5281/zenodo.21983122 |
| learning-standards-ontology | v0.1.0 | 10.5281/zenodo.21983125 | 10.5281/zenodo.21983124 |
| enterprise-knowledge-ontology | v0.1.0 | 10.5281/zenodo.21983127 | 10.5281/zenodo.21983126 |
| uk-register-ontology | v0.1.0 | 10.5281/zenodo.21983129 | 10.5281/zenodo.21983128 |
| italy-register-ontology | v0.1.0 | 10.5281/zenodo.21983133 | 10.5281/zenodo.21983132 |
| securities-register-ontology | v0.1.0 | 10.5281/zenodo.21983171 | 10.5281/zenodo.21983170 |
| register-integrity-index | v0.1.0 | 10.5281/zenodo.21983151 | 10.5281/zenodo.21983150 |

Cite the concept DOI when referring to a repository in general, because it
always resolves to the newest version. Cite the version DOI when a claim
depends on the exact numbers in a given release, which is the normal case for
findings, since the underlying registers change daily.

## Operating notes for future releases

Connecting a Zenodo account to GitHub does not archive anything by itself.
Each repository carries its own switch at
https://zenodo.org/account/settings/github/ , newly created repositories only
appear there after pressing sync, and the switch does not reach backwards. A
release published before the switch was enabled stays unarchived until the
release is deleted and recreated against the same tag, which fires the webhook
again without disturbing the version number.

Zenodo reads `.zenodo.json` and ignores `CITATION.cff` whenever both files are
present. Both exist in every repository here, so both have to be updated
together on every release or the archived metadata will drift from the
citation file that humans read.

The Zenodo search index lags behind minting by several minutes, and it indexes
record titles rather than repository names. A repository that appears to be
missing straight after a release is usually already archived under its title.
