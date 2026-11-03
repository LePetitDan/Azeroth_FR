#!/bin/bash
# usage: log.sh "message"
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') | $*" >> /home/claude/coa-fr/collecte/site-coa/journal.txt
