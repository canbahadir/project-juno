provider "aws" {
  access_key                  = "mock"
  secret_key                  = "mock"
  region                      = "ap-southeast-1"
  s3_force_path_style         = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    dynamodb       = "http://localhost:4576"
  }
}