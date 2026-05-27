---
name: binary-search-trees
description: Use when reasoning about binary search trees, red-black trees, ordered dynamic sets, predecessor or successor queries, transplant-based deletion, rotations, balance invariants, or production ordered-container choices.
license: MIT
---

# Binary Search Trees

## Overview

Binary search trees are not mainly a recommendation to hand-roll pointer trees. They teach an ordered-set mindset: keep ordering separate from representation, treat height as the operational risk, make local navigation decisions from invariants, and use small pointer rewrites to preserve object identity while changing structure.

When applying this chapter in industrial contexts, answer both questions:

1. What invariant makes the operation correct?
2. What data-shape, identity, duplicate, cache, or library constraint makes the textbook implementation inappropriate or appropriate?

## Shared CLRS Conventions

Also follow the parent `clrs` skill for mathematical formatting, theorem preconditions, proof tone, and chapter-skill routing. Put formal bounds in display LaTeX blocks, not inline prose.

## When to Use

Use this skill for:

- Ordered dictionaries, ordered sets, range scans, predecessor and successor queries, nearest-neighbor-by-key questions, and sorted traversal.
- Basic BST operations: `TREE-SEARCH`, `TREE-MINIMUM`, `TREE-MAXIMUM`, `TREE-SUCCESSOR`, `TREE-PREDECESSOR`, `TREE-INSERT`, `TREE-DELETE`, and `TRANSPLANT`.
- Red-black-tree invariants, rotations, insertion fixup, deletion fixup, and height guarantees.
- Questions asking whether a plain BST, balanced BST, B-tree, skip list, hash table, array, or standard library container is the right production choice.
- Debugging pointer-tree code where the ordering relation is correct but parent links, external handles, rotations, or color/black-height repair are suspicious.

Do not use this skill as the primary guide for:

- Unordered exact lookup with no rank, range, predecessor, or sorted-order need; prefer hash-table reasoning.
- External-memory indexes, storage engines, or database indexes where B-trees or LSM-style structures dominate.
- Full sorting problems unless the point is to contrast inorder traversal with sorting or range enumeration.
- Implementing a production ordered map when the language standard library already provides one and no special invariant is required.

## First Decision: What Ordered-Set Tool Fits?

| Need | Prefer | Why |
| --- | --- | --- |
| Exact lookup only | Hash table | Ordering adds cost and complexity without value. |
| Ordered iteration, predecessor, successor, floor, ceiling, or range scan | Balanced ordered container | These are the ordered-tree strengths, but height must be controlled. |
| Small, fixed, cache-sensitive sorted data | Sorted array plus binary search | Better locality and simpler code than pointer trees. |
| Frequent arbitrary insert/delete with sorted traversal | Library tree, skip list, or B-tree-like container | Use engineered balancing, tested duplicate policies, and allocator behavior. |
| Adversarial, sorted, or externally controlled insertion order | Never plain BST | Height can degrade to a chain. |
| Disk/page/cache-line dominated access | B-tree or cache-aware structure | Pointer-tree teaching models teach invariants, not memory-hierarchy efficiency. |
| Need object handles that remain meaningful | Node-moving deletion or explicit handle semantics | Copying payloads can silently mutate the wrong logical object. |

## BST Quick Reference

Always say that a BST operation costs proportional to height unless a balancing scheme is specified.

$$
O(h)
$$

| Operation | Local rule | Industrial trap |
| --- | --- | --- |
| Search | Compare at current node and take exactly one child path. | This is not logarithmic unless height is bounded. |
| Minimum / maximum | Follow left pointers for minimum, right pointers for maximum. | Fast in balanced trees; linear in a chain. |
| Successor | If right subtree exists, take its minimum; otherwise climb until leaving a left child relation. | Enables ordered iteration without restarting from root. Preserve parent links. |
| Predecessor | Symmetric to successor. | Same parent-link and iterator-validity concerns. |
| Inorder walk | Visit left subtree, node, right subtree. | Gives sorted order, but not a replacement for a production sort pipeline. |
| Insert | Search to the missing child position while remembering the parent, then attach the node. | Preserves order but does not control height. |
| Delete | Use `TRANSPLANT`; with two children, move the successor node into the deleted node's position. | Moving nodes preserves object identity better than copying keys/payloads. |

Inorder traversal visits every node once.

$$
\Theta(n)
$$

## The Core BST Invariant

State the ordering invariant before giving an operation or proof. For every node, keys in the left subtree are at most the node key, and keys in the right subtree are at least the node key. If duplicates are present, state the actual policy; the basic BST property permits equality on either side, but production code must choose a deterministic rule.

Good duplicate policies include:

- Store a count at one node when equal keys are indistinguishable.
- Store a list or bucket of records when one ordering key maps to multiple payloads.
- Use a compound key such as primary key plus stable tie-breaker when iteration must be deterministic.
- Route equals consistently left or right only for educational code, and still analyze the resulting height risk.

## Height Is the Risk, Not the Operation List

Do not write that BST operations are logarithmic unless balance or input randomness is explicit. The correct analysis habit is:

1. Name the operation.
2. Say it follows one downward path, one upward parent-link path, or one traversal.
3. Bind the cost to tree height or node count.
4. Then explain what controls height.

Plain BSTs can be excellent as a concept and terrible as a service dependency. Random-ish insertion may give good average behavior, but sorted insertion, adversarial keys, or skewed duplicate routing can make the tree a chain.

Use this phrasing in production answers: "The textbook BST teaches the invariant and local operation. I would not deploy it directly unless input order and height are controlled; I would use a tested balanced ordered container or a cache-aware index."

## Successor and Predecessor as Local Navigation

For successor and predecessor questions, avoid re-searching from the root unless the data structure lacks parent links. The chapter's insight is that sorted order is encoded locally:

- Right subtree exists: successor is the leftmost node in that right subtree.
- No right subtree: climb until the current node is in the left subtree of an ancestor; that ancestor is the successor.
- Predecessor is the mirror image.

This matters for industrial iteration because it turns "next item in sorted order" into a local operation on an iterator or node handle. Then check whether the implementation guarantees parent links, iterator validity after mutation, and duplicate ordering.

## Deletion: Preserve Identity Before Optimizing Mechanics

Use `TRANSPLANT` as the conceptual boundary between "which node should occupy this position" and "how parent/child pointers are rewired." Deletion cases:

1. No left child: replace the deleted node by its right child.
2. No right child: replace the deleted node by its left child.
3. Two children: choose the successor, the minimum node in the right subtree, and move that successor node into the deleted node's position.

When the successor is not the deleted node's immediate right child:

1. Replace the successor by its own right child.
2. Give the successor the deleted node's right child.
3. Replace the deleted node by the successor.
4. Give the successor the deleted node's left child.

When the successor is the immediate right child, skip the first detach-and-reattach step for the right subtree.

The industrial lesson is stronger than the pseudocode: if external systems hold node pointers, iterators, locks, observers, cache entries, or identity-based handles, copying a successor's key and payload into the deleted node can make the wrong object appear to survive. The transplant-based deletion procedure moves nodes so the removed object is actually removed and the successor object remains itself.

Only copy keys or payloads when the API explicitly treats nodes as invisible storage cells and all external identity is by key/value, not by node object.

## Red-Black Trees: Separate Order from Balance

A red-black tree is a BST plus color and black-height invariants. Keep two debugging tracks separate:

| Symptom | Suspect | Reasoning move |
| --- | --- | --- |
| Inorder traversal is not sorted | BST pointer or rotation bug | Rotation or transplant broke order links. |
| Sorted order is correct but height/color checks fail | Red-black fixup bug | Order is intact; balance metadata was repaired incorrectly. |
| Root is red | Insertion fixup termination bug | The root must be black. |
| Red node has red child | Insert recoloring/rotation case missed | The local red-red violation was not discharged or moved upward. |
| Paths from a node have unequal black counts | Delete fixup or rotation/recolor bug | The extra-black deficit was not moved or eliminated correctly. |

Red-black properties to preserve:

- Every node is red or black.
- The root is black.
- NIL leaves are black.
- Red nodes have black children.
- All simple paths from a node to descendant NIL leaves contain the same number of black nodes.

These properties imply logarithmic height.

$$
h \le 2\lg(n+1)
$$

## Rotations: Local Pointer Rewrite, Global Order Preserved

Use rotations as the key mental model for balanced trees: a rotation changes shape and heights without changing inorder order. It is a constant-time pointer rewrite around two adjacent nodes and three subtrees. Therefore:

- A rotation should not change the sorted sequence of keys.
- A rotation may change parent, child, root, and sentinel links.
- A red-black fixup combines rotations with recoloring to repair balance invariants after a normal BST insert or delete.

When explaining or debugging rotations, name the three ordered regions before and after the rotation. If their inorder concatenation is unchanged, the BST invariant survives; then verify colors and black heights separately.

## Red-Black Insert and Delete Mindset

Insertion:

1. Insert as a normal BST leaf.
2. Color the new node red so black heights are initially unchanged.
3. Repair only possible violations: red root or red parent with red child.
4. If the uncle is red, recolor and move the red-red problem upward.
5. If the uncle is black, rotate and recolor to discharge the problem locally.

Deletion:

1. Do ordinary BST deletion while tracking the original color of the node actually removed from the tree.
2. If a red node was removed, black heights are unchanged.
3. If a black node was removed, model the replacement child as carrying an extra black deficit.
4. Use sibling cases to move the deficit upward, convert cases by rotation, or eliminate the deficit locally.

For production explanations, do not recite every case unless requested. Instead, state what each case is trying to preserve: order from the BST, no red-red edges, and equal black counts on all downward paths.

## One Practical Design Pattern

When reviewing a proposed ordered-set implementation, use this checklist:

1. **Operation need:** Is there a real predecessor, successor, range, min/max, or sorted-iteration requirement?
2. **Height control:** Is balance guaranteed by the data structure, randomized enough for the risk, or absent?
3. **Identity semantics:** Are users holding node handles or iterators, and what happens after delete or rotation?
4. **Duplicate policy:** Are equal keys counted, bucketed, tie-broken, or routed consistently?
5. **Memory behavior:** Is pointer chasing acceptable, or would sorted arrays, B-trees, or library containers be faster and safer?
6. **Mutation contract:** Which operations invalidate iterators, parent links, cached extrema, or external indexes?

If any answer is vague, prefer a standard library or database/index structure over custom pointer-tree code.

## Invariant and Proof Recipes

For BST operation correctness:

1. State the BST property and duplicate policy.
2. Identify the only path or local region the operation changes.
3. Show unchanged subtrees keep their relative order.
4. Show changed parent/child boundaries still separate lower keys from higher keys.
5. Conclude the invariant holds; then analyze height-dependent cost.

For rotations:

1. Name the left region, middle pivot relationship, and right region.
2. Show the inorder sequence is unchanged.
3. Check all parent/root/sentinel pointers affected by the local rewrite.
4. Only after order is preserved, analyze balance metadata.

For red-black height:

1. Use the red-node rule to argue at least every other node on a root-to-leaf path is black.
2. Use equal black count to relate path length to subtree size.
3. Conclude the height bound with the displayed inequality above.

## RED Pressure Failures This Skill Prevents

Baseline agents usually know the textbook operations. This skill exists to prevent subtler failures:

- Saying "BST operations are logarithmic" without first proving or assuming height control.
- Treating BST deletion as just a key-copy trick and ignoring node identity, external handles, and payload mutation.
- Explaining red-black cases as memorized mechanics instead of separating order invariants from black-height repair.
- Recommending hand-rolled pointer trees when a standard ordered map, B-tree, skip list, sorted array, or hash table better matches production constraints.
- Omitting duplicate-key policy even though equality handling changes shape, iteration determinism, and worst-case height.
- Forgetting that rotations preserve inorder order but still must update parent, root, and sentinel links.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| "A BST gives logarithmic operations." | Say operations cost by height; only balanced or probabilistically controlled height gives logarithmic behavior. |
| "Just copy the successor into the deleted node." | Safe only when node identity is invisible; otherwise move nodes or define handle invalidation explicitly. |
| "Duplicates can go anywhere." | Pick and document count, bucket, tie-breaker, or routing policy. |
| "Rotation fixes ordering." | Rotation preserves ordering; it fixes shape/balance when paired with the right metadata updates. |
| "Red-black insert/delete is a list of cases to memorize." | Explain the invariant being repaired: red-red for insert, black-height deficit for delete. |
| "Inorder traversal sorts the data, so use it as a sort." | It emits sorted order from an already-built ordered structure; building and maintaining that structure has its own costs. |
| "Pointer-tree teaching implementations are good default production indexes." | They are teaching models; prefer engineered containers unless the custom invariants justify implementation and testing cost. |

## Verification Pressure Tests

Use these prompts to check whether this skill is working:

1. "A teammate says our plain BST map has logarithmic lookup because search halves the remaining tree. Correct them and recommend a production-safe alternative."
2. "We delete a node with two children by copying its successor's key and payload. What can go wrong if clients hold node handles? Give the transplant-based fix."
3. "A red-black-tree bug preserves sorted inorder traversal but violates black heights. How should we debug it?"
4. "Choose between hash table, plain BST, red-black tree, sorted array, and B-tree for a workload with exact lookup, range scans, duplicates, and cache-sensitive reads."
5. "Explain successor and predecessor without restarting search from the root, and state the parent-link assumption."

Static checks for this skill:

- `SKILL.md` lives at `clrs/binary-search-trees/SKILL.md`.
- Frontmatter name is `binary-search-trees` and description starts with `Use when`.
- The parent `clrs` skill lists this chapter skill.
- Formal bounds are displayed in LaTeX blocks, not embedded in prose.
- The text distinguishes textbook mechanics from production container choice.
