# Ranked Bottlenecks

## Ranking Method

Each bottleneck is ranked on:

- pain intensity,
- frequency,
- closeness to our chosen ICP,
- fit for a narrow MCP-native utility,
- speed to first deploy,
- and fit for the current external launch channel once promoted into a product.

## Current Ranking

### 1. Signal-to-opportunity synthesis for MCP builders

Builders can find raw signals everywhere, but turning those signals into ranked,
evidence-backed product opportunities is still slow and noisy.

- pain: high
- frequency: high
- channel fit: high
- build scope: medium
- monetization fit: high

### 2. API docs to minimal MCP tool-surface design

Builders repeatedly struggle to turn large third-party API docs into a safe, narrow,
useful tool surface they can actually ship.

- pain: high
- frequency: medium
- channel fit: high
- build scope: medium
- monetization fit: medium-high

### 3. Marketplace-ready MCP packaging and listing preparation

Many builders can ship a server locally but stall on README quality, example prompts,
pricing, positioning, and marketplace submission hygiene.

- pain: medium-high
- frequency: high
- channel fit: high
- build scope: low-medium
- monetization fit: medium

### 4. OAuth and scope minimization for public API-backed MCP servers

Auth setup remains a real barrier, but it is more episodic and harder to package into
a low-friction first marketplace tool.

- pain: high
- frequency: medium
- channel fit: medium
- build scope: medium-high
- monetization fit: medium

### 5. Post-launch usage interpretation for MCP creators

Understanding which calls, prompts, and users actually create value matters, but this
comes after first launch and depends on data that new creators do not yet have.

- pain: medium
- frequency: medium
- channel fit: medium
- build scope: medium
- monetization fit: medium

## Selected First Internal Mechanism

Build around bottleneck `#1`: signal-to-opportunity synthesis for MCP builders.

Working mechanism name: `bottleneck-radar`

This mechanism should help Skillfoundry identify and shape external product candidates.
It should not be treated as the first monetized product by default.
