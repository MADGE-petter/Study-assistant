from src.database.db_manager import DatabaseManager
import os

db_path = os.path.join(os.path.dirname(os.path.abspath('main.py')), 'study_assistant.db')
db = DatabaseManager(db_path)

# Check notes
print('=== NOTES ===')
notes = db.get_all_notes()
for note in notes:
    print(f'ID: {note[0]}, Title: {note[1]}')

print()
print('=== SUMMARIES ===')
summaries = db.get_all_note_summaries()
for summary in summaries:
    print(f'Summary ID: {summary[0]}, Note ID: {summary[1]}, Title: {summary[2]}')

print()
print('=== LOOKING FOR "trường" ===')
for note in notes:
    if 'trường' in note[1].lower():
        print(f'Found note: ID={note[0]}, Title={note[1]}')
        # Check if this note has summaries
        note_summaries = db.get_note_summaries_by_note_id(note[0])
        print(f'Summaries for this note: {len(note_summaries)}')
        for ns in note_summaries:
            print(f'  - Summary ID: {ns[0]}, Created: {ns[5]}')
