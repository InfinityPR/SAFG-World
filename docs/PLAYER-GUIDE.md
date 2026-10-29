# SAFG World: player submission guide

Use this guide to request a custom **donation vehicle shader**, **player skin
shader**, or **organization base**. You can do the GitHub steps in your normal web
browser; you do not need Git, a terminal, or access to the server files.

- [Start here: fork and branch](#1-fork-the-repository-and-create-a-branch)
- [Prepare a shader submission](#2-prepare-your-shader-files)
- [Open a pull request](#3-open-your-pull-request-and-add-its-link)
- [Request the shader in game](#5-request-your-shader-in-game)
- [Request an organization base](#organization-base-requests)
- [Fix common problems](#common-problems)

## Before you start

A **fork** is your own copy of SAFG-World. A **branch** keeps one submission's
changes together. A **pull request (PR)** asks SAFG staff to review and merge those
changes into the official repository.

| Request | What you need | In-game cost |
| --- | --- | --- |
| Vehicle livery or FX | An approved donation vehicle owned by your account; assets for its exact model | 0.5 donation points per shader request |
| Player skin livery or FX | Assets for a valid GTA skin model; your game account | 0.5 donation points per shader request |
| Organization base | Organization details, coordinates, screenshots, and map files if applicable | Staff review; this guide does not set a base price |

A skin shader changes the appearance of an existing model. It does **not** unlock
SWAT, police, medic, or other restricted uniforms, or give you a new spawn class.
Use assets you made or have permission to submit. This is a public repository:
include your game account name where requested, never passwords or payment details.

## 1. Fork the repository and create a branch

1. Sign in to [GitHub](https://github.com).
2. Open [InfinityPR/SAFG-World](https://github.com/InfinityPR/SAFG-World).
3. Click **Fork** near the top right, then **Create fork**. The owner should be
   your GitHub account. If you already have a fork, open that instead.
4. Your copy's address should look like `github.com/YOUR-NAME/SAFG-World`.
5. If this is an older fork, select its **main** branch and use **Sync fork →
   Update branch** before starting a new submission. If GitHub reports conflicts,
   ask staff before discarding any of your work.
6. Open the branch selector (normally labelled **main**). Type a new branch name,
   such as `my-swat-skin-v1`, and choose **Create branch** from main.
7. Check that this new branch is selected before editing or uploading files.

Keep each request on its own branch. Work in your fork, then submit the PR to the
official InfinityPR repository.

## 2. Prepare your shader files

### Choose a release key

Your release key is the folder name under `shaders/`, for example
`my-swat-skin-v1`. You will type this exact key in game later.

Use lowercase letters, numbers, hyphens, or underscores; start with a letter or
number and keep it to 64 characters or fewer. Choose a name not already present
in the official repository. **Do not edit or delete an existing merged release.**
For a later revision, use a new key such as `my-swat-skin-v2`; it needs a new
in-game request and approval.

### Files and limits

For a paint/livery submission, your folder should look like this:

```text
shaders/my-swat-skin-v1/
    request.json
    livery.fx
    swat.png
```

- `request.json` describes the model, texture targets, and files.
- The `.fx` file applies the texture or implements your custom effect. The
  [example livery.fx](../examples/livery.fx) can be used for a basic livery with
  the `gTexture` uniform.
- A livery requires one PNG or DDS texture: at most **512 × 512 pixels for
  vehicles**, or **256 × 256 pixels for skins**. Both width and height must fit
  the limit; smaller and rectangular textures are allowed. The file must also
  stay within **4 MiB**. Match the model's texture layout (UVs); an arbitrary picture will
  not automatically fit the skin or vehicle.
- FX must be UTF-8 text, at most **128 KiB**. Custom effects need testing in MTA;
  passing the file checks does not prove an effect is fast or visually correct.
- Supply **1–8 actual texture names or targeted patterns** from the model. A lone
  `*` is forbidden. Texture names are not the name of your uploaded image.
- Use simple local filenames such as `livery.fx` and `swat.png`, with lowercase
  extensions. Do not submit remote asset URLs, Lua/JS scripts, executables, or
  replacement DFF/TXD models as shader assets.

If you do not know the model's texture names or how to prepare its texture,
ask staff or an experienced texture creator before submitting.

### Example: SWAT skin livery

The working [SWAT submission](../shaders/swat-skin/request.json) uses skin model
**285** and texture name **swat**. For your own release, create this JSON:

```json
{
  "target": "skin",
  "model": 285,
  "kind": "livery",
  "github": "https://github.com/InfinityPR/SAFG-World/pull/123",
  "textures": ["swat"],
  "fx": "livery.fx",
  "image": "swat.png",
  "uniform": "gTexture"
}
```

**123 is a placeholder.** Replace it with your real PR number in step 3. Do not
reuse the example's PR or the already-published `swat-skin` release key.

| Field | What to enter |
| --- | --- |
| `target` | `skin` for a player skin, or `vehicle` for a donation vehicle |
| `model` | The exact numeric GTA model ID; no quotation marks. Use a valid skin ID or vehicle ID 400–611 |
| `kind` | `livery` for paint/texture, or `effect` for a custom FX effect |
| `github` | Your PR's exact URL in the official InfinityPR/SAFG-World repository |
| `textures` | The actual texture names/patterns to which your shader applies |
| `fx` | Your local FX filename, including `.fx` |
| `image` | Your local PNG/DDS filename; required for liveries |
| `uniform` | The image input variable used by your FX; `gTexture` for the provided livery template |

For a vehicle, set `target` to `vehicle`, use your donation vehicle's model ID,
and change the texture targets to that model's textures. Do not copy `swat` for
a vehicle. For an effect without an image input, omit `image` and `uniform`;
keep `textures`, and set `kind` to `effect`.

### Add the files through GitHub

1. In your fork on your submission branch, click **Add file → Create new file**.
2. Enter `shaders/my-swat-skin-v1/request.json` as the filename. Replace the key
   with your own. Slashes create the folders.
3. Paste and edit the JSON, then **Commit changes** to your submission branch.
4. Open that new folder and use **Add file → Upload files** for your `.fx` and
   image. Commit them to the same branch. You can also create/paste a text `.fx`
   through **Create new file**.
5. Check the filenames and folder. All referenced files must be together, without
   an extra nested folder or a ZIP archive.

## 3. Open your pull request and add its link

1. In your fork, click **Contribute → Open pull request**. Alternatively open the
   official repository's **Pull requests → New pull request → compare across forks**.
2. Check **base repository** is `InfinityPR/SAFG-World`, **base** is `main`, and
   **head/compare** is your fork and submission branch.
3. Give it a clear title, such as `Skin livery: my SWAT design (model 285)`.
4. Include your game account name, release key, target/model, screenshots or a
   video, and any asset credits. Explain how you tested it. Do not claim testing
   you have not done; say if you need staff help testing.
5. Click **Create pull request**, then copy its address. It should look like
   `https://github.com/InfinityPR/SAFG-World/pull/123`.
6. Return to `request.json` **in your fork on the same submission branch**, click
   the pencil to edit it, and replace the placeholder `github` URL with this PR's
   exact URL. Do not include `#issue-...`, comments, or extra query text.
7. Commit the edit to that same branch. Your open PR updates automatically;
   you do not need another PR for this correction.

## 4. Wait for checks, staff review, and deployment

Open your PR's **Checks** tab. A first-time fork can show **workflows awaiting
approval**: a maintainer must approve the workflow run. You do not need a token
or server access to fix this.

If validation fails, read the failing check, correct the files in your submission
branch, and commit again. Common causes are missing `textures`, a wrong PR URL,
invalid JSON, mismatched filenames, or an oversized image.

Staff review the appearance and FX, then the repository owner merges approved
assets into official **main**. Players do not need to merge their own PRs.
The publisher then imports reviewed shader files and deploys them to the game.
It checks on a schedule; merging is not an instant guarantee that the release is
available. If the in-game panel cannot find it, ask staff to check publishing.

**There are two separate approvals:** the GitHub review approves the asset files;
the in-game approval assigns a published shader to your account/vehicle.

## 5. Request your shader in game

1. Log in to the account that should receive the shader. Have at least **0.5
   donation points** available.
2. Type **`/donationshaders`**.
3. Under **Apply shader to**, choose **Approved donation vehicle** or **Player skin**.
4. Select your own approved donation vehicle, or enter the same skin model ID as
   your `request.json`.
5. Select **Paint / livery texture** or **Custom FX effect**, matching `kind`.
6. Enter your folder name in **GitHub release key**, for example
   `my-swat-skin-v1`. Do not enter a file path or `.json` filename.
7. Paste the same official PR URL used in `request.json`, add useful notes, and submit.
8. The request reserves **0.5 points**. Wait for an admin to review it through
   **`/donationadmin`**. Rejection or cancellation returns the reserved points;
   this is not a refund of the PayPal donation.
9. After approval, spawn the approved donation vehicle or use the approved skin
   model on your requesting account. Skin shaders follow that account/model;
   they do not unlock the model. If it does not appear, tell staff the release key,
   PR URL, and request ID shown in your panel.

One livery and one FX effect can be assigned per vehicle or per account/skin model.
A new approval for the same slot replaces that slot's assignment.

## Organization base requests

Bases use a separate, **manual** review and placement process.

1. Prepare screenshots and the entrance's **x, y, z, rotation, interior, and
   dimension**, plus the organization name and leader's game account name.
2. If supplying map files, follow step 1 to fork/create a branch. Put your files
   under `bases/YOUR-ORGANIZATION/YOUR-REQUEST/`, with a short README explaining
   placement, entrances, and any required assets. Open a PR to official main as
   in step 3. Shader `request.json` is not needed for a base.
3. Open [Organization base request](https://github.com/InfinityPR/SAFG-World/issues/new?template=organization-base.yml).
4. Complete the form, attach screenshots, and link your map PR. If you need help
   preparing files, explain that in the form rather than inventing a PR URL.
5. Staff discuss, review, and arrange approved placement/deployment manually.
   A merged base PR does **not** automatically place the base in game.

## Common problems

| Problem | What to do |
| --- | --- |
| I cannot find Fork | Sign in to GitHub and open the official repository; if you already forked it, use your existing copy |
| My changes are missing from the PR | Check you edited the PR's submission branch in your fork, not main or a different branch |
| Merging is blocked / checks await approval | Wait for maintainer approval of a first-fork workflow, read failed checks, and address staff feedback; do not bypass checks |
| JSON check fails | Use double quotes, no comments, no trailing comma; compare fields with the example above |
| Missing or unsupported asset | Match the exact filename, case, extension, and folder in `request.json` |
| Release key already exists / immutable release | Choose a new versioned folder key; leave merged assets unchanged |
| In-game release unavailable or mismatch | Match key, model, kind, and exact PR URL; ask staff whether publishing finished |
| No vehicle in the selector | Vehicle shaders require an approved donation vehicle owned by the requesting account |
| SWAT shader approved but I cannot choose SWAT | Shader approval does not grant access to restricted uniforms or classes |
| Points returned after rejection | These are donation points returned to the account, not a payment refund |

If asking staff for help, send the **PR URL, release key, game account name, and
exact error/check message**. These let staff find the right submission quickly.
