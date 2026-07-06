# Workflow

## Intake

- Record the RPC URL, chain ID, player wallet, target contract addresses, ABI or source files, and the exact win condition.
- Read the current `steps.md` before interacting so you inherit prior state reads, helper deployments, failed transactions, and current open hypotheses.
- Keep transient traces, decoded calldata, and fork-specific notes under `_artifacts/`. Keep final `solve*`, helper contracts, `steps.md`, and `wp.md` at the challenge root.

## Strong Signals

- Solidity or Vyper source, ABI JSON, deployed address list, private key, or Foundry project
- Bytecode-only contracts, selector tables, storage dumps, or transaction traces
- ERC20, ERC721, ERC1155, proxy, vault, AMM, flash-loan, governance, bridge, or permit language
- RPC methods, event logs, calldata, `delegatecall`, `selfdestruct`, `tx.origin`, or `CREATE2`

## Common Exploit Families

- Access control or initializer mistakes
- Reentrancy or callback misuse
- Proxy or delegatecall storage confusion
- Signature replay, permit misuse, or nonce handling bugs
- Oracle or price manipulation
- Accounting drift, share inflation, rounding abuse, or insolvency
- Storage-slot writes, arbitrary call surfaces, or unsafe upgrade paths
- Bytecode puzzles where the selector map or storage layout is the real challenge

## Proof Discipline

- Prefer read-only verification first: `eth_call`, storage reads, event review, or forked simulation.
- Prove one state transition or one invariant break before attempting the full exploit chain.
- Keep exact calldata, sender assumptions, and block-sensitive dependencies explicit in notes or code.
- If a later session disproves an earlier path, append the correction to `steps.md` rather than rewriting history.

## Multi-Session Handoff

- Record helper-contract addresses, deployment tx hashes, funded accounts, allowances, and any manipulated state another session must know.
- Note whether a local fork, anvil instance, or replay environment exists and whether it should be restarted cleanly.
- Before leaving, add the current strongest exploit hypothesis, what has been proven on-chain, and the next bounded action.
