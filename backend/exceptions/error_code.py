from enum import Enum


class ErrorCode(Enum):

    DUPLICATE_USERNAME = (
        409,
        "이미 존재하는 아이디입니다."
    )

    MEMBER_NOT_FOUND = (
        404,
        "존재하지 않는 회원입니다."
    )

    INVALID_PASSWORD = (
        401,
        "비밀번호가 일치하지 않습니다."
    )

    BOARD_NOT_FOUND = (
        404,
        "게시글이 존재하지 않습니다."
    )

    COMMENT_NOT_FOUND = (
        404,
        "댓글이 존재하지 않습니다."
    )

    FORBIDDEN = (
        403,
        "권한이 없습니다."
    )

    INTERNAL_SERVER_ERROR = (
        500,
        "서버 오류가 발생했습니다."
    )

    def __init__(self,
                 status_code,
                 message):

        self.status_code = status_code
        self.message = message