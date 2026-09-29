# AI Challenge Workflow

## 1. Interaction-Model Triage

Identify which shape the challenge has before choosing techniques:

| Shape | Strong signals | First move |
|---|---|---|
| Black-box chat | Web UI or completion API, win condition is model output | Probe for system-prompt leakage and delimiters |
| Agent with tools | Tool schemas, function calling, "bot can use X" | Enumerate tools, find flag-reachable ones |
| Model artifact | `.pt` `.pth` `.pkl` `.ckpt` `.safetensors` `.onnx` `.gguf` `.h5` | Static inspection; never load pickles blindly |
| Adversarial ML | Perturbation budget, classifier accuracy target | Determine white-box vs black-box, metric |
| Data recovery | Model inversion, membership inference, leakage wording | Inspect what the challenge exposes (logits, embeddings) |

## 2. Prompt Injection Discipline

- Direct injection: instructions in user input that override the system prompt.
- Indirect injection: hostile instructions arriving through retrieved documents, tool outputs, web pages, or filenames the model reads.
- System-prompt extraction: delimiter confusion, "repeat the above", encoding requests, roleplay reframing.
- Output-filter evasion: Unicode homoglyphs, translations, base64 or rot13 framing, splitting the flag across turns, asking for a poem/acrostic.
- Multi-turn: build trust in early turns, then escalate; some guards only trigger on single-turn patterns.
- Keep a payload matrix (`goal -> payload -> result`) so a later session never reruns a dead payload.

## 3. Agent and Tool Abuse

- Enumerate every tool and its arguments; look for tools that read files, fetch URLs, execute code, or touch the flag directly.
- Excessive agency: can the model be talked into calling the flag tool "for debugging"?
- Chain hops: inject through one tool's output (indirect injection) so the model calls another tool with attacker-controlled arguments.
- If the agent browses, remember SSRF-style reasoning applies to what it can be steered to fetch.

## 4. Model Artifact Analysis

- Pickled formats (`.pt` `.pth` `.pkl` `.ckpt`):
  - Inspect with `pickletools.dis` before anything else; look for `__reduce__`, `os.system`, `eval`, suspicious globals.
  - A pickle gadget chain is often the intended solve (code execution on load) — extract it statically.
  - If flags hide in tensors, parse the zip/protobuf container directly instead of importing the framework.
- `safetensors` / `ONNX` / `GGUF`: metadata inspection first; look for hidden strings in metadata, tokenizer merges, or quantized weight anomalies.
- Weight stego: compare against the published upstream weights when the base model is identifiable; diffs often carry the payload.
- Sandbox rule: loading anything pickle-based happens only in a disposable environment and only after the user agrees.

## 5. Adversarial Inputs

- White-box: use gradients (PGD / FGSM variants) under the stated budget and metric.
- Black-box: transfer attacks from a local surrogate, or query-efficient methods if a query budget exists.
- Check the win condition precisely: top-1 flip, target-class misclassification, or confidence threshold — each changes the objective.

## 6. Logging and Handoff

- Every payload attempt goes into `steps.md` as goal, payload, and observed result.
- Record endpoint behavior changes (guards tightening after attempts) — they change the next strategy.
- Final solve script keeps exact prompts, parameters, and decoding steps so the path replays end to end.
