resource "aws_lambda_function" "bin_collection" {
  filename         = data.archive_file.bin_collections.output_path
  function_name    = var.project_name
  role             = aws_iam_role.bin_collections.arn
  handler          = "get_bins.main"
  source_code_hash = data.archive_file.bin_collections.output_base64sha256
  runtime          = var.runtime
  layers           = [data.aws_lambda_layer_version.requests.arn]
  architectures    = ["arm64"]
  timeout          = "60"

  environment {
    variables = {
      UPRN                  = var.uprn
      SNS_TOPIC             = "arn:aws:sns:${var.region}:${data.aws_caller_identity.current.account_id}:${var.sns_topic_name}"
      NOTIFICATIONS_ENABLED = var.notifications_enabled
    }
  }
}