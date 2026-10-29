# Security

## Important warning

ProofPatch AI executes Python code during reproduction and verification. Running code in a temporary directory with a timeout does not make execution safe. Untrusted code may attempt filesystem access, network access, resource exhaustion, or other harmful operations.

Do not expose the current execution workflow as a public service or run untrusted submissions on a machine containing sensitive data.

## Required protections before public execution

- Run each job in a strongly isolated sandbox or disposable container/VM.
- Use a non-privileged account and a read-only base filesystem where practical.
- Restrict network access by default.
- Limit CPU, memory, process count, disk usage, and execution time.
- Restrict file access to the job workspace.
- Enforce request-size and source-code-size limits.
- Add authentication, authorization, rate limiting, and abuse monitoring.
- Avoid logging API keys, secrets, or sensitive source code.
- Validate model responses and patches before any execution.
- Keep the original repository unchanged until a human or trusted process approves changes.

## Secrets

- Store real API keys in local environment configuration or a managed secret store.
- Never commit `.env` files containing real secrets.
- Do not paste credentials into issues, screenshots, logs, or public support requests.
- If a key is exposed, revoke it and issue a replacement.

## Prompt injection and untrusted content

Source code, comments, test names, test output, and model responses must be treated as untrusted data. Instructions embedded in these inputs must not override application policy.

## Verification limitations

Passing defined tests does not prove that a patch is correct for every input. Tests may be incomplete, and code may have side effects that the tests do not detect.

## Reporting vulnerabilities

Do not publish exploit details or secrets in public issues. Until a private security reporting channel is established, contact the project maintainer directly through a trusted channel.
