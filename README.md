# Vault web challenge

An intentionally vulnerable, easy-difficulty Flask challenge for a legitimate CTF event. Do not deploy it outside an isolated CTF environment.

## Build and run

```bash
docker build -t vault .
docker run --rm -p 5000:5000 vault
```

Open `http://localhost:5000`.

## Challenge-author reference

The complete flag is assembled from two parts:

```text
CYV{mighty_paul_is_good_boy}
```

1. The document viewer deliberately joins `file` directly to `docs/`. Requesting `/view?file=../config/app.conf` traverses to the configuration file and reveals `FLAG_PART_2=ood_boy}`.
2. Log in with `user` / `user@123`. This sets the client-controlled `role` cookie to Base64-encoded `user` (`dXNlcg==`). Replacing it with Base64-encoded `admin` (`YWRtaW4=`) allows `/admin` and reveals `FLAG_PART_1=CYV{mighty_paul_is_g`.

These weaknesses are intentional and should remain limited to the CTF deployment.
# cyv-web-chall
