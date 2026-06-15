import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { api, handleApiError } from "@/lib/api";
import type { Board } from "@/lib/types";
import { useAuth } from "@/lib/auth";
import { toast } from "sonner";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "게시판" },
      { name: "description", content: "게시판 메인" },
    ],
  }),
  component: BoardListPage,
});

function formatDate(s: string) {
  try {
    const d = new Date(s);
    return d.toLocaleString("ko-KR", { dateStyle: "short", timeStyle: "short" });
  } catch {
    return s;
  }
}

function BoardListPage() {
  const [boards, setBoards] = useState<Board[]>([]);
  const [loading, setLoading] = useState(true);
  const [keyword, setKeyword] = useState("");
  const [searchType, setSearchType] = useState<"title" | "content" | "author">("title");
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await api.get<Board[]>("/boards");
        if (!cancelled) {
          const sorted = [...res.data].sort(
            (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
          );
          setBoards(sorted);
        }
      } catch (err) {
        handleApiError(err);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const onWrite = () => {
    if (!isAuthenticated) {
      toast.error("로그인이 필요합니다.");
      return;
    }
    navigate({ to: "/boards/new" });
  };
  const kw = keyword.trim().toLowerCase();
  const filtered = kw
    ? boards.filter((b) => {
        if (searchType === "title") return b.title.toLowerCase().includes(kw);
        if (searchType === "content") return (b.content ?? "").toLowerCase().includes(kw);
        return String(b.member_id).includes(kw);
      })
    : boards;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">게시글 목록</h1>
        <button
          onClick={onWrite}
          disabled={!isAuthenticated}
          className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
          title={isAuthenticated ? "글쓰기" : "로그인이 필요합니다"}
        >
          글쓰기
        </button>
      </div>
 <div className="flex flex-col gap-2 sm:flex-row">
        <select
          value={searchType}
          onChange={(e) => setSearchType(e.target.value as "title" | "content" | "author")}
          className="rounded-md border bg-background px-3 py-2 text-sm"
        >
          <option value="title">제목</option>
          <option value="content">내용</option>
          <option value="author">작성자 ID</option>
        </select>
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="검색어를 입력하세요"
          className="flex-1 rounded-md border bg-background px-3 py-2 text-sm"
        />
        {keyword && (
          <button
            onClick={() => setKeyword("")}
            className="rounded-md border px-3 py-2 text-sm hover:bg-accent"
          >
            초기화
          </button>
        )}
      </div>

      {loading ? (
        <div className="rounded-lg border bg-card p-8 text-center text-muted-foreground">
          불러오는 중...
        </div>
      ) : filtered.length === 0 ? (
        <div className="rounded-lg border bg-card p-8 text-center text-muted-foreground">
                  {kw ? "검색 결과가 없습니다." : "게시글이 없습니다."}
        </div>
      ) : (
                <>
        <div className="text-xs text-muted-foreground">총 {filtered.length}건</div>
        <ul className="space-y-3">
          {filtered.map((b) => (
            <li key={b.id}>
              <Link
                to="/boards/$boardId"
                params={{ boardId: String(b.id) }}
                className="block rounded-lg border bg-card p-4 transition hover:border-primary hover:shadow-sm"
              >
                <h2 className="font-semibold text-base sm:text-lg line-clamp-1">
                  {b.title}
                </h2>
                <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground">
                  <span>작성자 #{b.member_id}</span>
                  <span>조회 {b.view_count}</span>
                  <span>{formatDate(b.created_at)}</span>
                </div>
              </Link>
            </li>
          ))}
        </ul>
        </>
      )}
    </div>
  );
}
