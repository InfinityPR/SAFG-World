For a skin shader use `"target":"skin"`, a valid GTA skin model ID (0–312,
excluding unused IDs), and its actual skin texture names. Use `"kind":"effect"`
for custom FX; `image` and `uniform` may be omitted for effects that do not need a
texture. Do not submit an example until you have opened a real PR and tested the
actual model/UV texture. `livery.fx` is a small alpha-blended template for a
`gTexture` RGBA texture. Both targets are donor features with staff approval.

For standard liveries, omit `fx`: submit just request.json plus the PNG/DDS image.
The importer supplies the built-in `livery.fx` and `gTexture` binding.
See `skin-request.json` for an image-only skin example. Custom `kind: effect`
submissions still need a reviewed local FX file; existing submissions with an
explicit FX remain valid. Do not edit old merged releases.
