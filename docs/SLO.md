# Service-Level Objectives

| SLO | Initial target | Reason |
| --- | --- | --- |
| Queue-to-start p95 | <= 90 seconds | Measures whether capacity responds quickly enough |
| Runner startup success | >= 99% | Detects image, capacity, JIT, and scheduling failures |
| Runner cleanup success | 100% | Prevents state persistence and abandoned compute |
| Maximum queue age | <= 300 seconds | Limits prolonged customer-visible delay |
| Lifecycle evidence coverage | 100% | Every runner should have startup and cleanup evidence |

These are design targets, not achieved production claims. Evidence must include
the exact load profile, timestamps, configuration, and measurement interval.

## Error-budget use

Any startup or cleanup failure in the small portfolio lab consumes the entire
demonstration error budget and requires an incident record. Automated
infrastructure mutation remains out of scope until false-positive and rollback
behavior have been tested.
