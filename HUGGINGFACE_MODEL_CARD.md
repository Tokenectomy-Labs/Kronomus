---
base_model: unsloth/qwen2.5-coder-7b-instruct-bnb-4bit
tags:
- text-generation-inference
- transformers
- unsloth
- qwen2
- swe-bench
- autonomous-agents
- program-repair
- code-generation
- rust-subcortex
license: apache-2.0
language:
- en
datasets:
- princeton-nlp/SWE-bench_Verified
pipeline_tag: text-generation
---

# ⚡ Kronumos 2 Kairos: The Dual-Brain Sub-Cortex Autonomous Program Repair Engine

**Organization:** Tokenectomy Labs  
**Base Model:** Qwen/Qwen2.5-Coder-7B-Instruct  
**Research Paper:** [10.5281/zenodo.22929676](https://doi.org/10.5281/zenodo.22929676)  
**Repository:** [Tokenectomy-Labs/Kronomus](https://github.com/Tokenectomy-Labs/Kronomus)  

Kronumos 2 Kairos is an open-weight 7B autonomous program repair (APR) model fine-tuned for high-precision code remediation on real-world production software bugs. It pairs parametric neural intuition with a deterministic, zero-allocation Rust Sub-Cortex (Tokenectomy Procedural Cognitive Kernel).

---

## 🥊 Benchmark Verification: SWE-bench Verified (500 Instances)

Evaluated end-to-end on the official Princeton SWE-bench Verified benchmark (500 production instances across Django, Scikit-Learn, PyData Xarray, Sphinx, Sympy, etc.) using official Docker execution containers.

| Metric | Kronumos 2 Kairos | Industry Multi-Turn Baselines |
| :--- | :---: | :---: |
| **Model Size** | **7B Parameters** | 70B - 405B / Frontier APIs |
| **Execution Mode** | **Single-Pass Zero-Shot** | Multi-Turn Agent Loop (50-100 Turns) |
| **Avg Tokens / Task** | **2,512 Tokens** | 40,000 - 150,000 Tokens |
| **Token Efficiency** | **93.5% Reduction** | Baseline (1.0x) |
| **API Cost** | **$0.00 (Pure Local Weights)** | $3.00 - $15.00 per issue |
| **Verified Resolved Tasks** | **8 Full Production Issues** | - |

### 🏆 Verified Resolved Production Issues:
1. `django__django-13569`: Broken aggregation expression logic in database queries.
2. `django__django-13658`: Management command argument parser collision.
3. `django__django-14855`: Admin URL generation prefix regression.
4. `django__django-15104`: Model custom key migration constraint hazard.
5. `django__django-16333`: Many-to-many relationship foreign key mapping.
6. `pydata__xarray-4629`: Multi-index coordinate slice dimension regression.
7. `scikit-learn__scikit-learn-10844`: Pipeline estimators parameter validation fault.
8. `sphinx-doc__sphinx-8595`: Python domain autodoc signature formatting error.

---

## 🏛️ The Dual-Brain Cybernetic APR Architecture

Traditional LLM agents rely exclusively on multi-turn prompt loops, generating massive token overhead and hallucinating syntax formatting. Kronumos Kairos decouples cognition into two integrated computing cortices:

```
           [Raw GitHub Issue Discussion]
                         │
                         ▼
        ┌──────────────────────────────────┐
        │   Sub-Cortex IssueDeNoiser       │
        │   - Excises human chatter/quotes │
        │   - Tags user reproduction code  │
        │   - Extracts Core Signal Triad   │
        └────────────────┬─────────────────┘
                         │
        [Cleaned Technical Specification]
                         │
                         ▼
        ┌──────────────────────────────────┐
        │  Procedural Cognitive Kernel     │ ◄─── Procedural Seeds (<64 bytes)
        │  - BoundaryCondition Invariants  │      (Zero-DB L1 Cache Execution)
        │  - DefensiveNullWrap / PopGuards │
        └────────────────┬─────────────────┘
                         │
    ┌────────────────────┴────────────────────┐
    ▼                                         ▼
┌───────────────────────┐         ┌───────────────────────┐
│   CORTEX (Neural)     │         │ SUBCORTEX (Deterministic)
│  Qwen2.5-Coder-7B     │ ◄─────► │ Tree-sitter AST Slicer│
│  - 5-Step CoT Reason  │ Dual-Key│ Auto-Bracket & Indent │
│  - Precise Code Hunk  │ Consens.│ Merkle Causal Ledger  │
└───────────────────────┘         └───────────────────────┘
```

1. **Issue De-Noiser**: Strips human conversational chaff, extracting the core reproduction triad.
2. **Procedural Cognitive Kernel**: Diagnoses invariants across 9 domains (Boundary, Defensive, Concurrency, etc.) without external database lookups.
3. **Dual-Key Consensus Gate**: Requires simultaneous semantic approval and deterministic AST validation before admitting state changes.
4. **Auto-Bracket & Indentation Healer**: Deterministically balances parentheses and enforces strict PEP 8 4-space block indentation.

---

## 💻 Quickstart: Running Inference

### With Transformers:
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "NadevA23/Kronumos-Kairos-v2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

messages = [
    {"role": "system", "content": "You are Kronumos Kairos, an expert autonomous program repair engine."},
    {"role": "user", "content": "Fix the issue in the following function:\n\ndef safe_divide(a, b):\n    return a / b"}
]

inputs = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt").to(model.device)
outputs = model.generate(inputs, max_new_tokens=512, do_sample=False)
print(tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True))
```

### With GGUF (Llama.cpp / Ollama):
For quantized local execution on consumer hardware, visit [NadevA23/Kronumos-Kairos-v2-GGUF](https://huggingface.co/NadevA23/Kronumos-Kairos-v2-GGUF).

---

## 📜 Citation

If you use Kronumos Kairos or Tokenectomy Sub-Cortex in your research, please cite:

```bibtex
@software{nadev2026kronumos,
  author = {Nadev, Daffa},
  title = {Kronumos 2 Kairos: Dual-Brain Cybernetic Autonomous Program Repair with Deterministic Sub-Cortex},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.22929676},
  url = {https://doi.org/10.5281/zenodo.22929676}
}
```

**License:** Apache 2.0  
**Maintained by:** Tokenectomy Labs
