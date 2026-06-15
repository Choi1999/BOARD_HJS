import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useCallback, useEffect, useState, type FormEvent } from "react";
import { api, handleApiError, getErrorMessage } from "@/lib/api";
import type { Board, Comment } from "@/lib/types";
import { useAuth } from "@/lib/auth";
import { toast } from "sonner";
import { AxiosError } from "axios";

export const Route = createFileRoute("/boards/$boardId")({
  head: () => ({ meta: [{ title: "게시글" }] }),
  component: BoardDetailPage,
});

function formatDate(s: string) {
  try {
    return new Date(s).toLocaleString("ko-KR", { dateStyle: "short", timeStyle: "short" });
  } catch {
    return s;
  }
}

function BoardDetailPage() {
  const { boardId } = Route.useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated, isAdmin } = useAuth();
  const [board, setBoard] = useState<Board | null>(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);

  const [comments, setComments] = useState<Comment[]>([]);
  const [commentText, setCommentText] = useState("");
  const [commentLoading, setCommentLoading] = useState(false);
  const [commentsLoading, setCommentsLoading] = useState(true);

  const loadBoard = useCallback(async () => {
    try {
      const res = await api.get<Board>(`/boards/${boardId}`);
      setBoard(res.data);
    } catch (err) {
      const msg = getErrorMessage(err);
      toast.error(msg);
      if (err instanceof AxiosError && err.response?.status === 404) {
        navigate({ to: "/" });
      }
    } finally {
      setLoading(false);
    }
  }, [boardId, navigate]);

  const loadComments = useCallback(async () => {
    setCommentsLoading(true);
    try {
      const res = await api.get<Comment[]>(`/comments/board/${boardId}`);
      setComments(res.data);
    } catch (err) {
      handleApiError(err);
    } finally {
      setCommentsLoading(false);
    }
  }, [boardId]);

  useEffect(() => {
    loadBoard();
    loadComments();
  }, [loadBoard, loadComments]);

  const canModify =
    !!board && !!user && (user.memberId === board.member_id || isAdmin);

  const onDelete = async () => {
    if (!confirm("정말 삭제하시겠습니까?")) return;
    setDeleting(true);
    try {
      await api.delete(`/boards/${boardId}`);
      toast.success("삭제되었습니다.");
      navigate({ to: "/" });
    } catch (err) {
      handleApiError(err);
    } finally {
      setDeleting(false);
    }
  };

  const onSubmitComment = async (e: FormEvent) => {
    e.preventDefault();
    if (!user) {
      toast.error("로그인이 필요합니다.");
      return;
    }
    if (!commentText.trim()) return;
    setCommentLoading(true);
    try {
      await api.post(
        `/comments`,
        { board_id: Number(boardId), content: commentText },
        { params: { member_id: user.memberId } }
      );
      setCommentText("");
      await loadComments();
    } catch (err) {
      handleApiError(err);
    } finally {
      setCommentLoading(false);
    }
  };

  const onDeleteComment = async (commentId: number) => {
    if (!confirm("댓글을 삭제하시겠습니까?")) return;
    try {
      await api.delete(`/comments/${commentId}`);
      toast.success("댓글이 삭제되었습니다.");
      await loadComments();
    } catch (err) {
      handleApiError(err);
    }
  };

  if (loading) {
    return <div className="rounded-lg border bg-card p-8 text-center text-muted-foreground">불러오는 중...</div>;
  }

  if (!board) return null;

  return (
    <div className="space-y-6">
      <article className="rounded-lg border bg-card p-6">
        <header className="border-b pb-4">
          <h1 className="text-2xl font-bold">{board.title}</h1>
          <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-sm text-muted-foreground">
            <span>작성자 #{board.member_id}</span>
            <span>{formatDate(board.created_at)}</span>
            <span>조회 {board.view_count}</span>
          </div>
        </header>
        <div className="prose prose-sm mt-4 whitespace-pre-wrap break-words text-foreground">
          {board.content}
        </div>
        <div className="mt-6 flex flex-wrap justify-between gap-2">
          <Link to="/" className="rounded-md border px-3 py-1.5 text-sm hover:bg-accent">
            ← 목록
          </Link>
          {canModify && (
            <div className="flex gap-2">
              <Link
                to="/boards/$boardId/edit"
                params={{ boardId }}
                className="rounded-md border px-3 py-1.5 text-sm hover:bg-accent"
              >
                수정
              </Link>
              <button
                onClick={onDelete}
                disabled={deleting}
                className="rounded-md bg-destructive px-3 py-1.5 text-sm text-white hover:opacity-90 disabled:opacity-50"
              >
                {deleting ? "삭제 중..." : "삭제"}
              </button>
            </div>
          )}
        </div>
      </article>

      <section className="rounded-lg border bg-card p-6">
        <h2 className="mb-4 text-lg font-semibold">댓글 {comments.length}</h2>

        {isAuthenticated ? (
          <form onSubmit={onSubmitComment} className="mb-4 flex gap-2">
            <input
              type="text"
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              placeholder="댓글을 입력하세요"
              className="flex-1 rounded-md border bg-background px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary"
            />
            <button
              type="submit"
              disabled={commentLoading}
              className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:opacity-90 disabled:opacity-50"
            >
              등록
            </button>
          </form>
        ) : (
          <p className="mb-4 text-sm text-muted-foreground">
            <Link to="/login" className="text-primary hover:underline">
              로그인
            </Link>{" "}
            후 댓글을 작성할 수 있습니다.
          </p>
        )}

        {commentsLoading ? (
          <p className="text-sm text-muted-foreground">댓글 불러오는 중...</p>
        ) : comments.length === 0 ? (
          <p className="text-sm text-muted-foreground">아직 댓글이 없습니다.</p>
        ) : (
          <ul className="space-y-3">
            {comments.map((c) => {
              const canDelete = user && (user.memberId === c.member_id || isAdmin);
              return (
                <li key={c.id} className="rounded-md border bg-background p-3">
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0 flex-1">
                      <div className="text-xs text-muted-foreground">
                        #{c.member_id} · {formatDate(c.created_at)}
                      </div>
                      <p className="mt-1 whitespace-pre-wrap break-words text-sm">
                        {c.content}
                      </p>
                    </div>
                    {canDelete && (
                      <button
                        onClick={() => onDeleteComment(c.id)}
                        className="shrink-0 rounded-md border px-2 py-1 text-xs text-muted-foreground hover:bg-accent"
                      >
                        삭제
                      </button>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </section>
    </div>
  );
}