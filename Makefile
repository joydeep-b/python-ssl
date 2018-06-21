all:proto/referee.proto
	protoc --python_out=protogen proto/referee.proto
