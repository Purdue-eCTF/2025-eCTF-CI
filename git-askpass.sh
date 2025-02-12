#!/bin/sh
# used for meta-infra
case "$1" in
    Username*) exec echo "$GITHUB_USERNAME" ;;
    Password*) exec echo "$GITHUB_TOKEN" ;;
esac