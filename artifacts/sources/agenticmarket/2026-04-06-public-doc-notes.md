# AgenticMarket Public Doc Notes

Captured: 2026-04-06

## Sources

- Home: <https://agenticmarket.dev/>
- Publishing guide: <https://agenticmarket.dev/docs/publishing-server>
- Monetization guide: <https://agenticmarket.dev/docs/monetization>
- Pricing page: <https://agenticmarket.dev/pricing>
- Monetization blog post: <https://agenticmarket.dev/blog/monetize-mcp-servers>

## Key Operational Facts

- AgenticMarket positions itself as a CLI-first MCP platform with one-command installs.
- It supports multiple MCP-capable tools, including Codex, Claude Code, Cursor, and
  related clients.
- Creators publish their own hosted MCP servers; AgenticMarket handles routing,
  authentication, billing, and payouts.
- Servers must already be deployed on a public HTTPS endpoint, follow the MCP spec,
  and expose discoverable tools via `tools/list`.

## Listing Constraints

- Server name is a unique lowercase identifier and is effectively fixed after publish.
- Server URL is also effectively fixed after publish.
- Price per call has a minimum of $0.01 and is fixed after publish; changing price
  requires a new listing.
- Visibility can be changed later, which makes unlisted first launches attractive.
- The long description should function like a README with tool list, parameters,
  example prompts, and limitations.

## Monetization Facts

- Standard revenue share is 80%; Founding Creator share is 90% for the first 100
  approved creators for 12 months.
- Minimum payout is $20 via Wise or Razorpay.
- The pricing page frames the platform as pay-as-you-go for users.

## Product Implications

- First products should be narrow and stable because name, URL, and price are sticky.
- Listing quality matters; vague general-purpose positioning is a bad fit.
- Per-call value should be legible enough that a buyer can justify the price from the
  listing alone.
- Builder-facing tools are a natural first fit because the marketplace audience is
  already MCP-native.
