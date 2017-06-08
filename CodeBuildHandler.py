import boto3
import LogsWatcher
import zip
import time

class CodeBuildHandler:
    def __init__(self,projectName):
        self.client = boto3.client('codebuild')
        self.projectName = projectName
        self.buildResult = None
        self.buildId = None
        self.sourceVersion = None

    def prepareBuild(self,sourcePath,sourceExcludes):
        projectInfo = self.client.batch_get_projects(names=[self.projectName])['projects'][0]
        bucketPath = projectInfo['source']['location']
        print("Zipping current directory")
        binaryZip = zip.zipws(sourcePath,sourceExcludes)
        s3_client = boto3.client('s3')

        bucket=bucketPath.split("/")[0].split(":")[-1]
        key=bucketPath.split("/",1)[1]
        print("Uploading zip to %s/%s" % (bucket,key))
        res = s3_client.put_object(Body=binaryZip, Bucket=bucket, Key=key)
        self.sourceVersion = res['VersionId']
        print("SourceVersion set to %s" % self.sourceVersion)

    def startBuild(self):
        res = self.client.start_build(projectName=self.projectName,sourceVersion=self.sourceVersion)
        self.buildId = res['build']['id']
        # get buildinfo to get log information
        while True: # do this until the logs appear in the output, then exit via return
            buildInfo = self.client.batch_get_builds(ids=[self.buildId])
            if not buildInfo['builds'][0].has_key('logs'):
                print("Waiting for log group to appear ...")
                time.sleep(1)
                continue
            # return log watcher with this info
            return LogsWatcher.LogsWatcher(buildInfo['builds'][0]['logs']['groupName'],buildInfo['builds'][0]['logs']['streamName'])

    def testBuildFinished(self):
       res = self.client.batch_get_builds(ids=[self.buildId]) 
       finished = res['builds'][0]['buildComplete']
       if finished:
           self.buildResult = res['builds'][0]['buildStatus']
       return finished

    def didBuildSucceed(self):
       return self.buildResult == u'SUCCEEDED'

