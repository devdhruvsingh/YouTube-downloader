# Security Policy

## Overview

Security is a core requirement of the YouTube Downloader project.

This application accepts user-provided YouTube URLs, communicates with external services, retrieves media information, processes media files, and temporarily stores files on the server.

Because of this, the application must carefully validate user input, restrict external resource access, protect backend resources, and remove temporary data after processing.

The application is intended to be used only for media that the user is authorized to download.

---

## Supported Use

This project is designed to process supported YouTube URLs for content that the user has permission to download.

The application must not be treated as a generic URL downloader or arbitrary proxy.

Only supported and explicitly allowed domains should be accepted by the backend.

---

## Security Principles

The project follows these principles:

* Validate all user input.
* Never trust user-provided URLs or format identifiers.
* Restrict accepted domains.
* Minimize data retention.
* Avoid storing downloaded media permanently.
* Remove temporary files after processing.
* Never expose internal filesystem paths.
* Never expose application stack traces to users.
* Limit resource consumption.
* Protect public endpoints from abuse.
* Keep secrets outside the source code.
* Keep dependencies updated.
* Prefer secure defaults.

---

## URL Validation

User-submitted URLs must be validated before any media-processing operation begins.

The backend should:

1. Verify that the URL is structurally valid.
2. Parse the URL safely.
3. Verify that the hostname belongs to an explicitly allowed YouTube domain.
4. Reject unsupported domains.
5. Reject malformed URLs.
6. Reject empty or invalid input.
7. Avoid accepting arbitrary URLs as download targets.

Example accepted URL patterns may include supported YouTube URL formats such as:

* `https://www.youtube.com/watch?v=...`
* `https://youtu.be/...`

The exact list of supported URL formats should be maintained by the application and tested.

URL validation must happen before expensive operations such as metadata extraction or downloading.

---

## SSRF and Arbitrary URL Protection

The backend must not become a generic server-side request proxy.

User input must never be passed directly to arbitrary network requests without validation.

The application should:

* Restrict accepted domains.
* Reject non-YouTube domains.
* Validate the parsed hostname.
* Avoid allowing user-controlled destinations.
* Avoid exposing internal network resources.
* Avoid accepting localhost or private network targets through generic URL handling.
* Never provide a generic "download this URL" feature.

This is particularly important because the backend performs network operations on behalf of the user.

---

## Format Validation

The frontend may display format identifiers returned by the backend.

However, the backend must not blindly trust a format identifier supplied by the client.

Before processing a download request, the backend should:

* Validate the format identifier.
* Confirm that the format belongs to the requested media.
* Reject unknown or malformed format identifiers.
* Prevent clients from manipulating format parameters to perform unintended operations.

The backend remains responsible for determining whether a requested format is permitted.

---

## Filename Security

Downloaded media may contain filenames originating from external metadata.

Filenames must therefore be sanitized before being used on the server filesystem.

The application should:

* Remove unsafe path characters.
* Prevent path traversal.
* Prevent absolute filesystem paths.
* Prevent filenames such as `../../file`.
* Avoid directly trusting external titles as filesystem paths.
* Generate safe temporary filenames where practical.

The application must never allow user-controlled input to determine an arbitrary filesystem location.

---

## Path Traversal Protection

The application must prevent path traversal attacks.

Examples of dangerous input include:

```text
../../secret.txt
../../../etc/passwd
/var/www/file
~/private/file
```

User-controlled values must never be concatenated directly into filesystem paths.

Temporary directories should be controlled by the application.

---

## Temporary File Management

Downloaded files are temporary application data.

The expected lifecycle is:

```text
Request
   ↓
Create temporary directory
   ↓
Download/process media
   ↓
Send file to user
   ↓
Delete temporary file
   ↓
Delete temporary directory
```

Temporary files must be removed after successful processing.

Cleanup must also occur when:

* The download fails.
* Media processing fails.
* A request times out.
* An unexpected exception occurs.
* The client disconnects where practical.

The application should avoid permanently storing downloaded media.

---

## Data Retention and Privacy

The application should follow a minimal-data-retention approach.

The MVP should avoid permanently storing:

* Submitted URLs.
* Downloaded videos.
* User information.
* Unnecessary request data.

Temporary media files should be deleted after processing.

If future versions introduce logging, analytics, accounts, or download history, those features should be reviewed separately for privacy and security implications.

---

## Rate Limiting

A publicly deployed downloader can consume significant server resources.

The application should implement rate limiting to reduce abuse.

Recommended protections include:

* IP-based rate limiting.
* Concurrent download limits.
* Request frequency limits.
* Processing timeouts.
* Maximum download size.
* Maximum request size.
* Protection against repeated expensive metadata requests.

The MVP may use a simple rate-limiting mechanism, with stronger controls introduced as the application scales.

---

## Resource Protection

Media processing can consume substantial:

* CPU
* RAM
* Disk space
* Network bandwidth

The backend should therefore enforce reasonable limits.

Where practical, the application should limit:

* Maximum file size.
* Maximum processing duration.
* Number of simultaneous downloads.
* Number of requests per client.
* Temporary storage usage.

The application should fail safely when resource limits are reached.

---

## Error Handling

Internal exceptions must not be exposed directly to users.

Do not return:

```text
Traceback (most recent call last):
...
```

or internal filesystem paths, implementation details, or sensitive configuration values.

Instead, users should receive a safe and useful message such as:

```text
Unable to process this video.

The video may be unavailable or the request may be invalid.
```

Detailed errors may be recorded in server logs where appropriate, but sensitive information should not be logged unnecessarily.

---

## Secrets and Environment Variables

Secrets and environment-specific configuration must not be committed to Git.

Sensitive values should be stored using environment variables.

Examples include:

```text
CORS_ORIGINS
TEMP_DIRECTORY
MAX_FILE_SIZE
```

The repository should contain an `.env.example` file containing configuration names and safe example values.

The real `.env` file must remain excluded from Git.

Never commit:

* API keys.
* Authentication tokens.
* Passwords.
* Private credentials.
* Production secrets.

---

## CORS

The backend should use an explicit CORS configuration.

Production deployments should not blindly allow every origin.

Avoid using unrestricted configuration such as:

```text
*
```

unless there is a specific and documented reason.

Allowed frontend origins should be configured through environment variables where appropriate.

---

## API Security

All public API endpoints should validate incoming requests.

The backend should:

* Validate request bodies.
* Validate URL parameters.
* Validate format identifiers.
* Apply rate limits.
* Return appropriate HTTP status codes.
* Avoid exposing internal exceptions.
* Apply reasonable request limits.
* Reject malformed requests.

The API should expose only the functionality required by the application.

---

## Dependency Security

The project depends on external packages including:

* FastAPI
* Uvicorn
* Pydantic
* yt-dlp
* FFmpeg
* React
* Vite
* Tailwind CSS

Dependencies should be kept reasonably up to date.

Before upgrading major dependencies, the project should be tested to ensure that security improvements do not introduce functional regressions.

Dependency files should be committed so that project environments remain reproducible.

---

## FFmpeg Security

FFmpeg may be used for media processing and format merging.

FFmpeg operations should only process files and formats generated through the application's controlled workflow.

The application should avoid passing arbitrary user-controlled command-line arguments to FFmpeg.

Command construction must prevent command injection.

---

## Logging

Logs should contain enough information to diagnose application problems without unnecessarily collecting user data.

Avoid logging:

* Secrets.
* Authentication tokens.
* Environment variables containing credentials.
* Full sensitive request data.
* Unnecessary personal information.

If submitted URLs are logged for debugging, retention should be minimized.

---

## Security Headers

The production frontend and backend should use appropriate security-related HTTP headers where supported by the deployment architecture.

Potential protections include:

* Content Security Policy.
* X-Content-Type-Options.
* Referrer-Policy.
* Frame protection.
* Strict Transport Security when HTTPS is correctly configured.

Security headers should be tested in the production environment before release.

---

## HTTPS

Production deployments should use HTTPS.

Sensitive configuration, API requests, and application traffic should not be transmitted over unencrypted HTTP.

HTTP-to-HTTPS redirection should be configured where supported by the hosting infrastructure.

---

## Authentication

Authentication is not required for the MVP.

Future versions may introduce authentication if features such as:

* User accounts.
* Download history.
* Usage statistics.
* Personal preferences.

are added.

If authentication is introduced, it must be designed and reviewed separately rather than added as an informal extension of the MVP.

---

## Abuse Prevention

The application should assume that a public downloader endpoint may be abused.

Potential abuse includes:

* Excessive download requests.
* Resource exhaustion.
* Automated request flooding.
* Large file requests.
* Repeated metadata extraction.
* Attempts to bypass URL validation.
* Attempts to manipulate filesystem paths.
* Attempts to exploit backend dependencies.

The application should use layered protections rather than relying on a single validation mechanism.

---

## Security Testing

Before production deployment, the project should test at minimum:

### URL Validation

* Valid YouTube URLs.
* Invalid URLs.
* Unsupported domains.
* Malformed URLs.
* Empty URLs.
* Unexpected URL parameters.

### Format Validation

* Valid format IDs.
* Invalid format IDs.
* Missing format IDs.
* Unexpected format values.

### File Handling

* Unsafe filenames.
* Path traversal attempts.
* Large files.
* Temporary-file cleanup.
* Failed downloads.

### API

* Malformed requests.
* Repeated requests.
* Invalid request bodies.
* Timeout behavior.
* Error responses.

### Configuration

* Missing environment variables.
* Invalid configuration values.
* CORS configuration.
* Production configuration.

---

## Responsible Disclosure

If you discover a security vulnerability, please do not publicly disclose the vulnerability before the project maintainers have had an opportunity to investigate it.

Report the issue privately through the project's designated security contact or GitHub security reporting mechanism.

When reporting a vulnerability, provide:

* A clear description.
* Steps to reproduce.
* Expected behavior.
* Actual behavior.
* Potential impact.
* Relevant logs or screenshots where safe.
* A suggested mitigation if available.

Do not include passwords, API keys, tokens, or other secrets in a security report.

---

## Security Issue Severity

Security issues may be categorized approximately as:

### Critical

Issues that could result in:

* Remote code execution.
* Complete server compromise.
* Major unauthorized access to sensitive systems.

### High

Issues that could result in:

* Significant unauthorized access.
* Major data exposure.
* Serious resource exhaustion.

### Medium

Issues that could result in:

* Limited unauthorized behavior.
* Significant application abuse.
* Partial information disclosure.

### Low

Issues with limited impact that do not significantly compromise the application.

Severity may be adjusted based on the actual exploitability and impact.

---

## Security Checklist

Before production deployment:

* [ ] URL validation implemented.
* [ ] Allowed domains restricted.
* [ ] Arbitrary URL downloading disabled.
* [ ] Format IDs validated.
* [ ] Filename sanitization implemented.
* [ ] Path traversal protection implemented.
* [ ] Temporary files automatically removed.
* [ ] Download size limits configured.
* [ ] Processing timeouts configured.
* [ ] Rate limiting implemented.
* [ ] Concurrent download limits configured.
* [ ] CORS restricted to trusted origins.
* [ ] Secrets stored in environment variables.
* [ ] `.env` excluded from Git.
* [ ] Stack traces hidden from users.
* [ ] Security headers reviewed.
* [ ] HTTPS enabled.
* [ ] Dependencies reviewed.
* [ ] Backend tests passing.
* [ ] Security-related tests passing.
* [ ] Production configuration reviewed.

---

## Scope

This policy applies to the YouTube Downloader application and its associated source code, infrastructure, API, frontend, backend, and deployment configuration.

The project should be used only for content that the user is authorized to download.

---

## Final Security Principle

> **Validate input, minimize data retention, limit resource usage, isolate temporary processing, and fail safely.**

Security should be treated as part of the application's architecture rather than as a feature added immediately before deployment.

