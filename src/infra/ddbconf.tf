resource "aws_dynamodb_table" "test_table" {
  name           = "sqsqueries"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "message"

  attribute {
    name = "message"
    type = "S"
  }
}
