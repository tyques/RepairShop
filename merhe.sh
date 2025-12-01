#!/bin/sh

# The name of the final combined output file.
outputFile="combined_spring_boot_project.txt"

# Lists are defined as space-separated strings for POSIX sh compatibility.
includedExtensions=".java .kt .yml .sql .js .py .html"
includedFileNames="pom.xml build.gradle settings.gradle"
excludedDirs=".git .idea .vscode target build .gradle out gradle .venv"

fullOutputPath="./$outputFile"

# This command creates an empty file or clears the existing file.
# It is a more efficient way than checking if the file exists and then removing it.
> "$fullOutputPath"

echo "Start: $outputFile"

# Find all files recursively from the current directory.
find . -type f | while read -r file; do
    # Remove the leading "./" from the file path for cleaner output.
    file_path=${file#./}

    # A safety check to ensure the script doesn't try to add its own output file.
    if [ "$file_path" = "$outputFile" ]; then
        continue
    fi

    # Check if the file is within an excluded directory.
    is_in_excluded_dir=false
    for dir in $excludedDirs; do
        # We use a case statement with wildcards to check if the file path
        # contains the directory name as a distinct path component.
        # This is a robust way to check for "/.git/" or "target/", etc.
case "$file_path" in
    "$dir"/*)
        is_in_excluded_dir=true
        break
        ;;
esac
    done

    # If the flag is true, we skip this file and move to the next one.
    if [ "$is_in_excluded_dir" = "true" ]; then
        continue
    fi

    # Get the filename and extension for the inclusion checks.
    file_name=$(basename "$file_path")
    file_ext=".${file_path##*.}"
    # If the file has no extension, the above command results in file_ext being ".filename".
    # This check corrects it to be an empty string.
    if [ "$file_name" = "$file_ext" ]; then
        file_ext=""
    fi

    # Determine if the file should be included.
    include=false

    # First, check if the file name is in our list of included names.
    for name in $includedFileNames; do
        if [ "$file_name" = "$name" ]; then
            include=true
            break
        fi
    done

    # If not already included, check if the extension is in our list.
    if [ "$include" = "false" ]; then
        for ext in $includedExtensions; do
            if [ "$file_ext" = "$ext" ]; then
                include=true
                break
            fi
        done
    fi

    # If the include flag is set to true, we append the file's content.
    if [ "$include" = "true" ]; then
        echo "Adding file: $file_path"

        # Add a header with the full path of the file to the output.
        echo "==================== $file_path ====================" >> "$outputFile"

        # Attempt to add the file's content. If 'cat' fails (e.g., permission denied),
        # it will print a warning and add an error message to the output file.
        if ! cat "$file_path" >> "$outputFile"; then
            echo "Warning: Error reading file: $file_path" >&2
            echo " err" >> "$outputFile"
        fi
        # Add a newline for better spacing between concatenated files.
        echo "" >> "$outputFile"
    fi
done

echo "Done: $outputFile"
