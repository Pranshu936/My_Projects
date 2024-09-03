#pragma once
#include <string>
#include <map>
#include <vector>
#include <fstream>
#include <sstream>
#include <cctype>
#include <algorithm>

// FileIndex class definition and implementation
class FileIndex {
private:
    std::string fileName;
    std::map<std::string, std::vector<int>> wordIndex;

public:
    FileIndex(const std::string& fileName) : fileName(fileName) {}

    void addWordOccurrence(const std::string& word, int position) {
        wordIndex[word].push_back(position);
    }

    const std::map<std::string, std::vector<int>>& getWordIndex() const {
        return wordIndex;
    }

    std::string getFileName() const {
        return fileName;
    }
};

// Indexer class definition and implementation
class Indexer {
public:
    FileIndex indexFile(const std::string& filePath) {
        FileIndex fileIndex(filePath);
        std::ifstream file(filePath);
        std::string line;
        int position = 0;

        while (std::getline(file, line)) {
            std::vector<std::string> words = splitWords(line);
            for (const std::string& word : words) {
                fileIndex.addWordOccurrence(word, position++);
            }
        }

        return fileIndex;
    }

    std::vector<std::string> splitWords(const std::string& line) {
        std::vector<std::string> words;
        std::stringstream ss(line);
        std::string word;

        while (ss >> word) {
            // Remove punctuation and convert to lowercase
            word = cleanWord(word);
            words.push_back(word);
        }

        return words;
    }

    std::string cleanWord(const std::string& word) const {  // Add const qualifier
        std::string cleanedWord;
        for (char c : word) {
            if (!std::ispunct(c)) {
                cleanedWord += std::tolower(c);
            }
        }
        return cleanedWord;
    }
};

// SearchEngine class definition and implementation
class SearchEngine {
private:
    std::vector<FileIndex> fileIndices;
    Indexer indexer;

public:
    void addFile(const std::string& filePath) {
        FileIndex fileIndex = indexer.indexFile(filePath);
        fileIndices.push_back(fileIndex);
    }

    std::vector<std::string> search(const std::string& query) const {
        std::vector<std::string> results;
        std::string cleanQuery = indexer.cleanWord(query);  // No error now
        for (const FileIndex& fileIndex : fileIndices) {
            const std::map<std::string, std::vector<int>>& wordIndex = fileIndex.getWordIndex();
            if (wordIndex.find(cleanQuery) != wordIndex.end()) {
                results.push_back("Found in file: " + fileIndex.getFileName());
            }
        }
        return results;
    }
};
