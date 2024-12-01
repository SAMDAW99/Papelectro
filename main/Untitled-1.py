file_path = "db_utf8.json"

with open(file_path, "rb") as f:
    content = f.read()

# Remove BOM if it exists
if content.startswith(b'\xef\xbb\xbf'):
    content = content[3:]

with open(file_path, "wb") as f:
    f.write(content)

print("BOM removed successfully!")
