#!/usr/bin/env bash
# morning.sh: start the day. Make today's note, back up all notes,
# and delete backups older than a week.
set -euo pipefail

notes_dir="${1:-$HOME/sandbox/notes}"
backup_dir="$HOME/sandbox/backups"
today="$(date +%F)"
note="$notes_dir/$today.md"

if [[ ! -d "$notes_dir" ]]; then
  echo "morning: no notes folder at $notes_dir" >&2
  exit 1
fi

if [[ -f "$note" ]]; then
  echo "Today's note already exists"
else
  echo "# Notes for $today" > "$note"
  echo "Created $note"
fi

mkdir -p "$backup_dir"
archive="$backup_dir/notes-$today.tar.gz"
tar -czf "$archive" -C "$notes_dir" .
echo "Backed up to $archive"

find "$backup_dir" -name 'notes-*.tar.gz' -mtime +7 -print -delete

for file in "$notes_dir"/*.md; do
  echo "$(wc -w < "$file") words in $(basename "$file")"
done
