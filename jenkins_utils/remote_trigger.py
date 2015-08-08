import time
import json
import re
import jenkins

from six.moves.urllib.request import Request
from six.moves.http_client import BadStatusLine
from six.moves.urllib.error import HTTPError
from six.moves.urllib.request import Request, urlopen


class JenkinsManExcetion(jenkins.JenkinsException):
    pass

class MultipleMatches(JenkinsManExcetion):
    pass


class BuildHandleError(JenkinsManExcetion):
    pass


class BuildTimeOutError(JenkinsManExcetion):
    pass

# default timeout values
JENKINS_CALL_TIME_OUT=10
BUILD_START_TIME_OUT=BUILD_QUEUE_TIME_OUT=10
BUILD_EXECUTION_TIME_OUT=90

class JenkinsJob(jenkins.Jenkins):
    def __init__(self, job_name,jenkins_url,
                 user=None,password=None,
                 timeout=JENKINS_CALL_TIME_OUT,
                 queue_timeout=BUILD_QUEUE_TIME_OUT,
                 start_timeout=BUILD_START_TIME_OUT,
                 execution_timeout=BUILD_EXECUTION_TIME_OUT,
                 ):
        super(JenkinsJob,self).__init__(jenkins_url, user, password,timeout)
        # self.current_build_number = self.get_job_info(name)['lastBuild']['number']
        self.name = job_name
        self.validate_job_name()
        self.queue_timeout=queue_timeout
        self.start_timeout=start_timeout
        self.execution_timeout=execution_timeout
        self.build_status = "UNKNOWN"
        self._info = None
        self._job_build_info = None

    def validate_job_name(self):
        matches = self.get_all_matching_jobs(self.name)
        if not matches:
            raise jenkins.NotFoundException("No job found by name {}".format(JOB_NAME))
        if len(matches) > 1:
            raise MultipleMatches("Multiple match found: {}, be specific ".format(matches))

        url=matches[0]
        self.name = url[url.index('job')+4:]
        self._info= self.get_job_info(self.name)

    def get_info_at_path(self,path):
        try:
            return json.loads(self.jenkins_open(
                Request(path+jenkins.INFO)))
        except (HTTPError, BadStatusLine):
            raise jenkins.BadHTTPException("Error communicating with server[%s]"
                                   % self.server)
        except ValueError:
            raise jenkins.JenkinsException("Could not parse JSON info for server[%s]"
                                   % self.server)

    def get_jobs_at_path(self, path):
        return self.get_info_at_path(path)['jobs']

    def get_all_matching_jobs(self,pattern,path=None):
        jobs=[]
        path = path or self.server
        for job in self.get_jobs_at_path(path):
            if 'color' not in job:
                jobs.extend(self.get_all_matching_jobs(pattern,job['url']))
            elif re.search(pattern, job['name']):
                jobs.append(job['url'])
        return jobs

    @property
    def info(self,depth=0):
        if not self._info:
            self.update_info(depth)
        return self._info

    def update_info(self,depth=0):
        self._info = self.get_job_info(self.name, depth)

    @property
    def next_build_number(self):
        self.update_info()
        return self.info['nextBuildNumber']

    @property
    def job_queue_info(self):
        self.update_info()
        return self.info['queueItem']

    def update_job_build_info(self):
        self._job_build_info = self.get_build_info(self.name,self.build_number)
        return self._job_build_info

    @property
    def job_build_info(self):
        return self._job_build_info if self._job_build_info else self.update_job_build_info()

    @property
    def build_result(self):
        self.update_job_build_info()
        return self.job_build_info['result']

    def build(self):
        if self.is_build_queued():
            print "Build already in queue...am going to monitor"
            self.build_number  = self.next_build_number
        else:
            expected_build_number = self.next_build_number
            print "Triggering build no \"{}\" of downstream job {}".format(expected_build_number, self.info['url'])
            self.build_job(self.name)
            self.build_number = expected_build_number
            result = self.wait_for_build_result()
            print "Down stream job BUILD RESULT :: {}".format(result)

    def is_build_queued(self):
        if self.job_queue_info:
            self.build_status = "QUEUED"
            return True
        return False


    def wait_for_queue_update(self):
        for _ in range(0,self.queue_timeout):
            if self.is_build_started() or self.is_build_queued():
                return self.build_status
            else:
                time.sleep(1)
        raise BuildTimeOutError("Build neither queued nor started even after {} secs".format(self.queue_timeout))

    def is_build_started(self):
        try:
            if self.job_build_info:
                self.build_status = "STARTED"
            return True
        except jenkins.NotFoundException:
            return False

    def wait_for_build_to_start(self):
        if not self.is_build_queued:
            print "Waiting to be QUEUED..."
            self.wait_for_queue_update()

        print "Waiting to be STARTED..."
        for _ in range(0,self.start_timeout):
            if self.is_build_started():
                return self.build_status
            time.sleep(1)

        raise BuildTimeOutError("Build not started even after {} secs".format(self.start_timeout))

    @property
    def build_result(self):
        return self.get_build_info(self.name,self.build_number)['result']


    def wait_for_build_result(self):
        pause_between_check = 10
        if self.build_status != "STARTED":
            self.wait_for_build_to_start()

        print "BUILD_STARTED :: {}".format(self.job_build_info['url'])
        print "Waiting for Build Result ...."
        for _ in range(0,self.execution_timeout/pause_between_check):
            if self.build_result: return self.build_result
            time.sleep(pause_between_check)
        raise BuildTimeOutError("Build is not finished even after {} secs".format(self.execution_timeout))



if __name__ == "__main__":
    JENKINS_URL = 'http://localhost:8080/'
    USER='jp'
    PASSWORD='jp123'
    JOB_NAME = "apitest"
    jj = JenkinsJob(JOB_NAME,JENKINS_URL,USER,PASSWORD)
    jj.build()

