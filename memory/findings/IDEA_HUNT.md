# IDEA HUNT

This file is the running scouting log for new Skillfoundry directions.

Purpose:

- capture raw external signals quickly
- preserve how the search was done, not just what it found
- separate promising paths from weak paths early
- keep enough mess to learn from the hunt process before later cleanup
- connect hunt outputs back to the longer-term compounding-foundry thesis in [COMPOUNDING_PRIMITIVES.md](./COMPOUNDING_PRIMITIVES.md)

Operating rules:

- prefer fresh external signals over internal theorizing
- log source quality and search-path quality separately
- mark whether a signal is operational, commercial, or research-only
- record dead ends explicitly so the same weak paths do not get retried blindly

Status:

- started: `2026-04-11`
- owner: `skillfoundry`
- stage: `initial scouting`

## Hunt Questions

1. Where is real new pain emerging in the agent, MCP, and AI workflow stack?
2. Which pains are narrow enough for cheap Stage 1 probes?
3. Which surfaces look commercially reachable soon rather than merely technically interesting?
4. Which search methods produce decision-worthy signals fastest?

## Search Log

### Pass 1: ecosystem infrastructure and standards

- query family:
  - `Model Context Protocol official announcements`
  - `agent marketplace MCP servers official launch`
  - `OpenAI remote MCP official`
- result quality: `high`
- why it worked:
  - official ecosystem posts are good for structural direction
  - easy to distinguish substrate shifts from hype
- limitation:
  - weak on immediate monetizable pain

### Pass 2: latest enterprise and automation trend scanning

- query family:
  - `AI agents automation what actually works 2026`
  - `enterprise AI finally gets to work 2026`
- result quality: `medium`
- why it worked:
  - good for seeing where buyers are being educated
  - useful for language and wedge framing
- limitation:
  - lots of trend writing, little hard pain specificity

### Pass 3: official platform capability scanning

- query family:
  - `OpenAI Responses API remote MCP official`
  - `OpenAI Agents SDK official`
  - `Anthropic tool search programmatic tool calling official`
- result quality: `high`
- why it worked:
  - best way to identify what the substrate now makes easy
  - good for spotting suddenly-cheap probe classes
- limitation:
  - can bias toward buildability over demand

### Pass 4: live marketplace surface checks

- query family:
  - direct checks of AgenticMarket listings and live product surfaces
- result quality: `high`
- why it worked:
  - immediately useful for operational readiness and channel shape
- limitation:
  - does not prove demand on its own

### Pass 5: recent research sweep

- query family:
  - recent agents, tool-use, coding-agent, and evaluation papers
- result quality: `pending further deepening`
- why it may work:
  - good for finding capability discontinuities before they become product common sense
- limitation:
  - research novelty often outruns buyer demand

## Signals

### Structural signal: MCP is infrastructure now, not fringe glue

- type: `operational and strategic`
- source quality: `high`
- implication:
  - do not treat MCP-native products as speculative edge cases anymore
  - the better question is where narrow MCP surfaces become commercial leverage
- provisional search score: `promising`
- source notes:
  - Anthropic said on `2025-12-09` that MCP had grown to more than `10,000 active public MCP servers` and had been adopted by ChatGPT, Cursor, Gemini, Microsoft Copilot, and VS Code.
  - this is a substrate maturity signal, not a direct demand signal
- references:
  - Anthropic, `Donating the Model Context Protocol and establishing the Agentic AI Foundation`:
    `https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation`

### Structural signal: remote MCP support is normalizing inside major agent stacks

- type: `operational`
- source quality: `high`
- implication:
  - wrapper products, workflow adapters, and narrow workflow copilots got cheaper to ship
  - probe classes that depend on hosted remote tool access are more viable now
- provisional search score: `promising`
- source notes:
  - OpenAI announced remote MCP server support in the Responses API on `2025-05-21`, alongside background mode and built-in tools.
  - Anthropic's MCP connector docs show remote MCP is directly consumable through the Messages API, but only for tool calls and only over public HTTP.
- references:
  - OpenAI, `New tools and features in the Responses API`:
    `https://openai.com/index/new-tools-and-features-in-the-responses-api/`
  - Anthropic Claude API docs, `MCP connector`:
    `https://platform.claude.com/docs/en/agents-and-tools/mcp-connector`

### Structural signal: enterprise messaging says agents are moving from experiment to workflow

- type: `market framing`
- source quality: `medium`
- implication:
  - there is likely room for products that reduce adoption friction, trust friction, and operating ambiguity
  - messaging alone is not enough; need direct pain signals
- provisional search score: `needs triangulation`
- source notes:
  - Microsoft's `2025 Work Trend Index` says `82% of leaders` see this as a pivotal year to rethink strategy and operations, and `81%` expect agents to be moderately or extensively integrated into AI strategy in the next `12-18 months`.
  - Microsoft's follow-up says employees are interrupted every `two minutes` and `275 times a day`, which points toward workflow-compression and interruption-reduction wedges.
- references:
  - Microsoft WorkLab, `2025: The year the Frontier Firm is born`:
    `https://www.microsoft.com/en-us/worklab/work-trend-index/2025-the-year-the-frontier-firm-is-born`
  - Microsoft WorkLab, `Breaking down the infinite workday`:
    `https://www.microsoft.com/en-us/worklab/work-trend-index/breaking-down-infinite-workday`

### Structural signal: the market is filling with substrate, not clarity

- type: `commercial`
- source quality: `medium-high`
- implication:
  - there may be value in decision support, evaluation, packaging, compliance, and operational narrowing rather than general-purpose orchestration
- provisional search score: `promising`
- source notes:
  - Vercel's AI SDK 5 release emphasizes `agentic loop control` and highly typed agent application structure, which suggests frameworks are racing toward buildability.
  - Anthropic's MCP directory policy is already imposing sharp compatibility, safety, performance, and documentation constraints. That implies a practical gap between “you can build a server” and “you can get trusted distribution”.
- references:
  - Vercel, `AI SDK 5`:
    `https://vercel.com/blog/ai-sdk-5`
  - Anthropic support, `Anthropic MCP Directory Policy`:
    `https://support.claude.com/en/articles/11697096-anthropic-mcp-directory-policy`

### Structural signal: tool overload is becoming a first-order cost and latency problem

- type: `operational and commercial`
- source quality: `high`
- implication:
  - there may be room for tool filtering, tool-surface minimization, and runtime governance products
  - the problem is not only "which tool exists", but "which subset should be exposed and trusted"
- source notes:
  - Anthropic's programmatic tool calling is positioned as a way to reduce latency and token consumption in multi-tool workflows.
  - OpenAI's remote MCP guidance explicitly warns that servers may expose dozens of tools and recommends `allowed_tools` to constrain cost and latency.
- references:
  - Anthropic Claude API docs, `Programmatic tool calling`:
    `https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling`
  - OpenAI docs, `Connectors and MCP servers`:
    `https://platform.openai.com/docs/guides/tools-remote-mcp`

## Research Sweep Notes

### Research signal: "skills" themselves may be a weak abstraction

- type: `research and strategic`
- source quality: `high`
- why it matters:
  - directly pressure-tests the old Skillfoundry ontology
  - suggests that reusable skill packs are not automatically valuable just because they are structured
- note:
  - `SWE-Skills-Bench` reports that `39 of 49 skills` produced zero pass-rate improvement and the average gain was only `+1.2%`
  - only a small minority of specialized skills created meaningful gains
- implication:
  - do not build around “skills” as the core economic unit
  - if a path depends on reusable skill-pack injection, require hard evidence fast
- references:
  - arXiv, `SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World Software Engineering?`:
    `https://arxiv.org/abs/2603.15401`

### Research signal: long-horizon agents still have large evaluation gaps

- type: `research`
- source quality: `high`
- note:
  - `AgencyBench` says real-world scenarios require an average of `90 tool calls`, `1 million tokens`, and `hours` of execution time
  - performance differs materially by native framework and model ecosystem
- implication:
  - there may be room for products that shrink, scaffold, or benchmark real-world multi-tool work
  - there is also danger in building ambitious long-horizon products too early
- references:
  - arXiv, `AgencyBench: Benchmarking the Frontiers of Autonomous Agents in 1M-Token Real-World Contexts`:
    `https://arxiv.org/abs/2601.11044`

### Research signal: web-agent progress is likely overstated

- type: `research`
- source quality: `high`
- note:
  - `An Illusion of Progress?` argues current results are over-optimistic and introduces a more realistic benchmark over `300 tasks` and `136 websites`
  - the paper reports roughly `85%` agreement between its LLM-as-a-judge method and human judgment
- implication:
  - avoid assuming browser automation is solved
  - evaluation, failure interpretation, and trust tooling may be easier wedges than full autonomous browser products
- references:
  - arXiv, `An Illusion of Progress? Assessing the Current State of Web Agents`:
    `https://arxiv.org/abs/2504.01382`

### Research signal: agent memory remains weak and structurally lossy

- type: `research`
- source quality: `high`
- note:
  - `AMA-Bench` argues existing memory systems underperform because they lack causality and objective information and rely too much on lossy similarity-based retrieval
- implication:
  - "memory for agents" is a real problem
  - but it is likely a dangerous first commercial wedge unless tightly scoped to a concrete workflow
- references:
  - arXiv, `AMA-Bench: Evaluating Long-Horizon Memory for Agentic Applications`:
    `https://arxiv.org/abs/2602.22769`

## Candidate Paths

### 1. Launch and packaging intelligence for MCP builders

- why it still matters:
  - live evidence already exists that builders need help packaging and listing servers
  - adjacent pains likely exist around versioning, trust signals, pricing, and post-launch interpretation
- why the latest signals strengthen it:
  - directory and compatibility policies are getting more explicit
  - ecosystem growth creates more supply-side confusion and more review burden
- likely cheap probes:
  - narrow listing optimizer
  - benchmark-driven launch grader
  - post-launch telemetry interpreter
  - compliance and directory-readiness checker
- search status: `keep digging`
- converted artifacts:
  - assumption: [launch-compliance-intelligence.md](../assumptions/launch-compliance-intelligence.md)
  - probe draft: [launch-compliance-intelligence-manual-offer.md](../probes/drafts/launch-compliance-intelligence-manual-offer.md)

### 2. Tool-surface compression for technical products

- idea:
  - builders increasingly have docs, repos, APIs, and MCP surfaces but still struggle to choose the minimum useful tool surface
- why interesting:
  - this looks like a repeated design bottleneck rather than one product-specific complaint
  - the newest platform/tooling releases make shipping narrow adapters easier, which raises the value of deciding *what not to build*
- likely cheap probes:
  - manual design review offer
  - docs-to-tool-surface MCP assistant
  - allowed-tools recommender
  - MCP server narrowing and tool-governance audit
- search status: `promising`
- converted artifacts:
  - assumption: [tool-surface-compression.md](../assumptions/tool-surface-compression.md)
  - probe draft: [tool-surface-compression-review.md](../probes/drafts/tool-surface-compression-review.md)

### 3. Evaluation and trust tooling for agentic products

- idea:
  - as remote tools normalize, teams need help proving reliability, failure boundaries, and operator trust
- why interesting:
  - strong fit with Skillfoundry's current architecture strengths
  - recent research suggests evaluation gaps remain large even when capability demos look strong
- risk:
  - risk of building meta-infra for ourselves instead of solving buyer pain
- search status: `promising but dangerous`
- converted artifacts:
  - assumption: [agent-evaluation-trust-evidence.md](../assumptions/agent-evaluation-trust-evidence.md)
  - probe draft: [agent-evaluation-trust-review.md](../probes/drafts/agent-evaluation-trust-review.md)

### 4. Tool-governance and approval policy products

- idea:
  - as remote MCP becomes normal, teams will need help deciding what tools to expose, what should require approval, and what should be excluded entirely
- why interesting:
  - this is a real policy and operating problem reflected in official docs, not just a speculative architecture concern
  - likely easier to sell as trust and cost control than as abstract agent infrastructure
- risk:
  - could collapse into generic security theater if not tied to a real workflow
- search status: `promising`

### 5. Workflow-specific wrappers around suddenly-cheap agent capabilities

- idea:
  - new platform support may make many small workflow wrappers viable
- why interesting:
  - lower build cost can support broader Stage 1 exploration
- risk:
  - easy to overproduce wrappers with no durable demand
- search status: `good spray area, low confidence`

### 6. Voice and real-time agent operations

- idea:
  - production voice agents and SIP support create new ops and QA pain
- why interesting:
  - likely adjacent to trust, compliance, and observability needs
- risk:
  - may be too far from current Skillfoundry edge and buyer access
- search status: `interesting but not first`

### 7. Interruption-compression and agent-manager workflows

- idea:
  - if workers are drowning in pings, meetings, and fragmented agent workflows, there may be demand for narrow products that compress decision overhead rather than automate full jobs
- why interesting:
  - macro trend evidence is strong
  - fits with small operational copilots, triage layers, and exception managers
- risk:
  - broad productivity categories are noisy and crowded
- search status: `worth narrowing`

## Search Methods: What Worked

- official announcement plus docs scanning:
  - best for identifying substrate changes that make probes cheaper
- policy-page scanning:
  - unexpectedly strong for finding friction-shaped opportunities because standards imply where builders will fail
- direct live-surface checks:
  - best for grounding claims about channel and operational status
- cross-checking trend articles against official platform changes:
  - good for separating hype from actual capability movement
- benchmark-paper scanning:
  - good for identifying where capability progress is overstated and where trust tooling may be more viable than full autonomy

## Search Methods: What Did Not Yet Work

- broad generic trend searches:
  - too much repetition, not enough pain
- unbounded market-opportunity phrasing:
  - returns hot takes, not buildable assumptions
- research-first search without commercial framing:
  - finds capability novelty but not reachable buyers
- latest-news-only scanning:
  - good for recency, weak for repeatable bottleneck detection unless paired with policy pages, docs, or direct user complaints

## Next Searches To Run

- look for repeated complaints from MCP builders after listing or launch, not just before launch
- look for signals around agent evaluation and trust from teams actually deploying internal agents
- scan recent research specifically for capabilities that reduce the cost of narrow commercial probes
- compare marketplace surfaces to find repeated weak spots in packaging, trust, and activation
- search support and policy surfaces for MCP directories, SDKs, and hosted-agent platforms because they reveal forced constraints before users describe them cleanly
- search for explicit user complaints around post-launch MCP operations, not just build and launch

## Concrete Outputs From This Pass

- shortlist note:
  - [2026-04-11-shortlist-from-idea-hunt.md](../assumptions/2026-04-11-shortlist-from-idea-hunt.md)
- assumptions:
  - [launch-compliance-intelligence.md](../assumptions/launch-compliance-intelligence.md)
  - [tool-surface-compression.md](../assumptions/tool-surface-compression.md)
  - [agent-evaluation-trust-evidence.md](../assumptions/agent-evaluation-trust-evidence.md)
- probe drafts:
  - [launch-compliance-intelligence-manual-offer.md](../probes/drafts/launch-compliance-intelligence-manual-offer.md)
  - [tool-surface-compression-review.md](../probes/drafts/tool-surface-compression-review.md)
  - [agent-evaluation-trust-review.md](../probes/drafts/agent-evaluation-trust-review.md)

## Working Invariants

- keep substrate shifts separate from buyer pain
- do not confuse live deployment with demand
- prefer bottlenecks that can be tested with one narrow external probe
- keep logging the search method, not just the ideas
