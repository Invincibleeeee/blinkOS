# Commit Signing Guide

This guide explains how to create a GPG key and sign commits so others can verify they were authored by the repository owner.

Short steps

1. Install GPG (e.g., GnuPG).
2. Create a new key: gpg --full-generate-key
3. List keys and get the key ID: gpg --list-secret-keys --keyid-format LONG
4. Configure git to sign commits by default:
   - git config --global user.signingkey <KEYID>
   - git config --global commit.gpgsign true
5. Export your public key and add it to GitHub (Settings > SSH and GPG keys > New GPG key):
   - gpg --armor --export <KEYID>

Verifying signed commits

Others can verify signed commits by checking the signature on commits in the GitHub UI or by running:
 - git log --show-signature

Important

- Do not share private keys or passphrases.
- If you use a hardware key (YubiKey), it's even stronger verification.
