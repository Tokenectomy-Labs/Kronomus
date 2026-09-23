# Kronumos: A Cost-Bounded Vertical Bug-Remediation System via Context Surgery and Deterministic Diff Re-Anchoring

**M N Daffa**, Tokenectomy Labs, daffa2555@users.noreply.github.com
Code and run logs: https://github.com/Tokenectomy-Labs/Kronomus
September 2026

*Editing conventions: [TODO: ...] marks a value or decision that must come from your run JSON, training pipeline, or the literature. Numbers not marked [TODO] are taken or recomputed from the original draft. Wilson 95% intervals are used for proportions.*

---

## Abstract

Repository-level automated program repair (APR) is usually addressed with general-purpose agents that spend hundreds of thousands of tokens per issue on multi-turn tool use. We study the opposite end of the design space: a *vertical* system built only for bug remediation. Kronumos combines a LoRA fine-tuned Qwen2.5-Coder-7B-Instruct (4-bit NF4) with components of the Tokenectomy Rust runtime: Tree-sitter traceback pruning, linear-time secret redaction, deterministic unified-diff re-anchoring, and AST syntax pre-validation. It runs under a blind single-turn protocol: no tests or program code are executed during inference, and only structural checks (patch dry-run application and AST parsing) gate the output.

On the full SWE-bench Verified set (500 instances, official Docker harness), Kronumos resolves 10 instances (2.0%; 95% Wilson CI 1.1%-3.6%). Of the 79 patches it submitted, 10 resolve the issue (12.66% precision); on the remaining 421 instances (84.2%) no candidate passed validation and the system emitted an empty patch. The average prompt is 3,009.3 tokens, a 92.2% reduction from the unpruned 38,412-token context, at $0 marginal API cost on Kaggle T4 GPUs. Compared with unanchored raw model output (347 diffs, 0 applicable), re-anchoring yields 79/79 applicable patches, showing that deterministic patch construction is a prerequisite for small-model APR. We position these results as an efficiency and safety baseline for vertical APR, not as competitive with interactive agents, and describe Kronumos v2, which adds test feedback under anti-overfitting guards.

---

## 1 Introduction

Resolving a real GitHub issue requires an agent to localize a fault in a large repository, write an edit that is exact at the character level, and leave existing behavior intact. SWE-bench and its human-validated subset SWE-bench Verified [4] made this task measurable, and interactive agents such as SWE-agent [11] and OpenHands [10] now reach substantially higher resolve rates than single-pass models by executing code and iterating on feedback. That capability comes with many shell interactions and large token budgets per issue [TODO: cite exact figures and sources for each system].

Bug remediation, however, is a narrow task with a predictable input: an issue description, a failing trace, and a target file. We argue that much of the cost and risk in this setting is not semantic and can be handled by deterministic code rather than by a larger model or a longer loop. We observe four recurring problems, each addressed by a Kronumos component:

1. **Context noise.** Raw tracebacks are dominated by framework and library frames. Pruning them shrinks the prompt without removing the frames that carry the fault [6].
2. **Credential exposure.** Traces can contain tokens, connection strings, and keys. Redaction must run before any text reaches a model, and it must not be vulnerable to regex backtracking.
3. **Patch-format failure.** Generative models often produce unified diffs with wrong hunk headers or invented paths, so `patch` fails before any test runs. Headers and offsets are arithmetic, not language, and can be computed exactly.
4. **Unsafe failure modes.** An invalid diff should never leave a workspace dirty. When no candidate validates, the system should return an empty patch.

**Kronumos.** Kronumos is a vertical bug-remediation system, not a general-purpose coding agent. It is built on the Tokenectomy ecosystem (Table 1) and pairs a fine-tuned 7B model (the only neural component) with deterministic Rust components that prepare the prompt and construct and validate the patch. We call this split the *Dual-Cortex* architecture: semantic reasoning in the model, mechanics in the runtime.

**Table 1: Relationship between Kronumos and the Tokenectomy ecosystem.** *Tier assignments are placeholders and must be confirmed against the tagged release used for the benchmark.*

| Function | Tokenectomy tier [TODO: confirm] | Kronumos v1 (this paper) | Kronumos v2 |
|---|---|---|---|
| Tree-sitter traceback pruning | Razor (OSS) | Yes | Yes |
| Linear-time secret redaction | Razor (OSS) | Yes | Yes |
| Path grounding, diff re-anchoring, patch dry-run | [TODO: Sentinel / Sovereign] | Yes | Yes |
| AST syntax pre-validation | [TODO: Sentinel / Sovereign] | Yes | Yes |
| Anti-overfitting guards (assertion stripping, lazy deletion, domain narrowing) | Sovereign | No | Yes |
| Bounded retry FSM with circuit breaker (max 3 turns) | Sovereign | No | Yes |
| Zero-LLM symbolic repair for simple regressions | Sovereign | No | Optional |
| Branch, commit, and PR automation | Tokenectomy Git | No (deployment only) | Yes |

Tokenectomy release used: [TODO: version / commit hash]. The only model is Qwen2.5-Coder-7B-Instruct with a LoRA adapter.

**Scope and non-claims.** We evaluate under a blind single-turn protocol in which no tests or program code are executed during inference. The patch dry-run and the Tree-sitter parse are structural checks and do not observe program behavior. Results are therefore not comparable to interactive agents, and we do not claim state-of-the-art performance. Comparisons to single-turn results reported in [4] are indicative only, because they use a different benchmark split and retrieval setting. The closest systems in spirit are pipeline-style, non-agentic approaches such as Agentless [12] and AutoCodeRover [13], which we plan to use as baselines in future work.

**Contributions.**

- A vertical remediation system that couples a 7B model with deterministic context pruning, secret redaction, and patch construction, run at $0 marginal API cost and 3,009.3 prompt tokens per instance on average.
- A formalization of gated abstention (the Zero Dirty Diff invariant): the system returns an empty patch unless a candidate passes path grounding, anchoring, dry-run application, and AST validation.
- An empirical study on all 500 SWE-bench Verified instances (10 resolved, 2.0%, 95% CI 1.1%-3.6%; 12.66% precision on 79 submissions) with per-repository results and five resolved case studies.
- An ablation of the two Sub-Cortex effects (context pruning and patch re-anchoring), including fairer alternatives to re-anchoring.
- A path to v2, where test-feedback iteration is combined with anti-overfitting guards so that additional turns do not reward patches that only satisfy the visible tests.

---

## 2 System Architecture

### 2.1 Surgical intervention

The design follows a distinction between *Chronos* (open-ended, sequential iteration) and *Kairos* (a decisive, minimal intervention). Interactive agents search over many turns; Kronumos formulates one minimal transformation per issue and abstains when it cannot validate it.

```
RAW CONTEXT: failing traceback + issue (mean 38,412 tokens)
        |
        v
TOKENECTOMY SUB-CORTEX (Rust)
  [1] Tree-sitter frame boundary filter (prunes framework/library frames)
  [2] Linear-time secret redaction (JWT, Bearer, AWS key, DB URI, private key)
        |
        v
PRUNED PROMPT (mean 3,009 tokens)
        |
        v
COGNITIVE CORTEX: Qwen2.5-Coder-7B-Instruct + LoRA (NF4), single turn
        |
        v
RE-ANCHORING AND VALIDATION GATE
  [3] Path grounding (reject paths not in the repository)
  [4] Substring alignment and line-offset computation
  [5] Unified-diff header synthesis
  [6] Patch dry-run
  [7] AST pre-validation (reject ERROR nodes)
        |
   valid |            | invalid
        v            v
  SUBMIT PATCH    EMPTY PATCH (Zero Dirty Diff)
```
**Figure 1:** Dual-Cortex architecture. Token counts are per-instance means from the benchmark run.

### 2.2 Dual-Cortex decoupling

1. **Cognitive Cortex (neural):** a LoRA fine-tuned Qwen2.5-Coder-7B-Instruct loaded in 4-bit NormalFloat. It performs semantic code understanding, fault localization within the given file, and replacement-chunk synthesis.
2. **Sub-Cortex (deterministic):** the Tokenectomy runtime in Rust. It performs traceback parsing, secret redaction, offset computation, diff-header formatting, and validation.

### 2.3 Machine-to-machine interface

Tokenectomy is invoked by agents through JSON-RPC 2.0 over stdio rather than as a human-facing CLI. It operates on raw byte slices (`&[u8]`) and targets low, predictable latency [TODO: report measured Sub-Cortex latency and allocation behavior from `stress_benchmark`, or drop the "< 5 ms" and "zero allocation" claims].

---

## 3 Problem Formulation

Let a repository $R = \{f_1, \dots, f_M\}$ at commit $c_0$ have an issue description $I$ and a test suite $T = T_{fail} \cup T_{pass}$ with $T_{fail} \cap T_{pass} = \emptyset$, where every $t \in T_{fail}$ fails and every $t \in T_{pass}$ passes on $R$.

A patch is a sequence of hunks $P = \{(f_k, S_k, L^{(k)}_{orig}, L^{(k)}_{repl})\}_{k=1}^{K}$ (target path, start line, removed lines, added lines), applied by the operator $R' = R \oplus P$. A patch is correct for the benchmark if:

- $\forall t \in T_{fail}: t(R \oplus P) = \text{PASS}$ (defect resolution)
- $\forall t \in T_{pass}: t(R \oplus P) = \text{PASS}$ (regression invariance)
- $\lVert P \rVert_0 = \sum_k (|L^{(k)}_{orig}| + |L^{(k)}_{repl}|) \le \kappa$ (locality) [TODO: state $\kappa$ if the gate enforces it; otherwise present locality as a design preference, not a constraint]

**Zero Dirty Diff invariant.** Define the gated abstention function

$$\Phi(P, R) = \begin{cases} P & \text{if Validate}(P, R) = \text{TRUE} \\ \epsilon & \text{otherwise} \end{cases}$$

where $\epsilon$ is the empty patch, so that $R \oplus \epsilon = R$. Under invalid or unanchored output the workspace is never modified. Note that Validate checks structure (path, anchoring, applicability, syntax), not correctness; a validated patch can still fail the tests.

---

## 4 The Tokenectomy Sub-Cortex

### 4.1 Traceback frame pruning

Let a traceback be $T_{raw} = (F_1, \dots, F_D)$ with frames $F_i = (path_i, line_i, func_i, code_i)$. A boundary classifier $\Psi$ labels a frame FRAMEWORK if its path matches a vendor set $B_{vendor}$ (e.g. `site-packages`, `node_modules`, `.cargo/registry` [TODO: list the full set]) and USER_SPACE otherwise.

**Algorithm 1: Traceback frame pruning.** Input: $T_{raw}$, repository tree $R$. Output: $T_{pruned}$.

1. $T_{pruned} \leftarrow [F_1]$ (keep the entry point).
2. For $i = 2, \dots, D-1$: if $\Psi(path_i) = $ USER_SPACE or $path_i \in R$, append $F_i$; else if $\Psi(path_{i-1}) \ne \Psi(path_i)$, append $F_i$ (keep boundary transitions).
3. Append $F_D$ (keep the leaf exception site). Return $T_{pruned}$.

Consecutive framework frames are dropped, while the entry frame, boundary transitions, and the exception site are preserved. Across the benchmark, the mean prompt shrinks from 38,412 to 3,009.3 tokens (-92.2%) [TODO: state that the 38,412 figure is the mean of the raw issue + traceback + file context and how tokens are counted]. Pruning is evaluated only by its downstream effect (Table 4); we do not measure whether the excised frames ever contained the fault [TODO: optional check].

### 4.2 Secret redaction

Issue text and tracebacks may contain credentials. Kronumos redacts five classes (JWT, Bearer token, AWS access key, database URI, private key block) using automata-based matching (Rust's regex engine and Aho-Corasick) rather than backtracking, so matching time is linear in the input length for a fixed pattern set and inputs cannot trigger exponential blowup. Matches are replaced with fixed placeholders (e.g. `[REDACTED_TOKEN]`) before any model call. Coverage is limited to these five classes, and recall was [TODO: measured on a synthetic secret-injection set / not measured].

### 4.3 Deterministic re-anchoring

Models often emit unified diffs whose hunk headers or line offsets are wrong (for example `@@ -96,7 +96,7 @@` when the target code starts at line 98), causing `patch` to reject the hunk. The Sub-Cortex therefore takes only the model's replacement blocks and constructs the diff itself.

**Algorithm 2: Deterministic re-anchoring.** Input: raw candidate $H_{raw}$, repository $R$. Output: patch $P_{valid}$ or $\epsilon$.

1. Extract the target path $f_{target}$ and the original/replacement blocks $B_{orig}$, $B_{repl}$ from $H_{raw}$.
2. If $f_{target} \notin R$, return $\epsilon$ (hallucinated path).
3. Read the file content $C$. Find the exact byte offset $\Omega$ of $B_{orig}$ in $C$; if absent, try a whitespace-tolerant alignment; if still absent, return $\epsilon$ (context mismatch).
4. $L_{start} \leftarrow$ (number of newlines in $C[0..\Omega]$) + 1; $N_{orig}, N_{repl} \leftarrow$ line counts of $B_{orig}, B_{repl}$.
5. Emit the header `@@ -L_start,N_orig +L_start,N_repl @@` and assemble the patch.
6. Run a patch dry-run against $R$ (`git apply --check` [TODO: confirm; earlier text also cited `patch -p1`]). Return $P$ on success, else $\epsilon$.

### 4.4 AST pre-validation

The patched file is parsed with Tree-sitter. If the tree contains an ERROR node (unbalanced brackets, indentation errors, unclosed literals), the patch is discarded and $\epsilon$ is returned, so syntactically broken code is never submitted.

---

## 5 Model and Fine-Tuning

### 5.1 Base model and quantization

The base model is Qwen2.5-Coder-7B-Instruct [3] (7.61B parameters; RoPE, SwiGLU, grouped-query attention), loaded in 4-bit NormalFloat (NF4) via bitsandbytes to fit on two 16 GB Tesla T4 GPUs.

### 5.2 LoRA and loss masking

Low-rank adapters [2] ($r = 16$, $\alpha = 32$) are injected into all attention and MLP projections. The loss is computed only over the patch tokens, masking the prompt:

$$\mathcal{L}(\theta) = -\sum_{j=1}^{V} \log P_\theta(y_j \mid x_1, \dots, x_U, y_1, \dots, y_{j-1})$$

**Table 2: Fine-tuning hyperparameters.**

| Parameter | Value |
|---|---|
| Base model | Qwen2.5-Coder-7B-Instruct |
| Precision | 4-bit NormalFloat (NF4) |
| LoRA rank / alpha | 16 / 32 |
| Target projections | q, k, v, o, gate, up, down |
| Trainable parameters | 40.89M (0.54% of base) |
| Optimizer | Paged AdamW (8-bit) |
| Learning rate / schedule | 2.0e-4, cosine annealing, 5% warmup |
| Weight decay | 0.01 |
| Effective batch size | 16 (gradient accumulation 4) |
| Max context | 4,096 tokens |
| Hardware | Dual Tesla T4 (Kaggle) |
| Marginal training cost | $0.00 (excludes free-tier GPU quota) |

### 5.3 Prompt representation

The prompt uses XML-style delimiters: a `<system>` instruction, `<issue_description>` (redacted), `<diagnostics>` (pruned traceback), and `<source_file path="...">` (target code section). [TODO: state how the code section is cut to fit the 4,096-token window, since the raw baseline context (38,412 tokens) exceeds the training window.]

### 5.4 Training data and decontamination [TODO: fill from your pipeline]

The model was fine-tuned on [N] (issue, file context, patch) examples from [source], collected between [dates] and built by [method]. To prevent train-test leakage, we removed every example whose instance ID, repository-commit pair, or patch (exact or near-duplicate under [method, threshold]) matches any of the 500 SWE-bench Verified instances; [K] examples were removed. [N_overlap] training repositories also appear among the 12 Verified repositories. We cannot exclude that Qwen2.5-Coder's pre-training data contains public GitHub issues and fixes overlapping the benchmark; results should be read as an upper bound on generalization to unseen issues, and evaluation on post-cutoff issues is future work.

---

## 6 Experimental Setup

### 6.1 Benchmark

We evaluate on all 500 instances of SWE-bench Verified [4], covering 12 Python repositories, using the official Docker harness (`swebench.harness.run_evaluation`, [TODO: harness version]). Verified instances were human-reviewed for well-specified issues and reliable tests.

### 6.2 Blind single-turn, zero-execution protocol

During inference the system does not execute repository code, tests, or any interpreter, and receives no runtime feedback. The model produces one candidate patch per instance [TODO: decoding settings (greedy or temperature), max new tokens, seed, number of runs]. Two structural checks are applied to that candidate: a patch dry-run and a Tree-sitter parse of the patched file. These do not observe program behavior, but they can reject a candidate, so we report their effect separately (Table 5).

### 6.3 Input construction and file provenance [TODO: keep exactly one variant]

**Variant A (retrieval).** The target file in `<source_file>` is selected by [method, e.g. BM25 over repository files or traceback-derived path] without access to the gold patch. File-level top-1 localization accuracy is [X]%.

**Variant B (oracle files).** The target file(s) are the files edited by the reference patch (an oracle-file setting). File-level localization is therefore given, and results are not comparable to systems that localize files themselves. Line-level localization and the edit remain the model's task.

### 6.4 Reproducibility

Harness version and commit, Docker image tags, Tokenectomy version, model and adapter checkpoint hashes, GPU type, and the run file (`Kronumos-7B.kronumos_run.json`): [TODO: fill].

---

## 7 Results

### 7.1 Main results

**Table 3: Official results on SWE-bench Verified (N = 500).**

| Metric | Baseline run (raw context, raw diff) | Kronumos v1 (pruned context, re-anchored) |
|---|---|---|
| Instances | 500 | 500 |
| Candidates | 347 raw diffs | 79 validated patches submitted |
| Submission rate | 347/500 (69.4%) | 79/500 (15.8%) |
| Patch applies | 0/347 (0.0%) | 79/79 (100.0%) |
| Resolved | 0/500 (0.0%) | 10/500 (2.0%) [95% CI 1.1-3.6] |
| Precision (resolved / submitted) | 0/347 (0.0%) | 10/79 (12.66%) [95% CI 7.0-21.8] |
| Instances with empty patch | n/a | 421/500 (84.2%) |
| Mean prompt tokens | 38,412 | 3,009.3 (-92.2%) |
| Mean latency / instance | 312.4 s | 43.60 s (-86.0%) [TODO: define what is timed] |
| Marginal API cost | $0.00 | $0.00 |
| GPU time per resolved issue | n/a | about 36.3 min (500 x 43.60 s / 10), dual T4 |

The 100% apply rate reflects the validation gate: every submitted patch applies by construction, so it measures the gate, not the model. Kronumos submitted a patch for 15.8% of instances, and 12.66% of those resolved the issue. The two runs differ in both prompt and post-processing, so Table 3 alone does not isolate either component; Table 4 does.

### 7.2 Ablation of the Sub-Cortex

**Table 4: 2x2 ablation (context x patch construction).**

| | Raw diff (no re-anchoring) | Re-anchored + gated |
|---|---|---|
| **Raw context (38,412 tok)** | 0/347 apply, 0/500 resolved | [TODO] |
| **Pruned context (3,009 tok)** | [TODO] | 79/79 apply, 10/500 resolved |

We additionally report, on the pruned context, (a) the raw diff repaired by `git apply --recount` and (b) `patch -F3` (fuzz) [TODO], as fairer baselines than an unrepaired diff, together with the fine-tuned model's search/replace output format and the non-fine-tuned base model + Sub-Cortex [TODO]. A raw generative diff with wrong headers failing 347/347 is expected; the informative question is how much of that gap simple existing tools already close.

**Table 5: Origin of the 421 empty patches** [TODO: fill from the run JSON].

| Stage | Count |
|---|---|
| No diff generated | [TODO] |
| Rejected: path not in repository | [TODO] |
| Rejected: search block not found | [TODO] |
| Rejected: dry-run failed | [TODO] |
| Rejected: AST ERROR node | [TODO] |
| **Total** | **421** |

Abstention here means that no candidate passed validation. It reflects generation and validation failure, not calibrated model uncertainty.

### 7.3 Per-repository results

**Table 6: Per-repository results (rows sum to 500).**

| Repository | Total | Submitted | Submit rate | Resolved | Resolve rate | Precision |
|---|---|---|---|---|---|---|
| django/django | 231 | 28 | 12.12% | 5 | 2.16% | 17.86% |
| sympy/sympy | 75 | 18 | 24.00% | 1 | 1.33% | 5.56% |
| sphinx-doc/sphinx | 44 | 2 | 4.55% | 0 | 0.00% | 0.00% |
| matplotlib/matplotlib | 34 | 3 | 8.82% | 0 | 0.00% | 0.00% |
| scikit-learn/scikit-learn | 32 | 9 | 28.13% | 2 | 6.25% | 22.22% |
| pydata/xarray | 22 | 5 | 22.73% | 1 | 4.55% | 20.00% |
| astropy/astropy | 22 | 6 | 27.27% | 0 | 0.00% | 0.00% |
| pytest-dev/pytest | 19 | 3 | 15.79% | 1 | 5.26% | 33.33% |
| pylint-dev/pylint | 10 | 2 | 20.00% | 0 | 0.00% | 0.00% |
| psf/requests | 8 | 3 | 37.50% | 0 | 0.00% | 0.00% |
| mwaskom/seaborn | 2 | 0 | 0.00% | 0 | 0.00% | n/a |
| pallets/flask | 1 | 0 | 0.00% | 0 | 0.00% | n/a |
| **Total** | **500** | **79** | **15.80%** | **10** | **2.00%** | **12.66%** |

Resolved instances fall in five repositories. With 1-5 resolved instances per repository, per-repository rates and precision have very wide confidence intervals (for example pytest, 1/3) and are descriptive only; we do not draw generalization conclusions from them.

### 7.4 Reference points from the literature

**Table 7: Published results in other settings. NOT comparable to Table 3.**

| System | Setting | Reported result | Source |
|---|---|---|---|
| Claude 2 | Original SWE-bench, BM25 retrieval, single-turn | [TODO: exact % from [4]] | [4] |
| GPT-4 | Original SWE-bench, BM25 retrieval, single-turn (subset) | [TODO: exact % and subset size from [4]] | [4] |
| SWE-agent + GPT-4o | Interactive, multi-turn | [TODO: leaderboard entry, split, date] | [11] |
| OpenHands + Claude 3.5 Sonnet | Interactive, multi-turn | [TODO: leaderboard entry, split, date] | [10] |

These systems differ from Kronumos in benchmark split, retrieval, and protocol, and interactive agents execute code during inference. We list them for context only and make no claim of superiority or parity. Cost and token figures for external systems are omitted unless a source reports them [TODO].

### 7.5 Efficiency

Pruning reduces the mean prompt from 38,412 to 3,009.3 tokens (-92.2%), and the full run takes about 6.1 GPU-hours on dual T4 (500 x 43.60 s), or about 36 minutes of GPU time per resolved issue. Marginal API cost is $0; this excludes training compute, free-tier GPU quota, and engineering time.

---

## 8 Case Studies

We present the five resolved instances that we compared against their reference fixes. In each case, the generated patch is shown in the form submitted to the harness. [TODO: verify each diff against the `patch` field in the run JSON.]

**8.1 django__django-15104 (Django).** *Defect:* the migration autodetector removes the `'to'` key from a field's deconstructed kwargs with `del`, which raises `KeyError` when a custom field's `deconstruct()` does not provide it [TODO: verify mechanism against the issue text; the draft described a swapped or removed target model]. *Patch:* replace `del deconstruction[2]['to']` with `deconstruction[2].pop('to', None)`.

```diff
--- a/django/db/migrations/autodetector.py
+++ b/django/db/migrations/autodetector.py
@@ -96,7 +96,7 @@ class MigrationAutodetector:
             if field.remote_field and field.remote_field.model:
-                del deconstruction[2]['to']
+                deconstruction[2].pop('to', None)
```

**8.2 scikit-learn__scikit-learn-[TODO: full ID, likely 10844] (Fowlkes-Mallows).** *Defect:* the score computes $t_k / \sqrt{p_k \cdot q_k}$; for large inputs the product $p_k \cdot q_k$ overflows, giving invalid values. *Patch:* rewrite as $\sqrt{t_k/p_k} \cdot \sqrt{t_k/q_k}$, which is mathematically equivalent and avoids the large product.

```diff
--- a/sklearn/metrics/cluster/supervised.py
+++ b/sklearn/metrics/cluster/supervised.py
-    return tk / np.sqrt(pk * qk) if tk != 0. else 0.
+    return np.sqrt(tk / pk) * np.sqrt(tk / qk) if tk != 0. else 0.
```

**8.3 pydata__xarray-4629 (xarray).** *Defect:* with `combine_attrs="override"`, `merge_attrs` returns a reference to the first object's attrs, so in-place edits of the merged result mutate an input. *Patch:* return a shallow copy.

```diff
--- a/xarray/core/merge.py
+++ b/xarray/core/merge.py
     elif combine_attrs == "override":
-        return variable_attrs[0]
+        return dict(variable_attrs[0])
```

**8.4 pytest-dev__pytest-6202 (pytest).** *Defect:* a string replacement `s.replace(".[", "[")` when building a node's report path corrupts test names that legitimately contain `.[`. *Patch:* remove the replacement and return the joined path unchanged.

```diff
--- a/src/_pytest/python.py
+++ b/src/_pytest/python.py
     s = ".".join(parts)
-    return s.replace(".[", "[")
+    return s
```

**8.5 sympy__sympy-22714 (SymPy).** *Defect:* constructing a `Point2D` under `evaluate(False)` raises "Imaginary coordinates are not permitted" because the imaginary-part check does not handle unevaluated arguments [TODO: verify against the issue]. *Patch:* [TODO: paste the exact patch from the run JSON. The draft's diff added `if evaluate is False: return None` inside `__new__`, which would return `None` from a constructor and is unlikely to be the submitted patch; the reference fix tightens the imaginary-part test itself, and a matching patch would show the same idea.]

**Observation.** Four of the five fixes change one or two lines and correspond closely to the reference fix, which is consistent with the locality preference (Section 3) but also with the small scale of the sample.

---

## 9 Discussion

### 9.1 Single-turn ceiling

Of the 79 submitted patches, 69 applied but failed the benchmark's tests. We manually categorized these [TODO: annotators, criteria, and the share per category; the draft reported 48% attributed to three causes]: off-by-one boundary errors (e.g. `>` vs `>=`), return-type mismatches (e.g. a tuple where a list was expected), and unhandled edge cases exercised by secondary tests. Each of these would surface as a test failure in an interactive loop. We hypothesize that test feedback would recover a fraction of them, but this paper provides no measurement of that fraction [TODO: cite prior work on execution-feedback gains if used].

### 9.2 Kronumos v2: test-driven self-healing with guards

Kronumos v2 closes the loop: $I \rightarrow P_1 \rightarrow \text{tests} \rightarrow T_{feedback} \rightarrow P_2 \rightarrow \dots$, bounded to three turns by a retry FSM with a circuit breaker, keeping the pruned prompt on each turn. Iterating against tests creates the risk of patches that satisfy only the visible tests, so v2 adds Sentinel-style guards from the Tokenectomy stack: detection of assertion stripping, skip/ignore annotations, lazy deletion of logic, and narrowing of input domains, plus isolated worktree execution so failed attempts leave the branch clean. Our target for v2 is 15%-25% resolution on SWE-bench Verified; this is a target, not a result, and will be reported only after a full run with the same harness.

### 9.3 Threats to validity

**Internal validity.**
- *Training-test overlap.* Overlap between fine-tuning data and the 500 test instances would inflate results. Mitigation: decontamination (Section 5.4); residual risk from Qwen pre-training remains.
- *Input provenance.* If `<source_file>` derives from the gold patch, file localization is given (Section 6.3). We state which variant applies.
- *Confounded ablation.* Table 3 changes prompt and post-processing together; Table 4 separates them, and stronger baselines are reported.
- *Single run.* Results come from [one run / N seeds]; variance across seeds is [not measured / reported].
- *Structural validators.* The dry-run and AST checks do not execute code but influence which patches are submitted.

**Construct validity.**
- *"Resolved" is test-based.* A patch that passes the tests may still be an overfitting or incomplete fix. Case-study patches were compared with reference fixes (Section 8).
- *Abstention is not calibration.* Empty patches result from generation or validation failure and do not indicate that the model recognized its own uncertainty.
- *Token and cost accounting.* Tokens are counted with [tokenizer]. "$0.00" excludes GPU quota, training compute, and engineering time; we report GPU time per resolved issue instead.
- *Failure analysis.* The categorization of failed candidates is qualitative and done by [N annotators].
- *Secret redaction.* Coverage is five secret classes; recall [TODO].

**External validity.**
- *Language and repositories.* Python only, 12 repositories, 10 resolved instances in 5 of them. Per-repository counts are too small for generalization claims.
- *Benchmark exposure.* SWE-bench Verified is public and may appear in pre-training corpora of many models, including the base model.
- *Model scale.* One 7B model is evaluated; no claims about other scales.

**Conclusion validity.**
- The 2.0% resolve rate has a 95% Wilson CI of 1.1%-3.6%, and the 12.66% precision a CI of 7.0%-21.8%. Differences from other systems within these intervals are not statistically meaningful, and no significance test is claimed.
- Literature comparisons (Table 7) use different splits, retrieval settings, and protocols and are given for context only.

---

## 10 Related Work

**Classical APR.** Early systems used genetic programming (GenProg [5]), symbolic execution (SemFix [8]), and constraint solving (Angelix [7]). They suffer from search-space explosion and often produce degenerate patches that pass tests by deleting functionality, which motivates the anti-overfitting guards in v2.

**LLM-based repair and agents.** Code language models [9, 3] enabled generative repair, and SWE-bench [4] set the standard for repository-level evaluation. SWE-agent [11] and OpenHands [10] give models an agent-computer interface with execution feedback. Pipeline-style systems such as Agentless [12] and AutoCodeRover [13] avoid open-ended agent loops by fixing the workflow (localize, repair, validate); they are the closest comparison points for Kronumos and the natural next baselines.

**Kronumos' position.** Kronumos differs from these systems in being vertical and cost-bounded: a small open-weight model plus deterministic Rust components, evaluated without execution feedback.

---

## 11 Conclusion

Kronumos is a vertical bug-remediation system that moves context pruning, secret redaction, and patch construction out of the model and into a deterministic runtime, and pairs it with a fine-tuned 7B model. On SWE-bench Verified it resolves 10 of 500 instances (2.0%; 95% CI 1.1%-3.6%) with 3,009.3 prompt tokens per instance and no API cost, under a zero-execution single-turn protocol. The results establish an efficiency and safety baseline for small-model APR and show that deterministic patch construction is necessary for such a model to produce applicable patches; they do not establish competitiveness with interactive agents. Kronumos v2 will add bounded test feedback with anti-overfitting guards, and future work will add stronger baselines, post-cutoff evaluation, and multi-seed variance.

---

## Data Availability and Reproducibility

Code, fine-tuning scripts, Tokenectomy Sub-Cortex source, and official evaluation logs (`Kronumos-7B.kronumos_run.json`) are at https://github.com/Tokenectomy-Labs/Kronomus [TODO: unify the spelling "Kronumos" / "Kronomus" in the repository name and URL].

## References

[1] C. Le Goues, M. Pradel, and A. Roychoudhury. Automated program repair. *Communications of the ACM*, 62(12):56-65, 2019.
[2] E. J. Hu et al. LoRA: Low-Rank Adaptation of Large Language Models. arXiv:2106.09685, 2021.
[3] B. Hui et al. Qwen2.5-Coder Technical Report. arXiv:2409.12186, 2024.
[4] C. E. Jimenez et al. SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ICLR, 2024.
[5] C. Le Goues, T. Nguyen, S. Forrest, and W. Weimer. GenProg. *IEEE TSE*, 38(1):54-72, 2012. [TODO: verify year]
[6] N. F. Liu et al. Lost in the Middle: How Language Models Use Long Contexts. *TACL*, 12:157-173, 2024.
[7] S. Mechtaev, J. Yi, and A. Roychoudhury. Angelix: Scalable multiline program patch synthesis via symbolic analysis. ICSE, 2016.
[8] H. D. T. Nguyen, D. Qi, A. Roychoudhury, and S. Chandra. SemFix: Program repair via semantic analysis. ICSE, 2013.
[9] B. Roziere et al. Code Llama: Open Foundation Models for Code. arXiv:2308.12950, 2023.
[10] X. Wang et al. OpenHands: An Open Platform for AI Software Developers as Generalist Agents. arXiv:2407.16741, 2024. [TODO: verify author initial]
[11] J. Yang et al. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. arXiv:2405.15793, 2024.
[12] C. S. Xia, Y. Deng, S. Dunn, and L. Zhang. Agentless: Demystifying LLM-based Software Engineering Agents. arXiv:2407.01489, 2024. [TODO: verify]
[13] Y. Zhang, H. Ruan, Z. Fan, and A. Roychoudhury. AutoCodeRover: Autonomous Program Improvement. arXiv:2404.05427, 2024. [TODO: verify]

---

## Pre-submission checklist (not part of the paper)

1. Fill Section 5.4 (training data, decontamination) and choose Variant A or B in Section 6.3.
2. Fill Table 4 (missing 2x2 cells and fair baselines) and Table 5 (breakdown of the 421 empty patches).
3. Paste the exact SymPy-22714 patch and confirm the other four diffs against the run JSON.
4. Fill Table 7 from the papers and the official leaderboard; confirm splits.
5. Confirm Tokenectomy tiers and version in Table 1.
6. State decoding settings, number of runs and seeds, and what the latency figures include.
7. Fix the reference details marked [TODO] and the "Kronumos"/"Kronomus" spelling.
