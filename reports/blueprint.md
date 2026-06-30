# CI/CD Blueprint: RAG Eval + Guardrail Stack

**Sinh viên:** Dương Thế Linh
**Mã học viên:** 2A202600914
**Ngày:** 30/06/2026

---

## Guard Stack Architecture

```
User Input
    │
    ▼ (~?ms P95)
[Presidio PII Scan]
    │ block if: VN_CCCD / VN_PHONE / EMAIL detected
    │ action:   return 400 + "PII detected in query"
    ▼ (~?ms P95)
[NeMo Input Rail]
    │ block if: off-topic / jailbreak / prompt injection
    │ action:   return 503 + refuse message
    ▼
[RAG Pipeline (Day 18)]
    │ M1 Chunk → M2 Search → M3 Rerank → GPT-4o-mini
    ▼
[NeMo Output Rail]
    │ flag if:  PII in response / sensitive content
    │ action:   replace with safe response
    ▼
User Response
```

---

## Latency Budget

*(Điền từ kết quả Task 12 — measure_p95_latency())*

| Layer | P50 (ms) | P95 (ms) | P99 (ms) | Budget |
|---|---|---|---|---|
| Presidio PII | - | 566.52 | - | <10ms |
| NeMo Input Rail | - | 553.29 | - | <300ms |
| RAG Pipeline | - | - | - | <2000ms |
| NeMo Output Rail | - | - | - | <300ms |
| **Total Guard** | - | **995.07** | - | **<500ms** |

**Budget OK?** [ ] Yes / [x] No  
**Comment:** Presidio local scanner và NeMo đang tốn thời gian đáng kể. Presidio có thể gặp vấn đề về IO hoặc load models trên môi trường local hiện tại dẫn đến chậm. NeMo Input Rail gọi LLM nên latency cao là điều dễ hiểu. Cần tối ưu hoặc deploy trên phần cứng tốt hơn.

---

## CI/CD Gates (phải pass trước khi merge to main)

```yaml
# .github/workflows/rag_eval.yml
- name: RAGAS Quality Gate
  run: python src/phase_a_ragas.py
  env:
    MIN_FAITHFULNESS: 0.75
    MIN_AVG_SCORE: 0.65

- name: Guardrail Gate
  run: pytest tests/test_phase_c.py -k "test_adversarial_suite_pass_rate"
  # phải ≥ 15/20 (75%)

- name: Latency Gate
  run: python -c "from src.phase_c_guard import measure_p95_latency; ..."
  # P95 total < 500ms
```

---

## Monitoring Dashboard (production)

| Metric | Alert Threshold | Action |
|---|---|---|
| RAGAS faithfulness (daily sample) | < 0.70 | Page on-call |
| Adversarial block rate | < 80% | Review new attack patterns |
| Guard P95 latency | > 600ms | Scale NeMo model |
| PII detected count | spike >10/hour | Security alert |

---

## Kết quả thực tế từ Lab

| | Kết quả |
|---|---|
| RAGAS avg_score (50q) | ? |
| Worst metric | ? |
| Dominant failure distribution | ? |
| Cohen's κ | 0.000 |
| Adversarial pass rate | 18 / 20 |
| Guard P95 latency | 995.07 ms |

---

## Nhận xét & Cải tiến

> Hệ thống Guardrails hoạt động khá tốt với Adversarial pass rate đạt mức yêu cầu (18/20). Tuy nhiên, latency hiện tại đang vượt quá mức ngân sách (995.07 ms so với 500 ms) do độ trễ từ mô hình LLM và engine PII. Trong môi trường production, cần tối ưu Presidio bằng cách pre-load rules hiệu quả hơn, và có thể sử dụng các local/edge model nhỏ hơn và nhanh hơn thay cho NeMo hoặc tinh chỉnh caching để giảm thiểu các truy vấn LLM không cần thiết.
