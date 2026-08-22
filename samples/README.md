# Samples

Fifty records per type, committed so that a reader can see the shape of this
pack's output without minting anything.

These regenerate exactly:

```bash
mintmark mint --pack . --recipe portfolio-baseline --seed 1 \
  --records policyholder=50 --records policy=50 --records claim=50 \
  --records payment=50 --records claim_note=50 \
  --records call_transcript=50 \
  --out ./regenerated
```

A test compares the committed files against a fresh run by digest, so a sample
that drifts from the declarations fails the build rather than quietly
misrepresenting them.

These are samples, not a dataset. They carry no manifest, so nothing binds them
to what produced them. The reference datasets, which do carry manifests and
checksums, are published as release artifacts and never committed here.
