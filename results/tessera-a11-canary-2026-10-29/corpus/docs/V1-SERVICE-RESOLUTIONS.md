# Tessera's resolutions of the service contract's Undecided items (V1)

> **Status: OWNER RESOLUTIONS, 2026-10-25** (Claude Opus 5.5), committed and OpenTimestamps-stamped **before any
> Phase 1a issuer code**, as promised to tupay (`docs/requests/2026-10-25-to-tupay-T1-acknowledgement.md`). It
> resolves the *Undecided* items of `docs/V1-SERVICE-CONTRACT.md` at `70c2cb7` for Tessera's own Phase 1a. It does not
> amend the contract handed to tupay. Rule applied throughout: V1 should work, with its limits stated; prefer the
> simplest promise that can be kept.
>
> **Residue, stated.** The owner lived through finding E-02 (a late-answered retry). S3 and S5 below are informed by
> it. Tupay's authors are not.
>
> Revised after a bounded Codex review (SR-01 to SR-06, all applied; `docs/reviews/service-resolutions/`).
>
> Items marked **AUTHOR** are promises the operator makes; the owner gives a recommendation only.

## Client side

| Item | Resolution | By |
|---|---|---|
| S1 forms, representation, size | One form: the request body is the content, as raw bytes. The receipt carries them as canonical base64 in `common.content`; decoding recovers exactly the submitted bytes, and those bytes are what is attested. Client limit: **1 MiB** of content; the complete encoded payload stays under the 16 MiB cap. A client with larger content submits a digest (S6). | Owner |
| S2 incomplete delivery | Every completed result carries the receipt's SHA-256. The client checks it, and can retrieve the result again as often as it likes while it is kept (S5). | Owner |
| S3 unknown outcome; terminal refusal | The client resolves an unknown outcome by status lookup, using its own request key (S5). **A refusal is final:** a refused request is never completed later. To try again, the client sends a new request. | Owner |
| S4 latency | **Stated, not guaranteed:** a receipt is usually complete within 3 hours of acceptance. A request not complete **24 hours** after acceptance ends as FAILED, with its reason. Start: the acceptance response. End: the status becoming COMPLETE. Window preparation happens before the window opens and does not count. Results are **retrieved by the client**, not pushed. | Owner |
| S5 request lifecycle | The client supplies a **request key** (a UUID). The same key returns the same request and the same receipt, every time. The same content under a different key is a separate request with its own receipt. States: ACCEPTED, COMPLETE, REFUSED, FAILED. Acceptance is durable once the ACCEPTED response is sent. Only the client credential that made a request may look it up or retrieve it. No cancellation in V1. Lookup and identical-result retrieval last **30 days** after the request ends (COMPLETE, REFUSED or FAILED). After that, lookup returns EXPIRED. A content-free record of the key is kept until issuance closes, so an expired key cannot start a new issuance. | Owner |
| S6 content exposure | Requests and results are readable only by the submitting client credential. Transport is encrypted. Refused content is not stored. Content and results are deleted 30 days after the request ends, copies included. Content is used for nothing but the request. A receipt the client hands to others exposes the content to them: that is the client's choice. | Owner |
| S7 cost | **AUTHOR.** Recommendation: V1 charges nothing (trial service). It states the measured cost per receipt (H3) as the cost figure A9.1 asks for. | Author |
| S8 availability | No target. Best effort, stated as such. | Owner |

## Adjudicator side

| Item | Resolution | By |
|---|---|---|
| AJ2 publication of authority records | **AUTHOR.** Recommendation: keep the DNS record and the git repository public for **10 years** after the window ends. That matches V1's 10-year design horizon (`docs/decisions/2026-10-19-horizon-cost.md`). | Author |
| AJ5 exit | **AUTHOR.** Recommendation: for a planned shutdown, 30 days' public notice, and archiving the authority records and git repository with an independent archive (for example Zenodo). A final verifier release only if release authorization is still trustworthy (profile §15.9 R5 stops new releases after a release-key compromise). For an unexpected shutdown: notice and archiving as far as practicable. | Author |
| AJ6 verification materials | Owner: acquisition instructions that identify a compatible signed release and a trust configuration covering the receipt's evidence, authenticated under profile §15.9. Supported environment: one stated platform per release (V1: Linux x86-64). **AUTHOR** (recommendation): releases stay downloadable for as long as AJ2's publication runs, with 12 months' notice before support ends. | Owner and Author |
| AJ7 capture notice | **AUTHOR.** Recommendation: promise to announce any known capture of the authority records or keys, within 7 days, through the channels that carry the release-key fingerprint. Detection is still not promised. | Author |

## Limits

| Item | Resolution | By |
|---|---|---|
| L1 window dates and closure | Both window endpoints are fixed and published before issuance preparation, at most 90 days apart. The actual dates stay OPEN until the dated operating record; a late first issuance does not extend the window. Signing stops 96 hours before the window ends (the runbook's operating margin, not a registered rule). Acceptance stops 120 hours before the end, so that every accepted request can complete or fail (S4) before signing stops. Only receipts that pass the registered window checks are shipped. Completed results stay retrievable for 30 days (S5). Closure is announced 14 days ahead on the service page. | Owner |
