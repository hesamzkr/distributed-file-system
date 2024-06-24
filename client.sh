#!/bin/bash

# usage:
# ./client.sh create_file test.txt
# ./client.sh read_file test.txt

BASE_URL="http://localhost:8000"

create_file() {
    local file_path=$1
    curl -X POST "$BASE_URL/create-file" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@$file_path"
}

read_file() {
    local filename=$1
    curl -X GET "$BASE_URL/read-file/$filename" \
        -H "Accept: application/octet-stream" \
        --output $filename
}

main() {
    case $1 in
        create_file)
            if [ -z "$2" ]; then
                echo "Usage: $0 create_file <file_path>"
                exit 1
            fi
            create_file "$2"
            ;;
        read_file)
            if [ -z "$2" ]; then
                echo "Usage: $0 read_file <filename>"
                exit 1
            fi
            read_file "$2"
            ;;
        *)
            echo "Usage: $0 {create_file|read_file} [args...]"
            exit 1
            ;;
    esac
}

main "$@"
