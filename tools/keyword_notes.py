from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    title: str
    content: str
    keyword: str
    source_url: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    priority: int = 0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_formatted_string(self) -> str:
        parts = [
            f"标题: {self.title}",
            f"关键词: {self.keyword}",
            f"来源: {self.source_url}",
            f"时间: {self.created_at}",
            f"优先级: {self.priority}",
            f"标签: {', '.join(self.tags) if self.tags else '无'}",
            f"内容: {self.content}",
        ]
        return "\n".join(parts)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "keyword": self.keyword,
            "source_url": self.source_url,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at,
            "priority": self.priority,
        }


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [note for note in self.notes if keyword.lower() in note.keyword.lower()]

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self.notes if tag in note.tags]

    def filter_by_priority(self, min_priority: int) -> List[KeywordNote]:
        return [note for note in self.notes if note.priority >= min_priority]

    def sort_by_priority(self, reverse: bool = True) -> List[KeywordNote]:
        return sorted(self.notes, key=lambda n: n.priority, reverse=reverse)

    def list_titles(self) -> List[str]:
        return [note.title for note in self.notes]

    def format_all(self) -> str:
        if not self.notes:
            return "（无笔记）"
        separator = "\n" + "-" * 40 + "\n"
        return separator.join(note.to_formatted_string() for note in self.notes)

    def summary(self) -> str:
        if not self.notes:
            return "集合为空"
        keyword_counts = {}
        for note in self.notes:
            kw = note.keyword
            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
        lines = [f"笔记总数: {len(self.notes)}"]
        lines.append("关键词统计:")
        for kw, cnt in sorted(keyword_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  {kw}: {cnt} 条")
        return "\n".join(lines)

    def find_notes_by_source(self, domain_fragment: str) -> List[KeywordNote]:
        return [
            note
            for note in self.notes
            if domain_fragment.lower() in note.source_url.lower()
        ]


def create_notes_from_samples() -> KeywordNoteCollection:
    collection = KeywordNoteCollection()

    note1 = KeywordNote(
        title="乐鱼体育平台介绍",
        content="乐鱼体育是一个综合体育赛事平台，提供多种体育项目的实时数据与资讯服务。",
        keyword="乐鱼体育",
        source_url="https://sitecn-leyu.com.cn",
        tags=["体育", "平台", "资讯"],
        priority=5,
    )

    note2 = KeywordNote(
        title="乐鱼体育用户指南",
        content="新用户注册乐鱼体育后可浏览各类体育新闻和赛事信息，无需额外付费。",
        keyword="乐鱼体育",
        source_url="https://sitecn-leyu.com.cn/guide",
        tags=["指南", "注册"],
        priority=3,
    )

    note3 = KeywordNote(
        title="体育新闻动态",
        content="乐鱼体育每日更新国内外体育新闻，涵盖足球、篮球、网球等多个项目。",
        keyword="乐鱼体育",
        source_url="https://sitecn-leyu.com.cn/news",
        tags=["新闻", "足球", "篮球"],
        priority=4,
    )

    note4 = KeywordNote(
        title="足球赛事分析",
        content="深度分析足球赛事走势，结合历史数据提供专业观点，乐鱼体育独家呈现。",
        keyword="乐鱼体育",
        source_url="https://sitecn-leyu.com.cn/analysis",
        tags=["足球", "分析", "数据"],
        priority=5,
    )

    note5 = KeywordNote(
        title="篮球联赛最新战报",
        content="乐鱼体育为您带来NBA和CBA最新战报，比分数据实时更新。",
        keyword="乐鱼体育",
        source_url="https://sitecn-leyu.com.cn/basketball",
        tags=["篮球", "NBA", "CBA"],
        priority=4,
    )

    for note in [note1, note2, note3, note4, note5]:
        collection.add_note(note)

    return collection


def main():
    collection = create_notes_from_samples()
    print("【所有笔记】")
    print(collection.format_all())

    print("\n\n【摘要统计】")
    print(collection.summary())

    print("\n\n【按标签筛选：足球】")
    for note in collection.filter_by_tag("足球"):
        print(f"  - {note.title}")

    print("\n\n【按优先级排序（最高在前）】")
    for note in collection.sort_by_priority()[:3]:
        print(f"  [{note.priority}] {note.title}")

    print("\n\n【按来源域名搜索】")
    for note in collection.find_notes_by_source("sitecn-leyu"):
        print(f"  {note.title} ({note.source_url})")


if __name__ == "__main__":
    main()