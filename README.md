# bin-collections

This is used to retrieve which bins are being collected tomorrow in Manchester, UK. This uses the Manchester City Council website to retrieve this data. The API requires authentication first which is done in the auth function/method?.

This deploys a Lambda function to retrieve the data. It is invoked daily by Eventbridge so that if a collection changes from the usual day, for example around Christmas, this will still be able to send a notification.

The UPRN can be retrieved by inspecting the console output at the Manchester City Council bin collection API.
