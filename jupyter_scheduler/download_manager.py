from multiprocessing import Queue
from typing import List, Optional

from jupyter_scheduler.models import DescribeDownload
from jupyter_scheduler.orm import Download, create_session, generate_uuid
from jupyter_scheduler.utils import get_utc_timestamp
from jupyter_scheduler.pydantic_v1 import BaseModel


class DownloadRecordManager:
    def __init__(self, db_url):
        self.session = create_session(db_url)

    def put(self, download: DescribeDownload):
        with self.session() as session:
            download = Download(**download.dict())
            session.add(download)
            session.commit()

    def get(self, download_id: str) -> Optional[DescribeDownload]:
        with self.session() as session:
            download = session.query(Download).filter(Download.download_id == download_id).first()

        if download:
            return DescribeDownload.from_orm(download)
        else:
            return None

    def get_downloads(self) -> List[DescribeDownload]:
        with self.session() as session:
            return session.query(Download).order_by(Download.download_initiated_time).all()

    def delete_download(self, download_id: str):
        with self.session() as session:
            session.query(Download).filter(Download.download_id == download_id).delete()
            session.commit()

    def delete_job_downloads(self, job_id: str):
        with self.session() as session:
            session.query(Download).filter(Download.job_id == job_id).delete()
            session.commit()


class DownloadManager:
    def __init__(self, db_url: str):
        self.record_manager = DownloadRecordManager(db_url=db_url)
        self.queue = Queue()

    def download_from_staging(self, job_id: str, redownload: bool):
        download_initiated_time = get_utc_timestamp()
        download_id = generate_uuid()
        download = DescribeDownload(
            job_id=job_id,
            download_id=download_id,
            download_initiated_time=download_initiated_time,
            redownload=redownload,
        )
        self.record_manager.put(download)
        self.queue.put(download)

    def delete_download(self, download_id: str):
        self.record_manager.delete_download(download_id)

    def delete_job_downloads(self, job_id: str):
        self.record_manager.delete_job_downloads(job_id)

    def populate_queue(self):
        downloads = self.record_manager.get_downloads()
        for download in downloads:
            self.queue.put(download)
