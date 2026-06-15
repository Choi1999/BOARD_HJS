import { Link, useNavigate } from "@tanstack/react-router";
import { useAuth, clearAuth } from "@/lib/auth";
import { toast } from "sonner";

export function Header() {
  const { user, isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();

  const onLogout = () => {
    clearAuth();
    toast.success("로그아웃되었습니다.");
    navigate({ to: "/" });
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/80 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-5xl items-center justify-between px-4">
        <Link to="/" className="text-lg font-bold tracking-tight">
          📋 Board
        </Link>
        <nav className="flex items-center gap-2 text-sm">
          {isAuthenticated ? (
            <>
              <span className="hidden sm:inline text-muted-foreground">
                {user?.nickname}님
              </span>
              {isAdmin && (
                <span className="rounded-md bg-primary px-2 py-0.5 text-xs font-semibold text-primary-foreground">
                  ADMIN
                </span>
              )}
              <button
                onClick={onLogout}
                className="rounded-md border px-3 py-1.5 text-sm hover:bg-accent"
              >
                로그아웃
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="rounded-md border px-3 py-1.5 hover:bg-accent"
              >
                로그인
              </Link>
              <Link
                to="/signup"
                className="rounded-md bg-primary px-3 py-1.5 text-primary-foreground hover:opacity-90"
              >
                회원가입
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}