#include "SearchEngine.h"
#include <iostream>

int main() {
    SearchEngine searchEngine;

    std::string command;
    while (true) {
        std::cout << "Enter command (add/search/exit): ";
        std::cin >> command;

        if (command == "add") {
            std::string filePath;
            std::cout << "Enter file path: ";
            std::cin >> filePath;
            searchEngine.addFile(filePath);
            std::cout << "File added.\n";
        } else if (command == "search") {
            std::string query;
            std::cout << "Enter search query: ";
            std::cin >> query;
            std::vector<std::string> results = searchEngine.search(query);
            if (!results.empty()) {
                for (const std::string& result : results) {
                    std::cout << result << std::endl;
                }
            } else {
                std::cout << "No results found.\n";
            }
        } else if (command == "exit") {
            break;
        } else {
            std::cout << "Unknown command.\n";
        }
    }

    return 0;
}
