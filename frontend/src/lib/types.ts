export interface Board {
  id: number;
  member_id: number;
  title: string;
  content: string;
  view_count: number;
  created_at: string;
}

export interface Comment {
  id: number;
  board_id: number;
  member_id: number;
  content: string;
  created_at: string;
}

export interface Member {
  id: number;
  username: string;
  nickname: string;
  role: string;
  created_at: string;
}