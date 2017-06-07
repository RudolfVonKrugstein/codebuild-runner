import boto3

class LogsWatcher:
    def __init__(self,logGroupName,logStreamName):
        self.client = boto3.client('logs')
        self.logGroupName = logGroupName
        self.logStreamName = logStreamName
        self.lastTimeStamp = None

    def getNewLogEvents(self):
        if self.lastTimeStamp == None:
            logs = self.client.get_log_events(logGroupName=self.logGroupName,logStreamName=self.logStreamName)
        else:
            logs = self.client.get_log_events(logGroupName=self.logGroupName,logStreamName=self.logStreamName,startTime=(self.lastTimeStamp+1))
        # update timestamp
        events = logs['events']
        if len(events) > 0:
            self.lastTimeStamp = events[-1]["timestamp"]
        # return list of log strings
        return map(lambda e: e['message'], events)

    def printLogEvents(self,events):
        for e in events:
            print(e.rstrip())
