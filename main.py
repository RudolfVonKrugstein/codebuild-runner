#!/bin/env python

import CodeBuildHandler
import LogsWatcher
import sys
import time
import getopt

def main():
    #parse command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:],"",["project-name=","source-path=","source-excludes="])
    except getopt.GetoptError:
        print("Usage: main.py --project-name <codebuild-project-name> --source-path <source-path> --source-excludes <comma-seperated-excludes>")
        sys.exit(2)

    sourcePath = "."
    sourceExcludes = [".git"]
    projectName = None

    for opt, arg in opts:
        if opt == "--source-path":
            sourcePath = arg
        if opt == "--source-excludes":
            sourceExcludes = arg.split(",")
        if opt == "--project-name":
            projectName = arg

    print("Using project: %s" % (projectName,))
    print("Using source folder: %s" % (sourcePath,))
    print("Using source excludes: %s" % (sourceExcludes,))

    # create the code build handler
    cbHandler = CodeBuildHandler.CodeBuildHandler(projectName)
    cbHandler.prepareBuild(sourcePath,sourceExcludes)

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

    cbHandler.cleanupBuild()
    print("Finished, exiting")
    cbHandler.printSummary()
    # return result
    exit(not cbHandler.didBuildSucceed())

if __name__ == "__main__":
    main()
