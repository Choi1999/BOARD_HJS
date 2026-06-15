import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useEffect, useState, type FormEvent } from "react";
import { api, handleApiError } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import type { Board } from "@/lib/types";
import { toast } from "sonner";

export const Route = createFileRoute("/boards/$boardId/edit")({
  head: () => ({ meta: [{ title: "게시글 수정" }] }),
  component: EditBoardPage,
});

function EditBoardPage() {
  const { boardId } = Route.useParams();
  const { user, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await api.get<Board>(`/boards/${boardId}`);
        if (cancelled) return;
        if (!user || (user.memberId !== res.data.member_id && !isAdmin)) {
          toast.error("권한이 없습니다.");
          navigate({ to: "/boards/$boardId", params: { boardId } });
          return;
        }
        setTitle(res.data.title);
        setContent(res.data.content);
      } catch (err) {
        handleApiError(err);
        navigate({ to: "/" });
      } finally {
        if (!cancelled) setFetching(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [boardId, user, isAdmin, navigate]);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.put(`/boards/${boardId}`, { title, content });
      toast.success("수정되었습니다.");
      navigate({ to: "/boards/$boardId", params: { boardId } });
    } catch (err) {
      handleApiError(err);
    } finally {
      setLoading(false);
    }
  };

  if (fetching) {
    return <div className="rounded-lg border bg-card p-8 text-center text-muted-foreground">불러오는 중...</div>;
  }

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-4 text-2xl font-bold">게시글 수정</h1>
      <form onSubmit={onSubmit} className="space-y-4 rounded-lg border bg-card p-6">
        <div>
          <label className="mb-1 block text-sm font-medium">제목</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className="w-full rounded-md border bg-background px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">내용</label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
            rows={12}
            className="w-full resize-y rounded-md border bg-background px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
        <div className="flex justify-end gap-2">
          <button
            type="button"
            onClick={() => navigate({ to: "/boards/$boardId", params: { boardId } })}
            className="rounded-md border px-4 py-2 text-sm hover:bg-accent"
          >
            취소
          </button>
          <button
            type="submit"
            disabled={loading}
            className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:opacity-90 disabled:opacity-50"
          >
            {loading ? "저장 중..." : "저장"}
          </button>
        </div>
      </form>
    </div>
  );
}