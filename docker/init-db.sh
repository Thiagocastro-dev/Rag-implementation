#!/bin/sh
    set -e
    
    # Wait for CouchDB to be ready
    echo "Waiting for CouchDB to start..."
    until curl -s http://couchdb:5984/ > /dev/null; do
        sleep 1
    done
    
    # Create database and indexes
    curl -X PUT http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@couchdb:5984/text_mpc
    
    # Create indexes
    curl -X POST http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@couchdb:5984/text_mpc/_index \
      -H "Content-Type: application/json" \
      -d '{
        "index": {
          "fields": ["content"]
        },
        "name": "content-index",
        "type": "json"
      }'
    
    curl -X POST http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@couchdb:5984/text_mpc/_index \
      -H "Content-Type: application/json" \
      -d '{
        "index": {
          "fields": ["tags"]
        },
        "name": "tags-index",
        "type": "json"
      }'
    
    echo "Database initialization completed successfully"
