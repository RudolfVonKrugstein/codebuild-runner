# codebuild-runner
Run a codebuild project and print the logs life.

The purpose, for which this project was made, is to start a codebuild project from jenkins and print the build messages life in the jenkins logs.

codebuild-runner does the following:

* zip your source code and upload it to s3
* start a codebuild project
* print the logs from cloudwatch-logs life to stdout
* waits for the project to finish

