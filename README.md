# 입시한입 — 통합 대문 (ipsihanip.github.io)

정시한입(`https://jeongsihanip.github.io/`)과 수시한입(`https://susihanip.github.io/`)을 하나로 묶는 대문 페이지입니다.

## 구성

- `index.html` — 대문 페이지 (정시/수시 선택 카드, 라이트/다크 테마 토글, 참고용 안내, 유튜브 채널 링크)
- `style.css` — 스타일 (라이트 `html[data-theme="light"]` / 다크 기본, 390px 모바일 ~ 데스크톱)
- `preview.py` — Playwright 검수 스크립트 (390/768/1440 · 라이트/다크 스크린샷 + 오버플로 검사)
- `robots.txt`, `sitemap.xml` — 검색엔진용

테마 선택은 `localStorage`의 `ipsihanip-theme` 키에 저장됩니다 (정시 `jeongsihanip-theme`, 수시 `susihanip-theme`와 별개).

## 배포

GitHub 조직 `ipsihanip`의 공개 저장소 `ipsihanip/ipsihanip.github.io` `main` 브랜치 루트가 곧 사이트입니다.

```bash
git push origin main   # → https://ipsihanip.github.io/
```

## 검수

```bash
export LD_LIBRARY_PATH=/workspace/work/chromium-libs/usr/lib/x86_64-linux-gnu:/workspace/work/chromium-libs/lib/x86_64-linux-gnu
python3 preview.py
```

## 양쪽 사이트 헤더의 대문 링크

정시한입·수시한입 헤더의 `정시 | 수시 | 대문` 전환 탭에서 `대문` 항목이 이 페이지(`https://ipsihanip.github.io/`)로 연결됩니다.
