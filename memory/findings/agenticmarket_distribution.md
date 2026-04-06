# AgenticMarket As Initial Distribution Surface

## Recommendation

Use AgenticMarket as the first public distribution and monetization surface for
Skillfoundry-built hosted MCP servers.

## Why It Fits

- It is already oriented around MCP-native installation and use.
- It handles billing, routing, authentication, and payouts, which removes a major
  amount of non-core infrastructure work.
- It is credible for reaching the same technical ICP we want to serve first.
- It supports unlisted visibility, which gives us a controlled first launch path.

## Operational Constraints

- The server must already be deployed at a public HTTPS endpoint.
- The listing must expose at least one discoverable MCP tool and respond correctly
  to `tools/list`.
- The server name, server URL, and price per call are effectively fixed after
  publish, so the initial tool surface and pricing choice must be deliberate.
- The long description should be treated as README-quality operator documentation,
  not marketing filler.

## Commercial Implication

Because price is fixed after publish, early listings should favor:

- narrow tools,
- legible value per call,
- low operational variability,
- and copy that tells users exactly what the tool does.

## Source Basis

See `artifacts/sources/agenticmarket/2026-04-06-public-doc-notes.md`.
