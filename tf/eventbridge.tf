#Create Eventbridge rule to invoke Lambda function following cron pattern
resource "aws_cloudwatch_event_rule" "bin_collection" {
  name        = "${var.project_name}_invoke"
  description = "Rule to invoke bin_collection function"

  schedule_expression = var.invoke_cron
}

#Link Eventbridge rule to Lambda function
resource "aws_cloudwatch_event_target" "bin_collection" {
  rule      = aws_cloudwatch_event_rule.bin_collection.name
  target_id = "${var.project_name}_invoke"
  arn       = aws_lambda_function.bin_collection.arn
}
