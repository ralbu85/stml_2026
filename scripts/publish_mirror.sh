#!/usr/bin/env bash
# 공개 미러(stml_2026)에 "공개된 주차"의 자료만 스냅샷으로 강제 푸시한다.
# 전체 소스는 비공개 리포(stml_2026_src)에 있다. Colab 링크와 raw 데이터 URL이
# 이 미러의 경로(lectures/weekNN/..., labs/data/...)를 가리키므로 경로를 바꾸지 않는다.
# 공개 주차 목록은 site/build.sh의 PUBLISH_WEEKS를 그대로 읽는다.
set -euo pipefail
cd "$(dirname "$0")/.."

WEEKS=$(sed -n 's/^PUBLISH_WEEKS="\(.*\)"$/\1/p' site/build.sh)
[ -n "$WEEKS" ] || { echo "PUBLISH_WEEKS not found in site/build.sh"; exit 1; }
MIRROR_URL="https://github.com/ralbu85/stml_2026.git"

tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT

for nn in $WEEKS; do
  mkdir -p "$tmp/lectures/week$nn"
  rsync -a --exclude 'slides.pptx' --exclude 'slides.html' --exclude 'slides_files' \
        --exclude '.ipynb_checkpoints' \
        "lectures/week$nn/" "$tmp/lectures/week$nn/"
  if [ -d "labs/checkpoints/week$nn" ]; then
    mkdir -p "$tmp/labs/checkpoints"
    cp -r "labs/checkpoints/week$nn" "$tmp/labs/checkpoints/"
  fi
done

# 주차별 데이터 의존물 (노트북이 raw URL로 내려받는 파일)
case " $WEEKS " in *" 05 "*)
  mkdir -p "$tmp/labs/data"; cp labs/data/coffee_sales.csv "$tmp/labs/data/";;
esac

cat > "$tmp/README.md" << 'MD'
# STML 2026 — 공개 자료 미러

수업 자료는 강의 사이트에서 열람한다: <https://stml.tailcce2b.ts.net>

이 리포는 Colab 실행을 위한 공개 주차 자료의 사본이며, 주차가 공개될 때마다 갱신된다.
MD

cd "$tmp"
git init -q -b main
git add -A
git -c user.name="ralbu85" -c user.email="ralbu85@gmail.com" \
    commit -q -m "공개 주차 자료 미러 갱신 (weeks: $WEEKS)"
git push -q --force "$MIRROR_URL" main
echo "mirror pushed: weeks $WEEKS"
