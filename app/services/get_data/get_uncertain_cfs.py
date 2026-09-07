from app.base import GetCfs


class GetUncertainCFS(GetCfs):

    @staticmethod
    def get(cfs_id: str | None):
        ...