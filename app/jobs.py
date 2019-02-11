from flask_rq2 import RQ
from rq.job import Job
from rq.exceptions import NoSuchJobError

def job_fetch(self, id):
	"""Job fetch patch to flask_rq2"""
    job = False, None
    try:
        job = True, Job.fetch(id, connection=rq_instance.connection)
    except NoSuchJobError as e:
        job = False, str(e)
    except Exception as e:
        job = False, str(e)
    return job
# class method injection
RQ.job_fetch = job_fetch

rq_instance = RQ()

def queue_job_with_connection(job, connection, *args, _queue_name=None, **kwargs):
	"""Queue a job inside another job with connection provided"""
    if not connection:
        return job

    from rq import Queue
    
    if not _queue_name:
        _queue_name = job.helper.queue_name

    rq_queue = Queue(
        name=_queue_name,
        connection=connection,
        is_async=True
        # job_class='flask_rq2.job.FlaskJob'
    )
    
    job = rq_queue.enqueue(
        job.helper.wrapped,
        args=args,
        timeout=job.helper.timeout,
        result_ttl=job.helper.result_ttl,
        ttl=job.helper.ttl,
        depends_on=job.helper._depends_on,
        at_front=job.helper._at_front,
        meta=job.helper._meta,
        description=job.helper._description
    )
    
    return job