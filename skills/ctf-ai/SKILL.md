---
name: ctf-ai
description: Use when a CTF challenge centers on AI or LLM security rather than a conventional web, crypto, or reverse-only path. Best for tasks involving chat endpoints or LLM APIs, system prompt extraction, direct or indirect prompt injection, jailbreaks, guardrail or output-filter bypass, AI agent tool abuse, RAG poisoning, data exfiltration through model output, adversarial examples against classifiers, model inversion or membership inference, and local model artifacts such as PyTorch pickles, safetensors, ONNX, GGUF, or Keras files inside a controlled CTF environment.
---

# CTF AI

## Overview

Treat AI challenges as interaction-model exploits. First identify what you are facing (black-box LLM endpoint, agent with tools, local model artifact, or adversarial-ML target), then pick the smallest payload or analysis step that changes the model's behavior decisively, and finally script the reproducible solve path.

## Use This Skill For

- Challenge text mentions an LLM bot, chat assistant, AI agent, guardrail, safety filter, or "make the model reveal X" win conditions.
- The target is an API endpoint serving a model, or a web UI wrapping one.
- Supplied files are model artifacts: `.pt` / `.pth` / `.pkl` / `.ckpt` (pickled), `.safetensors`, `.onnx`, `.gguf`, `.h5`, or exported pipelines.
- The task is adversarial ML: craft an input within a perturbation budget to fool a classifier, or recover training data.
- The challenge hides a flag inside weights, tokenizer data, embedded prompts, or model metadata.

## Workflow

1. Normalize the target.
   Capture the endpoint or files, available keys or quotas, the exact win condition (say the flag, leak the system prompt, exfiltrate a secret, misclassify an input, recover data), rate limits, and what the user already tried.
   Read any existing `steps.md` before new probing so the session inherits prior payloads, leaked fragments, and failed attempts.
2. Fingerprint the interaction model.
   - Black-box chat: probe for system-prompt leakage, delimiters, tool availability, output filtering.
   - Agent: enumerate the tool list, note which tools touch flags, files, or network (excessive agency).
   - Artifact: identify the serialization format and its loading risks before touching anything.
   - Adversarial ML: determine white-box (gradients available) vs black-box (query budget) and the constraint metric.
3. State one hypothesis.
   Pick one exploit family: direct prompt injection, indirect injection through retrieved/tool content, system-prompt extraction, output-filter evasion, tool abuse, insecure deserialization, weight stego, or adversarial optimization.
4. Prove with one payload.
   Run a single decisive attempt that observably changes behavior (a leaked token, an executed tool, a flipped label). Avoid spraying dozens of payloads without recording results.
5. Iterate with a payload log.
   Keep every attempt as `goal -> payload -> result` in `steps.md`. Reuse encodings, languages, roleplay framings, or multi-turn setups that worked once.
6. Script the solve.
   Reduce the winning path to a minimal reproducible script (request sequence or artifact-processing code) with the exact prompts and parameters.
7. Contain scratch artifacts.
   Put response dumps, decoded tensors, trial images, and intermediate payloads under `<challenge>/.cache/`. Keep the final solve script, decisive evidence, `steps.md`, and `wp.md` at the challenge root.

## Guardrails

- Work only on authorized CTF, lab, or training endpoints and artifacts.
- **Never blindly unpickle untrusted model files.** `.pt` / `.pth` / `.pkl` / `.ckpt` can execute arbitrary code on load. Statically inspect first (`pickletools`, scanning for `__reduce__` and suspicious globals); if loading is unavoidable, do it in a throwaway sandbox (container or disposable VM) and ask the user before running.
- Keep API keys, tokens, and platform credentials out of logs and writeups; record only that a saved credential was used.
- Respect endpoint rate limits; prefer a few targeted prompts over high-volume fuzzing.
- If the challenge is mostly a web wrapper (auth, upload, SSRF around the model), hand the web part to `$ctf-web`.
- If the core work becomes reversing a serialization format or custom container, pair with `$ctf-reverse`.
- If the challenge is evidence-driven over AI artifacts (memory dumps of inference servers, logs), pair with `$ctf-forensics`.

## Reference Routing

- For interaction-model triage, payload families, and artifact analysis details, read [references/workflow.md](references/workflow.md).
- Pair with `$ctf-web` when a web surface (session, upload, API auth) guards the model.
- Pair with `$ctf-reverse` for model-format reversing, embedded VMs in loaders, or obfuscated pickles.
- Pair with `$ctf-forensics` when artifacts and traces dominate over live interaction.

## Output Expectations

- Report the interaction model, the suspected exploit family, the minimal proof, and the scripted solve path.
- Keep the payload log decision-oriented: attempts that changed the next move, not every 400 response.
- Before pausing or ending, append a `steps.md` handoff covering leaked fragments, working payload encodings, remaining quota, and the next recommended action.
