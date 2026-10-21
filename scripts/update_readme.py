#!/usr/bin/env python3
"""TIL 레포의 README를 자동으로 갱신한다.

사용법:
    python3 scripts/update_readme.py

하는 일:
    1. topics/*/*.md 의 frontmatter를 읽어 TIL 목록을 만든다.
    2. sources/{종류}/{소스}/README.md 의 frontmatter와 retro.md 를 읽어 소스 목록을 만든다.
    3. 루트 README.md 의 마커 사이만 교체한다.
         STATS   : 총 TIL 수, 주제 수, 완료한 소스 수
         TOPICS  : 주제별 TIL 목록 (<details>)
         SOURCES : 공부 중/완료한 소스 표
         RECENT  : 최근 TIL 10개
    4. 각 소스 README 의 TILS 마커 사이에 관련 TIL 목록을 넣는다.
       (TIL frontmatter 의 source 값이 "{종류}/{소스-slug}" 와 같으면 연결된다.)

마커 형식:
    <!-- STATS:START -->
    (이 사이 내용이 교체된다)
    <!-- STATS:END -->

표준 라이브러리만 사용한다.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECENT_COUNT = 10


# ---------------------------------------------------------------
# frontmatter 파싱
# ---------------------------------------------------------------
def parse_value(raw):
    """값 문자열을 파싱한다. [a, b] 는 리스트로, 나머지는 문자열로 돌려준다."""
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        items = [x.strip().strip("'\"") for x in raw[1:-1].split(",")]
        return [x for x in items if x]
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "'\"":
        return raw[1:-1]
    return raw


def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_frontmatter(text):
    """(meta dict, 본문) 을 돌려준다. frontmatter 가 없으면 ({}, text)."""
    if not text.startswith("---"):
        return {}, text
    lines = text.split("\n")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    meta = {}
    for line in lines[1:end]:
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = parse_value(value)
    return meta, "\n".join(lines[end + 1:])


def first_heading(body, fallback):
    for line in body.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


# ---------------------------------------------------------------
# 스캔
# ---------------------------------------------------------------
def list_dirs(path):
    if not os.path.isdir(path):
        return []
    return sorted(d for d in os.listdir(path)
                  if os.path.isdir(os.path.join(path, d)) and not d.startswith("."))


def scan_tils():
    """topics/{주제}/*.md 를 읽어 TIL 정보 리스트를 돌려준다."""
    tils = []
    topics_dir = os.path.join(ROOT, "topics")
    for topic in list_dirs(topics_dir):
        folder = os.path.join(topics_dir, topic)
        for name in sorted(os.listdir(folder)):
            if not name.endswith(".md"):
                continue
            path = os.path.join(folder, name)
            meta, body = parse_frontmatter(read_file(path))
            slug = name[:-3]
            tils.append({
                "path": path,
                "rel": "topics/%s/%s" % (topic, name),
                "topic": topic,
                "date": str(meta.get("date", slug[:10])),
                "title": first_heading(body, slug),
                "source": str(meta.get("source", "")).strip("/"),
                "type": str(meta.get("type", "")),
            })
    return tils


def scan_sources():
    """sources/{종류}/{소스}/README.md 를 읽어 소스 정보 리스트를 돌려준다."""
    sources = []
    sources_dir = os.path.join(ROOT, "sources")
    for kind in list_dirs(sources_dir):
        for slug in list_dirs(os.path.join(sources_dir, kind)):
            folder = os.path.join(sources_dir, kind, slug)
            readme = os.path.join(folder, "README.md")
            if not os.path.isfile(readme):
                continue
            meta, body = parse_frontmatter(read_file(readme))
            retro_path = os.path.join(folder, "retro.md")
            oneliner = ""
            if os.path.isfile(retro_path):
                retro_meta, _ = parse_frontmatter(read_file(retro_path))
                oneliner = str(retro_meta.get("oneliner", ""))
            sources.append({
                "path": readme,
                "rel": "sources/%s/%s" % (kind, slug),
                "key": "%s/%s" % (kind, slug),
                "kind": str(meta.get("kind", kind)),
                "title": str(meta.get("title", first_heading(body, slug))),
                "status": str(meta.get("status", "")),
                "started": str(meta.get("started", "")),
                "finished": str(meta.get("finished", "")),
                "oneliner": oneliner,
            })
    return sources


# ---------------------------------------------------------------
# 마커 교체
# ---------------------------------------------------------------
def replace_marker(text, name, content):
    """<!-- NAME:START --> 와 <!-- NAME:END --> 사이를 content 로 바꾼다."""
    start = "<!-- %s:START -->" % name
    end = "<!-- %s:END -->" % name
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        print("경고: %s 마커를 찾지 못했습니다." % name, file=sys.stderr)
        return text
    block = start + "\n" + content.strip("\n") + "\n" + end if content.strip() else start + "\n" + end
    return pattern.sub(lambda m: block, text, count=1)


def sort_key_recent(til):
    return (til["date"], til["rel"])


# ---------------------------------------------------------------
# 섹션 만들기
# ---------------------------------------------------------------
def build_stats(tils, sources):
    topics = set(t["topic"] for t in tils)
    done = [s for s in sources if s["status"] == "완료"]
    return "\n".join([
        "| 총 TIL | 주제 | 완료한 소스 |",
        "| :---: | :---: | :---: |",
        "| %d | %d | %d |" % (len(tils), len(topics), len(done)),
    ])


def build_topics(tils):
    if not tils:
        return "_아직 TIL이 없습니다._"
    by_topic = {}
    for t in tils:
        by_topic.setdefault(t["topic"], []).append(t)
    parts = []
    for topic in sorted(by_topic):
        items = sorted(by_topic[topic], key=sort_key_recent, reverse=True)
        lines = ["<details>",
                 "<summary><b>%s</b> (%d)</summary>" % (topic, len(items)),
                 ""]
        for t in items:
            lines.append("- %s · [%s](%s)" % (t["date"], t["title"], t["rel"]))
        lines += ["", "</details>", ""]
        parts.append("\n".join(lines))
    return "\n".join(parts)


def build_sources(sources):
    if not sources:
        return "_아직 등록된 소스가 없습니다._"
    lines = ["| 종류 | 제목 | 상태 | 시작일 | 완료일 | 한 줄 평 |",
             "| --- | --- | --- | --- | --- | --- |"]
    for s in sorted(sources, key=lambda x: (x["started"], x["rel"]), reverse=True):
        lines.append("| %s | [%s](%s/) | %s | %s | %s | %s |" % (
            s["kind"], s["title"], s["rel"], s["status"],
            s["started"], s["finished"], s["oneliner"]))
    return "\n".join(lines)


def build_recent(tils):
    if not tils:
        return "_아직 TIL이 없습니다._"
    recent = sorted(tils, key=sort_key_recent, reverse=True)[:RECENT_COUNT]
    return "\n".join("- %s · `%s` · [%s](%s)" % (t["date"], t["topic"], t["title"], t["rel"])
                     for t in recent)


def build_related(source, tils):
    related = [t for t in tils if t["source"] == source["key"]]
    if not related:
        return "_아직 연결된 TIL이 없습니다._"
    related.sort(key=sort_key_recent)
    lines = []
    for t in related:
        # 소스 README 위치(sources/종류/소스/)에서 본 상대 경로
        link = os.path.relpath(os.path.join(ROOT, t["rel"]), os.path.dirname(source["path"]))
        lines.append("- %s · [%s](%s)" % (t["date"], t["title"], link))
    return "\n".join(lines)


# ---------------------------------------------------------------
# 실행
# ---------------------------------------------------------------
def write_if_changed(path, new_text):
    if read_file(path) != new_text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
        print("갱신: %s" % os.path.relpath(path, ROOT))


def main():
    tils = scan_tils()
    sources = scan_sources()

    # 루트 README
    root_readme = os.path.join(ROOT, "README.md")
    text = read_file(root_readme)
    text = replace_marker(text, "STATS", build_stats(tils, sources))
    text = replace_marker(text, "TOPICS", build_topics(tils))
    text = replace_marker(text, "SOURCES", build_sources(sources))
    text = replace_marker(text, "RECENT", build_recent(tils))
    write_if_changed(root_readme, text)

    # 각 소스 README 의 관련 TIL
    for s in sources:
        text = read_file(s["path"])
        text = replace_marker(text, "TILS", build_related(s, tils))
        write_if_changed(s["path"], text)

    print("완료: TIL %d개, 소스 %d개" % (len(tils), len(sources)))


if __name__ == "__main__":
    main()
