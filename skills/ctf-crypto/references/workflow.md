# Workflow

## Primitive Identification

- Look at alphabet, block sizes, modulus sizes, separators, and metadata.
- Distinguish encoding, compression, and serialization from actual crypto.

## Common Weakness Families

- RSA with shared primes, low exponent, bad padding assumptions, or leaked relations
- ECDSA or Schnorr with nonce reuse or partial nonce leakage
- XOR or stream constructions with key reuse
- Block modes with IV misuse or oracle behavior
- Custom schemes that reduce to linear algebra or modular equations

## Proof Discipline

- Recover one intermediate or one small plaintext fragment first.
- Make each assumption explicit in code or notes.
- Prefer a short solver that demonstrates the weakness over long symbolic exposition.
