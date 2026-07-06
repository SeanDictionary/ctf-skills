# Workflow

## Triage

- Identify the language or runtime.
- Check for packing, compression, or embedded resources.
- Use strings, imports, and obvious references to find the main validation path.

## Core Questions

- Where does input enter?
- Where is it transformed?
- Where is success decided?
- What constants or tables matter?

## Solve Styles

- Static reimplementation when the transform is readable.
- Small runtime trace when static output is unclear.
- Patch-and-observe when a branch gate hides later logic.
- Data extraction when the flag or key is stored and lightly disguised.

## Good Stops

- Once the comparison logic is understood, stop exploring unrelated functions.
- Once the transform is reproduced externally, prefer a clean solver over more reversing.
