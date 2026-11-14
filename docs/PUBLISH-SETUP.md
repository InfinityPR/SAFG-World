# Immediate shader publishing (maintainer setup)

After InfinityPR merges a PR into main, **Publish merged shaders** starts the
private publisher immediately. That publisher validates all immutable release
keys, the maintainer merge and exact asset hashes, then deploys only
SAFGworldShaders. No PR code is checked out or executed by the dispatch workflow.

One-time credential setup:

1. Create a fine-grained GitHub token with resource owner InfinityPR.
2. Select **only InfinityPR/safg-server** under repository access.
3. Grant repository **Actions: Read and write**. No Contents or administration
   permission is needed for this dispatch token. Use an expiry and renew it
   before it expires.
4. In **InfinityPR/SAFG-World → Settings → Secrets and variables → Actions**,
   create repository secret **SAFG_SHADER_PUBLISH_TOKEN** with that token.
5. Open **Actions → Publish merged shaders → Run workflow** to test it.

Do not paste the token in issues, PRs or chat, or commit it to either repository.
The public workflow has no private server checkout, host keys or payment settings.
Its only privileged command starts the fixed private publisher on main.

The existing private five-minute schedule remains a fallback, subject to GitHub
queue delays. In-game staff approval is still required after asset deployment.
