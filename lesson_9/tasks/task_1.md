# Create pre_request hook which compress body to gzip and add appropriate headers

1. You can use PreRequestHooks class to check your pre_request hook because it not implemented into current requests library
2. If gzip header not set than compress request body to gzip and add a header. Some sample how to do this https://stackoverflow.com/a/54338737
3. If gzip header exists than do not compress again
