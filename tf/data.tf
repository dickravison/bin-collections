#Get current account info
data "aws_caller_identity" "current" {}

#Get requests lambda layer version
data "aws_lambda_layer_version" "requests" {
  layer_name = "requests"
}

#Package up python into zip
data "archive_file" "bin_collections" {
  type        = "zip"
  source_dir  = "../src/bin_collections"
  output_path = "../src/bin_collections.zip"
}