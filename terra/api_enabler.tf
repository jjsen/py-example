provider "google" {}

variable "api_to_enable" {
  type        = string
  description = "The API to enable for the projects in the list"
  default     = "monitoring.googleapis.com"
}

variable "input_file" {
  type        = string
  description = "The input file containing the list of projects"
  default     = "list.txt"
}

variable "delay_between_api_calls" {
  type        = string
  description = "The delay between API calls in seconds"
  default     = "5"
}

locals {
  disabled_api_projects = [
    for line in split("\n", file(var.input_file)) :
    trimspace(line) if trimspace(line) != ""
  ]
}

resource "time_sleep" "delay" {
  for_each = toset(local.disabled_api_projects)

  create_duration = "${var.delay_between_api_calls}s"

  triggers = {
    project = each.key
  }
}

resource "google_project_service" "monitoring" {
  for_each = toset(local.disabled_api_projects)

  project = each.key
  service = var.api_to_enable

  disable_dependent_services = true
  disable_on_destroy         = false

  timeouts {
    create = "10m"
  }

  depends_on = [time_sleep.delay]
}
