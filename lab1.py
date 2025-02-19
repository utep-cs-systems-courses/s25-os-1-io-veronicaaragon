import os
import sys

def clean_word(word):
    return "".join(c for c in word if c.isalpha()) # only keep letters

def read_file(fd):
    word_count = {}
    
    while True:
        data = os.read(fd, 1024).decode("utf-8")  # read file & convert to string
        if not data:
            break  # nothing left to read

        data = data.lower()  # lowercase
        words = data.split()  # split into words

        for word in words:
            cleaned_word = clean_word(word)  # remove punctuation and digits
            if cleaned_word:
                word_count[cleaned_word] = word_count.get(cleaned_word, 0) + 1

    return word_count

def write_output(fd, word_count):
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True) #sort by count in descending order
    
    for word, count in sorted_words:
        line = f"{word} {count}\n".encode("utf-8")  # Encode to bytes
        os.write(fd, line)

def main():
    if len(sys.argv) != 3: # check correct number of arguments
        os.write(2, b"Use: python3 lab1.py input.txt output.txt\n")
        sys.exit(1)

    input_file, output_file = sys.argv[1], sys.argv[2]

    try:
        fd_in = os.open(input_file, os.O_RDONLY)
    except FileNotFoundError:
        os.write(2, b"Error: Input file not found\n")
        sys.exit(1)

    word_count = read_file(fd_in)
    os.close(fd_in)

    fd_out = os.open(output_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC) # write/create/clear output file
    write_output(fd_out, word_count)
    os.close(fd_out)

if __name__ == "__main__":
    main()
