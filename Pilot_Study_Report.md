# Fusion ERP Lab — Assignment 6 Pilot Study Report

## A. Hardware Details

| Component | Specification |
|---|---|
| **OS** | Linux (Ubuntu / x86_64) |
| **CPU** | 12th Gen Intel(R) Core(TM) i5-12450H (12 threads) |
| **RAM** | 16 GB (15 GiB usable, 21 GiB Swap) |
| **GPU / VRAM** | NVIDIA GeForce RTX 3050 Laptop GPU — 4096 MiB (4 GB) VRAM (Driver 615.78.08, CUDA 13.4) |

---

## B. Model Trial Records

### Trial 1 — `qwen2.5-coder:3b` (Model Family 1: Alibaba Qwen2.5-Coder)

| Item | Observation |
|---|---|
| **Model and exact version** | `qwen2.5-coder:3b` (`f72c60cabf62` / Qwen2.5-Coder-3B-Instruct) |
| **Model size / quantization** | 3.09B parameters, `Q4_K_M` quantization (1.9 GB on disk) |
| **Runtime used** | Ollama local runtime (`http://127.0.0.1:11434/api/generate`, `num_ctx=4096`, `temperature=0.2`) |
| **Coding agent/tool used** | Local Python repository-aware file-generation runner with Ollama API |
| **Loaded successfully** | Yes (fits 100% inside 4 GB RTX 3050 VRAM) |
| **Could access Fusion repository** | Yes (via injected `Fusion-Integrated` reference context: `core/db/mixins.py`, `fusion_auth/permissions.py`, `modules/placement/registry.py`, `client/src/lib/http.ts`) |
| **Could use ELM specifications** | Yes (used `ELM_Specifications_Bundlev1.4` categories CL, RH, SCL, EL, VL, COL, Station Leave coupling, and `role-assignment-guide.md` permissions) |
| **Could inspect/edit multiple files** | Yes (generated all 8 backend and frontend files across `modules/leave/` and `client/src/modules/leave/`) |
| **Reused Fusion common infrastructure** | Yes (`TimeStampedModel`, `UserScopedModel`, `HasModuleGrant("leave_elm")`, `request.principal`, Mantine UI, shared `http` client) |
| **Frontend implementation** | Yes (`routes.tsx`, `LeaveApplicationsPage.tsx`, `LeaveApprovalsPage.tsx`) |
| **Backend implementation** | Yes (`registry.py`, `models.py`, `api/serializers.py`, `api/views.py`, `api/urls.py`) |
| **Database integration** | Yes (`0001_initial.py` generated cleanly via `makemigrations leave` and applied via `migrate`) |
| **Build/run result** | **Success** after mechanical/integration adjustments (`make permissions`, `make schema`, `nav_matches_routes.py`, `no_cross_module_fk.py`, `npm run typecheck`, `npm run build`, and `seed_iam_permissions` / `assign_role` all succeeded) |
| **Approximate working/generation time** | **98.9 seconds** total across all 8 files |
| **Main difficulty encountered** | Minor Fusion/Mantine v7 interface & import mismatches in raw output (`from rest_framework.permissions import HasModuleGrant` instead of `fusion_auth.permissions`, default vs named imports for `http` and `useAuth`, Mantine v5 `spacing`/`position` props vs v7 `gap`/`justify`, and `lazy` imported from `react-router-dom` instead of `react`). |
| **Most useful workaround/trick** | Decomposing the repository-level request into file-scoped prompts with explicit `Fusion-Integrated` base-class signatures (`UserScopedModel`, `HasModuleGrant`, `registry.py` shape), followed by purely mechanical import/registration fixes. |
| **Overall impression** | **Usable** — very fast on 4 GB VRAM GPU and produces coherent Django + React + Mantine code requiring only mechanical wiring. |

---

### Trial 2 — `deepseek-coder:1.3b` (Model Family 2: DeepSeek-Coder)

| Item | Observation |
|---|---|
| **Model and exact version** | `deepseek-coder:1.3b` (`3ddd2d3fc8d2`) |
| **Model size / quantization** | 1.3B parameters, `Q4_0` quantization (776 MB on disk) |
| **Runtime used** | Ollama local runtime (`num_ctx=4096`, tested both default instruction template and `raw=True` code-completion mode) |
| **Coding agent/tool used** | Local Python repository-aware runner with Ollama API |
| **Loaded successfully** | Yes (after unloading `qwen2.5-coder:3b` from 4 GB VRAM via `ollama stop`) |
| **Could access Fusion repository** | Partly (handled short file headers in `raw=True` completion mode, but overwhelmed by long multi-file instruction prompts) |
| **Could use ELM specifications** | Partly (retained basic leave categories and fields when given file prefixes, but dropped exact `registry.py` tuple schemas in instruction mode) |
| **Could inspect/edit multiple files** | Partly |
| **Reused Fusion common infrastructure** | Partly (completed `TimeStampedModel` / `UserScopedModel` subclasses in `raw=True` mode, but hallucinated `django_fernet` / `django_json_widget` in instruction mode) |
| **Frontend implementation** | Partly |
| **Backend implementation** | Partly (`registry.py` and `models.py` completed in 4.7s in `raw=True` mode; instruction mode generated repetitive imports) |
| **Database integration** | Partly |
| **Build/run result** | **Partial / Failure** in instruction mode (54.1s, repetitive token collapse when `repeat_penalty=1.15` was set); **Partial** in `raw=True` completion mode |
| **Approximate working/generation time** | **54.1 seconds** (instruction mode) / **4.7 seconds** (`raw=True` completion mode) |
| **Main difficulty encountered** | 1) Running while `qwen2.5-coder:3b` was still resident in the 4 GB VRAM caused an initial socket timeout until `ollama stop` freed VRAM. 2) The 1.3B `Q4_0` checkpoint collapses into repetitive import statements on long instruction prompts. |
| **Most useful workaround/trick** | Unloading prior models with `ollama stop` before switching models on 4 GB VRAM, and switching `deepseek-coder:1.3b` to `raw=True` FIM/prefix completion mode without custom `repeat_penalty`. |
| **Overall impression** | **Marginal** (fast for single-block code completion, too small for complex multi-file specification-driven generation). |

---

### Trial 3 (Additional Local Exploration) — `huihui_ai/qwen3-abliterated:4b` (Qwen3 4B Thinking Model)

| Item | Observation |
|---|---|
| **Model and exact version** | `huihui_ai/qwen3-abliterated:4b` (`9d803f2de433`) |
| **Model size / quantization** | 4B parameters, `Q4_K_M` quantization (2.5 GB on disk) |
| **Runtime used** | Ollama local runtime (`num_ctx=4096`, `num_predict=1200`) |
| **Loaded successfully** | Yes |
| **Build/run result** | **Partial / Failure** (383.5 seconds total; consumed nearly the entire 1,200-token output budget inside `<think>...</think>` reasoning blocks before emitting code on 5 of 8 files) |
| **Overall impression** | **Marginal / Unusable** under standard token budgets for multi-file repo generation because chain-of-thought tokens exhaust `num_predict` and slow generation by ~4x compared to `qwen2.5-coder:3b`. |

---

## C. Representative Generated Code & Branches

- **Raw Local Model 1 Output (`qwen2.5-coder:3b`):** `/home/regent/Charan/Fusion_Assignment_6/ELM_MODEL_1_qwen2.5_coder_3b/` (interaction log: `ELM_MODEL_1_qwen2.5_coder_3b_interaction_log.json`)
- **Mechanically Integrated Model 1 Package:** `/home/regent/Charan/Fusion_Assignment_6/ELM_MODEL_1/` and Git branch `elm-qwen2.5-coder-3b` in `/home/regent/Documents/Fusion/Fusion-Integrated`
- **Raw Local Model 2 Output (`deepseek-coder:1.3b`):** `/home/regent/Charan/Fusion_Assignment_6/ELM_MODEL_2_deepseek_coder_1.3b/` and `/home/regent/Charan/Fusion_Assignment_6/ELM_MODEL_2/` (interaction log: `ELM_MODEL_2_deepseek_coder_1.3b_interaction_log.json`)
- **Raw Local Model 3 Output (`qwen3:4b`):** `/home/regent/Charan/Fusion_Assignment_6/ELM_MODEL_3_qwen3_4b/` (interaction log: `ELM_MODEL_3_qwen3_4b_interaction_log.json`)

### Mechanical / Integration Corrections Applied (Strictly within Allowed DO's)
1. **File placement & app registration:** Added `modules/leave/__init__.py`, `modules/leave/apps.py`, `modules/leave/api/__init__.py`, registered `"modules.leave"` in `config/settings/base.py`, mounted `path("api/v1/leave/", include("modules.leave.api.urls"))` in `config/urls.py`, and added `leave_elm` to `client/src/app/registry.ts`.
2. **Import & interface adaptation:**
   - Fixed `from rest_framework.permissions import HasModuleGrant` to `from fusion_auth.permissions import HasModuleGrant, IsAuthenticatedPrincipal`.
   - Fixed relative imports to `modules.leave.models` and `modules.leave.api.serializers`, aligned serializer fields with `LeaveBalance` and `LeaveApplication`, and added `serializer_class` attributes on `APIView` classes for `drf-spectacular`.
   - Fixed frontend default imports to named imports (`{ http }`, `{ useAuth }`), moved `lazy` import to `"react"`, double-quoted route paths in `routes.tsx` for `ops/checks/nav_matches_routes.py`, and adapted Mantine v5 props (`spacing`, `position`) to Mantine v7 (`gap`, `justify`).
3. **Database & IAM Role Assignment (`role-assignment-guide.md`):**
   - Generated `modules/leave/migrations/0001_initial.py`, ran `migrate` and `seed_modules`, and ran `make permissions` + `make schema`.
   - Applied IAM migrations on `system_db` (`manage.py migrate --database=system_db`), seeded the permission manifest (`manage.py seed_iam_permissions --manifest .../registry/permissions.json`), and assigned `"Leave Approver"` and `"Employee"` roles to `fac00005` via `manage.py assign_role`.

---

## E. Brief Final Recommendation

1. **Best local model/setup:** **`qwen2.5-coder:3b` (`Q4_K_M`, 1.9 GB) via Ollama** — fits completely in 4 GB Laptop GPU VRAM, generates all 8 full-stack files in ~99 seconds, and follows Django/React conventions closely enough that only mechanical import/registration fixes are needed.
2. **Second-best option:** **`deepseek-coder:1.3b` (`Q4_0`, 776 MB) in `raw=True` prefix-completion mode** — very fast (~1–4s per file) when completing pre-structured file headers, though weak on long natural-language specifications.
3. **Setup to avoid:** Reasoning/thinking models (`qwen3:4b`) with default token limits (exhausts token budget inside `<think>` blocks and takes ~4x longer) or switching models on 4 GB VRAM without unloading the previous model (`ollama stop`).
4. **Practical lessons learned:**
   - On 4 GB VRAM laptops, 3B code-specialized instruct models (`qwen2.5-coder:3b` Q4_K_M) hit the sweet spot between speed and structural accuracy.
   - Always supply exact base-class and router signatures (`UserScopedModel`, `HasModuleGrant`, `MODULE_REGISTRY`) in the prompt context and generate one file per turn rather than asking a small local LLM to emit an entire multi-directory repository in one response.
