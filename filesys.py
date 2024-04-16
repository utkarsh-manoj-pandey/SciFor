def analyze_file(file_path):
    total_lines = 0
    total_words = 0
    total_letters = 0
    lines_starting_with_letter = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                total_lines += 1
                total_words += len(line.split())
                total_letters += len(line)
                first_letter = line.strip()[0].lower()
                if first_letter.isalpha():
                    lines_starting_with_letter[first_letter] = lines_starting_with_letter.get(first_letter, 0) + 1
    except FileNotFoundError:
        print("File not found.")
        return

    print("Total number of lines:", total_lines)
    print("Total number of words:", total_words)
    print("Total number of letters:", total_letters)
    print("Lines starting with each letter:")
    for letter, count in sorted(lines_starting_with_letter.items()):
        print(f"{letter}: {count}")

def create_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except:
        print("Error occurred while creating the file.")

file_path = "sample_file.txt"
file_content = """\
Hello there!
How are you doing?
I hope everything is going well.
Let's analyze this file.
Starting with S.
Sure thing!
"""

create_file(file_path, file_content)
analyze_file(file_path)