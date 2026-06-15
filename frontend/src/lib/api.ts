import axios, { AxiosError } from "axios";
import { toast } from "sonner";

export const API_BASE_URL = "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

export interface ApiErrorBody {
  status?: number;
  message?: string;
}

export function getErrorMessage(err: unknown): string {
  if (err instanceof AxiosError) {
    const data = err.response?.data as ApiErrorBody | undefined;
    if (data?.message) return data.message;
    const status = err.response?.status;
    if (status === 500) return "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.";
    if (status === 403) return "권한이 없습니다.";
    if (status === 404) return "존재하지 않는 데이터입니다.";
    return err.message || "요청 처리 중 오류가 발생했습니다.";
  }
  if (err instanceof Error) return err.message;
  return "알 수 없는 오류가 발생했습니다.";
}

export function handleApiError(err: unknown): string {
  const msg = getErrorMessage(err);
  toast.error(msg);
  return msg;
}