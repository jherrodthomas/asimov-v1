# WP-A-05 Independence of the safety chain from the policy and tele-operation stack (freedom from interference)

| Field | Value |
|---|---|
| Work product | WP-A-05 Independence of the safety chain from the policy and tele-operation stack (freedom from interference) |
| Standard reference | SRP/CS: 13849-1 §6, §7; 61508-3 Annex F; IEC 62443: 62443-3-3 §5 (zoning) |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G2** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Independence of the safety chain from the locomotion policy and the tele-operation stack: freedom from interference through shared power, shared buses, shared processors and shared software; why nothing on the edge board or in the policy can hold the motor rail enabled or defeat a clamp.

## 2. Shared resources

Battery rail and 5 V input, the six CAN buses, the CM5 running both the safety layer and the policy runtime, the Wi-Fi link, the operator app.

## 3. Analysis

Per resource: interference path, barrier, residual.

## 4. Conclusion

Which functions are independent of the stack, which are not, and what that means for their category.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
