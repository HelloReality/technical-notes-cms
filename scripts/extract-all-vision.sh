#!/bin/bash
# Extract content from all 20 webp pages using z-ai vision
set -e
cd /home/z/my-project

PROMPT='Extract ALL text content from this Linux security handbook page exactly as shown. Include EVERY heading, paragraph, command, file path (with its description), table cell (preserve rows AND columns), tip box, warning, note, practical exercise step, footer text, and badge text. Preserve capitalization, punctuation, line breaks, and structure. Output as structured markdown with these sections (skip empty ones): TITLE, SUBTITLE, BADGES, SECTION_HEADINGS, BODY_PARAGRAPHS, IMPORTANT_FILES (with file path AND what it stores), TABLES (with full column headers and ALL rows), COMMANDS (each with command AND description AND example if shown), TIPS_NOTES_WARNINGS (full text), PRACTICAL_EXERCISES (numbered steps with full text and commands), FOOTER_TEXT, PAGE_NUMBER. Be EXHAUSTIVE and LITERAL — do NOT summarize, paraphrase, or omit anything. Every visible word matters.'

for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20; do
  if [ ! -f /home/z/my-project/scripts/vision-out/page${i}.json ] || [ ! -s /home/z/my-project/scripts/vision-out/page${i}.json ]; then
    echo "Extracting page ${i}..."
    z-ai vision -p "$PROMPT" -i /home/z/my-project/downloads/instagram-DcGGtvdFcWk/${i}.webp -o /home/z/my-project/scripts/vision-out/page${i}.json 2>&1 | tail -1
  fi
done
echo "Done."
