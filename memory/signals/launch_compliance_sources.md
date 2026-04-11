# Launch Compliance Harvest Sources

This note defines the public discovery surfaces used to refresh the launch
compliance target queue.

These sources are for target discovery only. They do not count as evidence.

## Fields

- `source_id`
- `url`
- `source_type`
- `status`
- `notes`

## Source Registry

| source_id | url | source_type | status | notes |
| --- | --- | --- | --- | --- |
| agenticmarket-sitemap | https://agenticmarket.dev/sitemap.xml | agenticmarket_sitemap | active | crawlable source of creator and listing URLs; use this as the primary harvest surface |
| agenticmarket-servers | https://agenticmarket.dev/servers | agenticmarket_servers | paused | registry shell is heavily client-rendered; keep paused unless it becomes harvestable again |
| smithery-registry | https://registry.smithery.ai/servers?pageSize=50 | smithery_registry | active | Smithery MCP directory API; yields independent builders with GitHub-linked homepages |
| github-mcp-repos | https://api.github.com/search/repositories?q=mcp-server+pushed:>2026-03-01&sort=updated&per_page=50 | github_mcp_search | active | GitHub search for recently-active MCP server repos; yields builders with public profiles and contact paths |

## Rules

- keep the source set narrow and high-signal
- add a new source only if it repeatedly yields real targets
- remove or pause sources that create noise without converting into conversations
