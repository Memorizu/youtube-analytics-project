from src.video import Video


class PLVideo(Video):

    def __init__(self, video_id: str, pl_id: str) -> None:
        super().__init__(video_id)
        self.pl_id = pl_id

