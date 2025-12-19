"""Tests for Scheduler async methods.

These tests verify that the async wrappers correctly delegate to sync methods
and run them in a thread pool to avoid blocking the event loop.
"""

import asyncio
import threading
import pytest
from unittest.mock import MagicMock, patch

from jupyter_scheduler.scheduler import Scheduler
from jupyter_scheduler.models import (
    CreateJob,
    CreateJobDefinition,
    CreateJobFromDefinition,
    CountJobsQuery,
    DescribeJob,
    DescribeJobDefinition,
    ListJobDefinitionsQuery,
    ListJobDefinitionsResponse,
    ListJobsQuery,
    ListJobsResponse,
    Status,
    UpdateJob,
    UpdateJobDefinition,
)


@pytest.fixture
def scheduler(jp_scheduler_db_url, jp_scheduler_root_dir, jp_scheduler_db):
    """Create a scheduler with test database."""
    from jupyter_scheduler.tests.mocks import MockEnvironmentManager

    return Scheduler(
        db_url=jp_scheduler_db_url,
        root_dir=str(jp_scheduler_root_dir),
        environments_manager=MockEnvironmentManager(),
    )


class TestSchedulerAsyncWrappers:
    """Test that async wrappers correctly delegate to sync methods."""

    @pytest.mark.asyncio
    async def test_get_job_async_delegates_to_sync(self, scheduler):
        """get_job_async should call get_job in thread pool."""
        mock_job = MagicMock(spec=DescribeJob)
        scheduler.get_job = MagicMock(return_value=mock_job)

        result = await scheduler.get_job_async("job-123", job_files=True)

        scheduler.get_job.assert_called_once_with("job-123", True)
        assert result == mock_job

    @pytest.mark.asyncio
    async def test_get_job_async_with_job_files_false(self, scheduler):
        """get_job_async should pass job_files=False correctly."""
        mock_job = MagicMock(spec=DescribeJob)
        scheduler.get_job = MagicMock(return_value=mock_job)

        result = await scheduler.get_job_async("job-456", job_files=False)

        scheduler.get_job.assert_called_once_with("job-456", False)
        assert result == mock_job

    @pytest.mark.asyncio
    async def test_list_jobs_async_delegates_to_sync(self, scheduler):
        """list_jobs_async should call list_jobs in thread pool."""
        mock_response = MagicMock(spec=ListJobsResponse)
        scheduler.list_jobs = MagicMock(return_value=mock_response)
        query = ListJobsQuery()

        result = await scheduler.list_jobs_async(query)

        scheduler.list_jobs.assert_called_once_with(query)
        assert result == mock_response

    @pytest.mark.asyncio
    async def test_create_job_async_delegates_to_sync(self, scheduler):
        """create_job_async should call create_job in thread pool."""
        scheduler.create_job = MagicMock(return_value="new-job-id")
        model = MagicMock(spec=CreateJob)

        result = await scheduler.create_job_async(model)

        scheduler.create_job.assert_called_once_with(model)
        assert result == "new-job-id"

    @pytest.mark.asyncio
    async def test_update_job_async_delegates_to_sync(self, scheduler):
        """update_job_async should call update_job in thread pool."""
        scheduler.update_job = MagicMock()
        model = MagicMock(spec=UpdateJob)

        await scheduler.update_job_async("job-123", model)

        scheduler.update_job.assert_called_once_with("job-123", model)

    @pytest.mark.asyncio
    async def test_delete_job_async_delegates_to_sync(self, scheduler):
        """delete_job_async should call delete_job in thread pool."""
        scheduler.delete_job = MagicMock()

        await scheduler.delete_job_async("job-123")

        scheduler.delete_job.assert_called_once_with("job-123")

    @pytest.mark.asyncio
    async def test_count_jobs_async_delegates_to_sync(self, scheduler):
        """count_jobs_async should call count_jobs in thread pool."""
        scheduler.count_jobs = MagicMock(return_value=42)
        query = CountJobsQuery(status=Status.IN_PROGRESS)

        result = await scheduler.count_jobs_async(query)

        scheduler.count_jobs.assert_called_once_with(query)
        assert result == 42

    @pytest.mark.asyncio
    async def test_stop_job_async_delegates_to_sync(self, scheduler):
        """stop_job_async should call stop_job in thread pool."""
        scheduler.stop_job = MagicMock()

        await scheduler.stop_job_async("job-123")

        scheduler.stop_job.assert_called_once_with("job-123")

    @pytest.mark.asyncio
    async def test_get_job_definition_async_delegates_to_sync(self, scheduler):
        """get_job_definition_async should call get_job_definition in thread pool."""
        mock_def = MagicMock(spec=DescribeJobDefinition)
        scheduler.get_job_definition = MagicMock(return_value=mock_def)

        result = await scheduler.get_job_definition_async("def-123")

        scheduler.get_job_definition.assert_called_once_with("def-123")
        assert result == mock_def

    @pytest.mark.asyncio
    async def test_list_job_definitions_async_delegates_to_sync(self, scheduler):
        """list_job_definitions_async should call list_job_definitions in thread pool."""
        mock_response = MagicMock(spec=ListJobDefinitionsResponse)
        scheduler.list_job_definitions = MagicMock(return_value=mock_response)
        query = ListJobDefinitionsQuery()

        result = await scheduler.list_job_definitions_async(query)

        scheduler.list_job_definitions.assert_called_once_with(query)
        assert result == mock_response

    @pytest.mark.asyncio
    async def test_create_job_definition_async_delegates_to_sync(self, scheduler):
        """create_job_definition_async should call create_job_definition in thread pool."""
        scheduler.create_job_definition = MagicMock(return_value="def-456")
        model = MagicMock(spec=CreateJobDefinition)

        result = await scheduler.create_job_definition_async(model)

        scheduler.create_job_definition.assert_called_once_with(model)
        assert result == "def-456"

    @pytest.mark.asyncio
    async def test_update_job_definition_async_delegates_to_sync(self, scheduler):
        """update_job_definition_async should call update_job_definition in thread pool."""
        scheduler.update_job_definition = MagicMock()
        model = MagicMock(spec=UpdateJobDefinition)

        await scheduler.update_job_definition_async("def-123", model)

        scheduler.update_job_definition.assert_called_once_with("def-123", model)

    @pytest.mark.asyncio
    async def test_delete_job_definition_async_delegates_to_sync(self, scheduler):
        """delete_job_definition_async should call delete_job_definition in thread pool."""
        scheduler.delete_job_definition = MagicMock()

        await scheduler.delete_job_definition_async("def-123")

        scheduler.delete_job_definition.assert_called_once_with("def-123")

    @pytest.mark.asyncio
    async def test_create_job_from_definition_async_delegates_to_sync(self, scheduler):
        """create_job_from_definition_async should call create_job_from_definition in thread pool."""
        scheduler.create_job_from_definition = MagicMock(return_value="job-789")
        model = MagicMock(spec=CreateJobFromDefinition)

        result = await scheduler.create_job_from_definition_async("def-123", model)

        scheduler.create_job_from_definition.assert_called_once_with("def-123", model)
        assert result == "job-789"

    @pytest.mark.asyncio
    async def test_get_staging_paths_async_delegates_to_sync(self, scheduler):
        """get_staging_paths_async should call get_staging_paths in thread pool."""
        mock_paths = {"input": "/path/to/input", "ipynb": "/path/to/output.ipynb"}
        scheduler.get_staging_paths = MagicMock(return_value=mock_paths)
        model = MagicMock(spec=DescribeJob)

        result = await scheduler.get_staging_paths_async(model)

        scheduler.get_staging_paths.assert_called_once_with(model)
        assert result == mock_paths


class TestSchedulerAsyncThreading:
    """Test that async methods properly run in thread pool."""

    @pytest.mark.asyncio
    async def test_async_method_runs_in_different_thread(self, scheduler):
        """Verify sync methods run in thread pool, not main thread."""
        main_thread = threading.current_thread()
        call_thread = None

        def capture_thread(*args, **kwargs):
            nonlocal call_thread
            call_thread = threading.current_thread()
            return MagicMock(spec=DescribeJob)

        scheduler.get_job = capture_thread

        await scheduler.get_job_async("job-123")

        # Sync method should run in different thread (thread pool)
        assert call_thread is not None
        assert call_thread != main_thread
        # Thread name varies by Python version and platform (ThreadPoolExecutor* or asyncio_*)
        # Key assertion: it's NOT the main thread

    @pytest.mark.asyncio
    async def test_multiple_async_calls_run_concurrently(self, scheduler):
        """Multiple async calls should run in parallel, not sequentially."""
        import time

        call_times = []

        def slow_get_job(*args, **kwargs):
            call_times.append(time.monotonic())
            time.sleep(0.1)  # Simulate slow operation
            return MagicMock(spec=DescribeJob)

        scheduler.get_job = slow_get_job

        start = time.monotonic()
        # Run 3 async calls concurrently
        await asyncio.gather(
            scheduler.get_job_async("job-1"),
            scheduler.get_job_async("job-2"),
            scheduler.get_job_async("job-3"),
        )
        elapsed = time.monotonic() - start

        # If parallel: ~100ms. If sequential: ~300ms.
        # Allow generous margin for CI variability
        assert elapsed < 0.25, f"Expected parallel execution, but took {elapsed:.3f}s"

        # All calls should have started within a short window (parallel)
        if len(call_times) >= 2:
            start_spread = max(call_times) - min(call_times)
            assert start_spread < 0.05, f"Calls didn't start together: {start_spread:.3f}s spread"


class TestSchedulerAsyncErrorHandling:
    """Test error propagation through async wrappers."""

    @pytest.mark.asyncio
    async def test_exception_propagates_from_sync_to_async(self, scheduler):
        """Exceptions from sync methods should propagate through async wrapper."""
        scheduler.get_job = MagicMock(side_effect=ValueError("test error"))

        with pytest.raises(ValueError, match="test error"):
            await scheduler.get_job_async("job-123")

    @pytest.mark.asyncio
    async def test_scheduler_error_propagates(self, scheduler):
        """SchedulerError should propagate through async wrapper."""
        from jupyter_scheduler.exceptions import SchedulerError

        scheduler.create_job = MagicMock(side_effect=SchedulerError("Job creation failed"))

        with pytest.raises(SchedulerError, match="Job creation failed"):
            await scheduler.create_job_async(MagicMock(spec=CreateJob))

    @pytest.mark.asyncio
    async def test_input_uri_error_propagates(self, scheduler):
        """InputUriError should propagate through async wrapper."""
        from jupyter_scheduler.exceptions import InputUriError

        scheduler.create_job = MagicMock(side_effect=InputUriError("nonexistent.ipynb"))

        with pytest.raises(InputUriError):
            await scheduler.create_job_async(MagicMock(spec=CreateJob))
