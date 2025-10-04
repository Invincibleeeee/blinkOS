# Authenticity & Verification

This document explains how people can verify that work in this repository was authored by the real Invincibleeeee and how you (the repository owner) can present verifiable provenance.

Do NOT attempt to fabricate proofs of identity. The recommendations below are legitimate steps you can take to reduce doubts about authenticity.

Recommended verification signals

- GitHub profile: https://github.com/Invincibleeeee — keep your profile public with a biography and links to other official profiles.
- Public keys: publish a public GPG key and/or an SSH public key to your GitHub account. Share the public key fingerprint in this file so others can verify signed commits.
- Event registration: link to official hackathon registration, team page, or organizer confirmation if applicable.
- Contact channels: provide an official email address or event chat handle so organizers can confirm identity directly.

How to publish a public key (short)

1. Create a GPG key locally (do NOT share the private key):
   - gpg --full-generate-key
2. Export your public key and fingerprint and add it to your GitHub account:
   - gpg --armor --export your.email@example.com
3. Paste the public key into GitHub > Settings > SSH and GPG keys > New GPG key.
4. Add the fingerprint to this file as additional verification.

What to include here

- A short sentence like: "I, Invincibleeeee, confirm that I authored the commits in this repository on behalf of team X. Public GPG fingerprint: <fingerprint>"
- Links to any event registration or official announcements that reference you.

Security reminders

- Never paste private keys, tokens, or passwords into this repo or comments.
- Use 2FA on your GitHub account and avoid sharing account credentials.
