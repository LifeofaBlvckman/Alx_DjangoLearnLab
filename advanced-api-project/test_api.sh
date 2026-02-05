#!/bin/bash

echo "=== ALX Generic Views - API Test ==="
echo "Server: http://127.0.0.1:8003/api/"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local method=${3:-GET}
    local data=${4:-""}
    
    echo -n "Testing $name... "
    
    if [ "$method" = "POST" ] || [ "$method" = "PUT" ] || [ "$method" = "DELETE" ]; then
        if [ -n "$data" ]; then
            response=$(curl -s -X "$method" "$url" -H "Content-Type: application/json" -d "$data" -w " %{http_code}")
        else
            response=$(curl -s -X "$method" "$url" -w " %{http_code}")
        fi
    else
        response=$(curl -s -X "$method" "$url" -w " %{http_code}")
    fi
    
    http_code=$(echo "$response" | awk '{print $NF}')
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ PASS ($http_code)${NC}"
        return 0
    elif [ "$http_code" = "401" ] || [ "$http_code" = "403" ]; then
        if [ "$method" = "POST" ] || [ "$method" = "PUT" ] || [ "$method" = "DELETE" ]; then
            echo -e "${GREEN}✅ PASS ($http_code - Permission check working)${NC}"
            return 0
        else
            echo -e "${RED}❌ FAIL ($http_code)${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ FAIL ($http_code)${NC}"
        return 1
    fi
}

# Run tests
echo "1. Testing API Root..."
test_endpoint "API Root" "http://127.0.0.1:8003/api/"

echo -e "\n2. Testing Book List (GET)..."
test_endpoint "Book List" "http://127.0.0.1:8003/api/books/"

echo -e "\n3. Testing Book Detail (GET)..."
test_endpoint "Book Detail" "http://127.0.0.1:8003/api/books/1/"

echo -e "\n4. Testing Book Create (POST - no auth)..."
test_endpoint "Book Create" "http://127.0.0.1:8003/api/books/create/" "POST" '{"title":"Test","publication_year":2020,"author":1}'

echo -e "\n5. Testing Book Update (PUT - no auth)..."
# Note: Using /books/update/ (NOT /books/1/update/)
test_endpoint "Book Update" "http://127.0.0.1:8003/api/books/update/" "PUT" '{"id":1,"title":"Updated"}'

echo -e "\n6. Testing Book Delete (DELETE - no auth)..."
# Note: Using /books/delete/ (NOT /books/1/delete/)
test_endpoint "Book Delete" "http://127.0.0.1:8003/api/books/delete/" "DELETE" '{"id":1}'

echo -e "\n=== Test Complete ==="
