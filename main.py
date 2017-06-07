import CodeBuildHandler
import LogsWatcher
import sys
import time
import getopt

#parse command line arguments
try:
    opts, args = getopt.getopt(sys.argv[1:],"",["project-name=","source-path="])
except getopt.GetoptError:
    print("Usage: main.py --project-name <codebuild-project-name> --source-path <source-path>")
    sys.exit(2)

sourcePath = "."
projectName = None

for opt, arg in opts:
    if opt == "--source-path":
        sourcePath = arg
    if opt == "--project-name":
        projectName = arg

print("Using project: %s" % (projectName,))
print("Using source folder: %s" % (sourcePath,))

# create the code build handler
cbHandler = CodeBuildHandler.CodeBuildHandler(projectName)
cbHandler.prepareBuild(sourcePath)

logsWatcher = cbHandler.startBuild()

starttime=time.time()
intervalTime = 2.0

while not cbHandler.testBuildFinished():
  time.sleep(intervalTime - ((time.time() - starttime) % intervalTime))
  newEvents = logsWatcher.getNewLogEvents()
  logsWatcher.printLogEvents(newEvents)

# printing remaining logs
newEvents = logsWatcher.getNewLogEvents()
logsWatcher.printLogEvents(newEvents)

print("Finished, exiting")
# return result
exit(not cbHandler.didBuildSucceed())
