#!/usr/bin/env python3
"""
Process CSV file to add songs to PCO and assign tags.
"""
import csv
import sys
import time
from pco_functions import create_song, find_song_by_title, assign_tags_to_song

def process_csv(csv_file_path):
    """
    Process CSV file and add songs to PCO with tags.

    Args:
        csv_file_path (str): Path to the CSV file
    """
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        total_rows = 0
        created_count = 0
        found_count = 0
        tagged_count = 0
        skipped_count = 0
        error_count = 0

        for row in reader:
            total_rows += 1
            ccli = row.get('CCLI', '').strip()
            title = row.get('Song', '').strip()
            tag = row.get('Tag', '').strip()

            if not title:
                print(f"Row {total_rows}: Skipping - no title")
                skipped_count += 1
                continue

            # Skip if CCLI is missing or invalid
            if not ccli or ccli.upper() == 'MISSING':
                print(f"Row {total_rows}: Skipping '{title}' - CCLI is missing")
                skipped_count += 1
                continue

            print(f"\nRow {total_rows}: Processing '{title}' (CCLI: {ccli})")

            try:
                # Search for song by title
                existing_songs = find_song_by_title(title)

                song_id = None
                if existing_songs:
                    # Found existing song
                    song_id = existing_songs[0]['id']
                    print(f"  ✓ Found existing song (ID: {song_id})")
                    found_count += 1
                else:
                    # Create new song
                    print(f"  → Creating new song...")
                    result = create_song(title, ccli)
                    song_id = result['id']
                    print(f"  ✓ Created song (ID: {song_id})")
                    created_count += 1

                # Assign tag if provided
                if tag and song_id:
                    print(f"  → Assigning tag '{tag}'...")
                    tag_result = assign_tags_to_song(song_id, [tag])
                    if tag_result.get('success'):
                        print(f"  ✓ Tag assigned")
                        tagged_count += 1
                    else:
                        print(f"  ✗ Failed to assign tag: {tag_result.get('message')}")
                        error_count += 1

                # Small delay to avoid rate limiting
                time.sleep(0.5)

            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
                error_count += 1

        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total rows processed: {total_rows}")
        print(f"Songs found:          {found_count}")
        print(f"Songs created:        {created_count}")
        print(f"Tags assigned:        {tagged_count}")
        print(f"Rows skipped:         {skipped_count}")
        print(f"Errors:               {error_count}")
        print("="*60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_songs.py <csv_file_path>")
        sys.exit(1)

    csv_file = sys.argv[1]
    print(f"Processing CSV file: {csv_file}")
    process_csv(csv_file)
