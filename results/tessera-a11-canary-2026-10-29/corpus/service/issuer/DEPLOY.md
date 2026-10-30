# Deploying the V1 issuer and its signers (owner, 2026-10-27)

> **Status: OWNER DRAFT, revised after the signer review** (`docs/reviews/signers/CODEX-REVIEW.md`, SG-01 to SG-05).
> These are the steps for the first deployment. No agent runs any of them: `terraform apply` and every AWS write
> run in the author's login session, from commands written out here in full. GCP steps can run on the NUC, where
> `gcloud` is logged in.

## Before the session (owner, no credentials)

1. `service/verifier/install.sh` has been run, so the pinned SHA-1DC binary exists.
2. All suites are green: issuer, `service/signer-kms`, `service/signer-gcp` (`.venv/bin/python -m pytest -q` in each).
3. Packages, each built deterministically (record each SHA-256):
   - `cd service/issuer && .venv/bin/python package.py dist/issuer-bootstrap.zip`
   - `cd service/signer-kms && .venv/bin/python package.py dist/signer-kms.zip`

## Keys and what counts as production — OWNER DECISION, revised 2026-10-28

**V1 uses new production keys, not the spike keys.** The hybrid registration commits to deleting both spike keys
(`formal/p8/HYBRID-SUPPLEMENT.md` §11 item 6, lines 524-526): "Both spike keys are deleted after the re-capture
verifies, once the review clears." The first version of this section reused them. That contradicted the
commitment, and Codex found it (`docs/reviews/amendment-11/CODEX-REVIEW.md`, A11-03). In the session:

- **KMS:** `aws kms create-key --key-spec ML_DSA_65 --key-usage SIGN_VERIFY`. Its id and fingerprint are
  `kms_key_id` and `key_fp` in step 5.
- **Slot 2:** a new HSM key in keyring `tessera-v1` (`gcloud kms keys create ... --protection-level=hsm
  --default-algorithm=ec-sign-p256-sha256 --purpose=asymmetric-signing`). Its version, `createTime` and fingerprint
  are exported as `SLOT2_KEY`, `SLOT2_KEY_VERSION`, `SLOT2_KEY_CREATED` and `SLOT2_KEY_FP` for
  `service/signer-gcp/deploy.sh`, which has no key defaults (the version number defaults to 1) and refuses the spike key.
- Both keys are recorded in the external custody record before either signs (profile §8).
- The spike keys are deleted (KMS: schedule deletion; GCP: destroy the key version) once the conditions in the
  supplement hold.

**Nothing separates TEST from production at signing time** (signer review, Q3). From the moment a window's
authority records name the new keys, every receipt they sign is a production receipt. The smoke test below
produces a real receipt over honest smoke-test content.

## In the session (author logged in: `aws login --profile tessera`)

1. **Issuer, bootstrap.** `terraform -chdir=infra plan -var lambda_zip=../dist/issuer-bootstrap.zip -out tfplan`.
   Read the plan together, then `terraform -chdir=infra apply tfplan`. The bootstrap package has no `install.json`,
   so pre-ship refuses and no receipt can ship from it.
2. **Install facts on Lambda.**
   `aws lambda invoke --profile tessera --function-name <poller> --payload '{"tessera":"install-facts"}' --cli-binary-format raw-in-base64-out install-facts.json`
3. **Runtime version.** `aws lambda get-function-configuration --profile tessera --function-name <poller>
   --query RuntimeVersionConfig.RuntimeVersionArn --output text`. This value is `RUNTIME_ARN` below.
4. **Issuer, deployable and pinned.** `.venv/bin/python package.py dist/issuer.zip --install-json install-facts.json`,
   then plan and apply with `-var lambda_zip=../dist/issuer.zip -var runtime_version_arn=$RUNTIME_ARN`. That pins
   both functions (`aws_lambda_runtime_management_config`, SG-05), so AWS cannot patch the runtime under the recorded
   Unicode digest. Collecting the facts hashes the SHA-1DC binary but does not run it. Step 9 shows it runs.
5. **KMS signer.** `terraform -chdir=../signer-kms/infra plan` with the issuer's queue and bucket outputs,
   `kms_key_id`, `key_fp` and `trail_retention_days`. The retention has no default, because Object Lock COMPLIANCE
   retention can never be shortened; choose it here. The plan **replaces the key's whole policy**: the account root
   keeps key administration (including `PutKeyPolicy`), only the signer role may `kms:Sign`, and everyone else is
   explicitly denied it. Read that diff, then apply.
6. **Slot-2 signer** (GCP; `service/signer-gcp/README.md`). Run `deploy.sh` steps in order: `sas`, `role`, then
   re-apply the issuer with `signer_principals`, then `keyiam`, `registry`, `build`, `job`, `run-now`, `scheduler`,
   `harden`.
7. **Gate: retire the prototype signer** (SG-03). `deploy.sh retire-instrument` must end with "instrument retired
   and verified". It fails on any error other than "already gone", disables the old service account, and checks that
   nothing of the instrument can still sign. Issuance does not start until this passes.
8. **Gate: who can cause a signature** (SG-04). List the principals that hold, on the AWS side,
   `lambda:InvokeFunction` on the signer, `iam:PassRole` on the signer role, `sqs:SendMessage` on either request
   queue, and `kms:PutKeyPolicy`. On the GCP side, list those that hold `run.jobs.runWithOverrides` or
   `run.jobs.update` on the job, `iam.serviceAccounts.actAs` / token creation on the runtime account, and
   `cloudkms.cryptoKeyVersions.useToSign` on the key. Record the lists in `docs/reviews/signers/REQUESTERS.md`.
   Anything beyond the issuer, the signers and the author's administrator identity is removed before issuance.
9. **Window and smoke test.** Upload `config/window.json` (L1 dates, both key fingerprints) to the result bucket.
   Then send one real request through the API, run it to VALID_STRICT through `service/verifier`, and include a
   negative control. This is the first run of pre-ship on Lambda, so it also shows the packaged detector works there.

## Not deployment gates, but release gates (still open; `formal/freeze-v1/FREEZE-RECORD.md:84-91`)

Before the first **public verifier release**: the custody procedure and its rehearsal; the production release key;
the fingerprint channels the author names; the release-format vectors; the **GCP VPC Service Controls perimeter**;
and a **policy for responses the signer was not asked for** (E-06). Deployment does not cancel any of them.
