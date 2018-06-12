# garbage-collection

reachable
finalized

live object가 아닌 dead object를 garbage

- serial vs parallel vs cms vs G1 (찾아보자)
- concurrent vs stop-the-world
- compacting vs non-compacting vs copying (non-compacting releases object in-place and can cause fragmentation)

Collector 종류

- mark-seep-compact collector
  - serial 혹은 parallel. young이든 old든 짦고 긴 STW pause가 필요
- mark & sweep collector : pause time이 짧다
  - CMS(Concurrent Mark & Sweep) collector는 compaction을 하지 않는다. fagmentation 이슈가 발생
- G1 collector
  - CMS와 유사하지만 대부분 reclaimable한 region들에 대해서 compaction 수행