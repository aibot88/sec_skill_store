---
name: kvcache-format
description: Paged KV cache page-out / page-in format used by pf-cache. Reference for vLLM and SGLang adapter authors.
---

# KV-cache page format

See `agent_docs/cache-layer.md` for the full spec. Cheat sheet:

## On-GPU page

A page is a contiguous `[n_layers, page_size_tokens, n_heads, head_dim]`
tensor for K, plus the same shape for V. Stored in vLLM's `gpu_cache` as a
list of `(K_page, V_page)` pairs indexed by physical-page id.

## Page-out

```
for phys_pid in occupied_pages:
    K, V = read_page(phys_pid)              # GPU → pinned host buffer
    digest = sha256(K.bytes() ‖ V.bytes())  # one digest per (K,V) pair
    if not blob_store.contains(digest):
        compressed = zstd_19(K.bytes() ‖ V.bytes())
        blob_store.put_with_digest(compressed, digest)
    page_table[phys_pid] = digest
emit_manifest({page_size_tokens, n_layers, n_heads, head_dim, dtype, pages: page_table})
```

## Page-in

```
manifest = read_manifest(cid)
for phys_pid, digest in zip(allocate_pages(len(manifest.pages)), manifest.pages):
    compressed = blob_store.get(digest)
    K_bytes, V_bytes = split(zstd_decompress(compressed))
    write_page(phys_pid, K_bytes, V_bytes)  # pinned → GPU
patch_logical_seq_table(manifest.logical_seqs)
```

## Logical sequences

vLLM tracks per-request logical-seq → physical-page mappings. We serialize
that mapping into `logical_seqs[]` so restore can rebuild request-level
prefix-sharing exactly.

## Bit-exactness

Requires the engine started with batch-invariant kernels (vLLM
`--enforce-deterministic`, SGLang `--deterministic-mode`). Otherwise restore
will produce numerically equivalent but not bit-equal logits.
