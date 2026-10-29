# SAFG World

Community submissions for SAFG:RPG. Fork this repository and open a pull request.

**New here? [Read the step-by-step player guide](docs/PLAYER-GUIDE.md)** for
forking, uploading shader files, opening a PR, requesting approval in game,
and submitting organization bases. No command-line tools required.

## Organization bases — manual placement

Use the **Organization base request** issue form. Include the organization name,
your account, outside entrance coordinates, interior/dimension and screenshots.
Put optional map files under `bases/<organization>/<request>/`. Staff review the
request and manually place/deploy approved bases. Merging a base submission does
not automatically put it on the live server.

## Donation vehicle and skin shaders

1. Fork the repository and create `shaders/<unique-release-key>/` on a branch.
2. Add `request.json`, a local `.fx` shader and, for liveries, a PNG/DDS texture.
   Copy the schema from `examples/request.json`; do not copy example metadata
   into the real catalog without replacing it.
3. Open a PR, then set `github` in your JSON to that PR's URL and push the update.
4. Staff review the visual result, texture targets, shader cost and assets. Once
   merged into **main**, the private server publisher imports the validated files
   into `SAFGworldShaders` automatically. Fork pushes and unmerged PRs never deploy.
5. In game, open `/donationshaders`. Choose your approved donation vehicle or a
   GTA skin model, enter the release key and the same PR URL, and submit.
   Each request reserves **0.5 donation points**. Staff approve it in
   `/donationadmin`; rejection/cancellation returns points only.

A skin shader is account-bound and only appears while you use the approved skin
model. It does not grant a police/medic skin or change your job's spawn model.
Vehicle shaders remain limited to approved donation vehicles owned by the account.
One livery and one FX effect may be assigned per vehicle or per account/skin model.

Use a **new release key** for every revision. Merged releases are immutable and
must remain available for existing approved players. Do not replace/delete old
assets. The importer pins commits and hashes; changing bytes cannot silently
replace someone else's approved shader.

Limits: 128 KiB UTF-8 FX, one PNG/DDS texture up to **512×512 for vehicles** or
**256×256 for skins**, with a 4 MiB file-size ceiling, 1–8
explicit texture names/patterns (never a lone `*`). No Lua, JavaScript, DFF/TXD,
executables, remote URLs, credentials or payment details in shader submissions.
Texture validation is not proof that an arbitrary FX is fast or crash-free;
maintainers must test custom effects in MTA before merging.

Run `python -m pip install -r tools/requirements.txt` then
`python tools/validate.py --world .` to check shader data. CI validates submissions
without deployment secrets. Bases are never included in automatic shader imports.
