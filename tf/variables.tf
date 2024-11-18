variable "region" {
  type        = string
  description = "AWS region to deploy the application in"
}

variable "project_name" {
  type        = string
  description = "Name of the project for this application"
}

variable "runtime" {
  type        = string
  description = "The runtime for the Lambda function"
}

variable "sns_topic_name" {
  type        = string
  description = "Name of the SNS topic to send notifications to"
}

variable "invoke_cron" {
  type        = string
  description = "Cron to determine when to run the bin_collections function"
}

variable "uprn" {
  type        = string
  description = "The UPRN is the area code for the bin collections"
}

variable "notifications_enabled" {
  type        = string
  description = "Set to true or false to toggle notifications being sent"
}