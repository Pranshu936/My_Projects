#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <fstream>

class Hangman {
public:
    Hangman() : maxAttempts(6), attemptsLeft(maxAttempts) {
        chooseWord();
        guessedWord = std::string(word.length(), '_');
    }

    void play() {
        char guess;
        bool hintGiven = false;
        bool won = false;

        while (attemptsLeft > 0 && !isWordGuessed()) {
            displayStatus();
            if (!hintGiven && attemptsLeft <= 3) {
                displayHint();
                hintGiven = true;
            }
            std::cout << "Guess a letter: ";
            std::cin >> guess;
            guess = tolower(guess);
            if (std::find(guessedLetters.begin(), guessedLetters.end(), guess) != guessedLetters.end()) {
                std::cout << "You already guessed that letter." << std::endl;
                continue;
            }
            guessedLetters.push_back(guess);
            if (!guessLetter(guess)) {
                std::cout << "Wrong guess!" << std::endl;
            }
        }
        if (isWordGuessed()) {
            std::cout << "Congratulations! You guessed the word: " << word << std::endl;
            won = true;
        } else {
            std::cout << "Game over! The word was: " << word << std::endl;
        }
        int score = getScore();
        std::cout << "Your score: " << score << std::endl;
        std::cout << "Enter your name for the leaderboard: ";
        std::string name;
        std::cin >> name;
        updateLeaderboard(name, score);
        updateStats(won);

        std::cout << "Do you want to see the leaderboard? (y/n): ";
        char showLeaderboard;
        std::cin >> showLeaderboard;
        if (tolower(showLeaderboard) == 'y') {
            displayLeaderboard();
        }
    }

private:
    std::string word;
    std::string guessedWord;
    int maxAttempts;
    int attemptsLeft;
    std::vector<char> guessedLetters;

    void chooseWord() {
        const std::vector<std::string> easyWords = {
            "cat", "dog", "fish", "bird", "ant", "cow", "sheep", "frog", "duck", "wolf",
            "rat", "goat", "pig", "hen", "bee", "owl", "seal", "deer", "bat", "rat",
            "lamb", "fox", "mouse", "camel", "zebra", "horse", "kitten", "puppy", "llama", "panda",
            "swan", "whale", "jellyfish", "beetle", "pigeon", "eagle", "peacock", "tiger", "lion", "bear",
            "shark", "octopus", "monkey", "koala", "giraffe", "penguin", "dolphin", "rabbit", "parrot", "snake"
        };

        const std::vector<std::string> mediumWords = {
            "hangman", "programming", "cplusplus", "function", "variable", "pointer", "iterator", "array", "object", "class",
            "dynamic", "algorithm", "compile", "header", "library", "syntax", "runtime", "compiler", "exception", "inheritance",
            "overload", "operator", "constructor", "destructor", "method", "object", "instance", "template", "parameter", "method",
            "object", "pointer", "reference", "package", "interface", "module", "runtime", "expression", "loop", "recursion",
            "variable", "constant", "thread", "process", "function", "database", "network", "protocol", "server", "client"
        };

        const std::vector<std::string> hardWords = {
            "extraordinary", "unbelievable", "counterproductive", "phenomenal", "incomprehensible", "disproportionate", "antidisestablishmentarianism", "floccinaucinihilipilification", "pseudopseudohypoparathyroidism", "hippopotomonstrosesquipedaliophobia",
            "supercalifragilisticexpialidocious", "psychoneuroimmunology", "subcompartmentalization", "electromagnetically", "counterdemonstration", "incontrovertibility", "counterrevolutionary", "overcompensatory", "misinterpretation", "nonconfrontational",
            "transcontinental", "unscrupulously", "counterproductive", "microspectrophotometer", "multidimensional", "overgeneralization", "counteractiveness", "overcompensate", "interdisciplinary", "neurobiological", "antifilibuster", "extraordinarily",
            "semiautomatic", "unquestionable", "antiestablishment", "microenvironment", "overestimation", "counterintuitive", "intercontinental", "biocompatibility", "unconventional", "misunderstanding", "inflammability", "hypoglycemia", "monochromatic", "misrepresentation", "unexceptional", "proportionality"
        };

        std::cout << "Choose difficulty (1: Easy, 2: Medium, 3: Hard): ";
        int difficulty;
        std::cin >> difficulty;

        std::vector<std::string> wordList;
        switch (difficulty) {
            case 1: wordList = easyWords; break;
            case 2: wordList = mediumWords; break;
            case 3: wordList = hardWords; break;
            default: wordList = mediumWords; break;
        }

        srand(time(0));
        word = wordList[rand() % wordList.size()];
    }

    void displayWord() const {
        std::cout << "Word: ";
        for (char c : guessedWord) {
            std::cout << c << ' ';
        }
        std::cout << std::endl;
    }

    bool guessLetter(char letter) {
        bool found = false;
        for (size_t i = 0; i < word.length(); ++i) {
            if (word[i] == letter) {
                guessedWord[i] = letter;
                found = true;
            }
        }
        if (!found) {
            --attemptsLeft;
        }
        return found;
    }

    bool isWordGuessed() const {
        return guessedWord == word;
    }

    void displayStatus() const {
        std::cout << "Attempts left: " << attemptsLeft << std::endl;
        displayWord();
    }

    void displayHint() const {
        std::cout << "Hint: The word is related to programming." << std::endl;
    }

    int getScore() const {
        int baseScore = 100;
        if (word.length() > 10) {
            baseScore -= 30; // Hard difficulty
        } else if (word.length() > 6) {
            baseScore -= 20; // Medium difficulty
        }
        return baseScore + attemptsLeft * 10; // Bonus for remaining attempts
    }

    void updateLeaderboard(const std::string& playerName, int score) {
        std::ofstream leaderboard("leaderboard.txt", std::ios::app);
        leaderboard << playerName << " - Score: " << score << std::endl;
        leaderboard.close();
    }

    void updateStats(bool won) {
        std::ifstream file("stats.txt");
        int gamesPlayed = 0, wins = 0, losses = 0;
        if (file.is_open()) {
            file >> gamesPlayed >> wins >> losses;
            file.close();
        }
        if (won) {
            ++wins;
        } else {
            ++losses;
        }
        ++gamesPlayed;
        std::ofstream outFile("stats.txt");
        outFile << gamesPlayed << " " << wins << " " << losses << std::endl;
        outFile.close();
    }

    void displayLeaderboard() const {
        std::ifstream leaderboard("leaderboard.txt");
        if (!leaderboard.is_open()) {
            std::cout << "No leaderboard data available." << std::endl;
            return;
        }

        std::cout << "Leaderboard:" << std::endl;
        std::string line;
        while (std::getline(leaderboard, line)) {
            std::cout << line << std::endl;
        }
        leaderboard.close();
    }
};

int main() {
    Hangman game;
    game.play();
    return 0;
}
