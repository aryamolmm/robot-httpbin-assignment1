# Python script to extract lines with "Wi-Fi" from a text file

# Open the file and read lines
with open("wifi_paragraph.txt", "r") as file:
    for line in file:
        if "Wi-Fi" in line:
            print(line.strip())