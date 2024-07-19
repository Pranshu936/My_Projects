import java.util.Scanner;
import java.util.Random;

public class TypingSpeedTest {
    private static final String[] SUBJECTS = {
        "The quick brown fox", "A lazy dog", "A fast cheetah", "An old turtle", "A young kitten",
        "The curious cat", "A wise owl", "A tiny mouse", "The playful puppy", "A brave lion"
    };
    private static final String[] VERBS = {
        "jumps over", "runs around", "crawls under", "leaps across", "sprints towards",
        "flies above", "dashes through", "hops over", "trots along", "strolls across"
    };
    private static final String[] OBJECTS = {
        "a lazy dog", "a tall fence", "a wide river", "a steep hill", "a deep valley",
        "a narrow bridge", "a rocky path", "a grassy field", "a dense forest", "a sandy beach"
    };
    private static final String[] ADVERBS = {
        "quickly", "slowly", "gracefully", "clumsily", "eagerly",
        "reluctantly", "boldly", "shyly", "enthusiastically", "cautiously"
    };
    private static final String[] ADJECTIVES = {
        "beautiful", "elegant", "enormous", "tiny", "colorful",
        "dull", "bright", "dark", "shiny", "matte"
    };

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            String generatedText = generateRandomText();

            System.out.println("Welcome to the Typing Speed Test!");
            System.out.println("\nType the following text and press Enter:");
            System.out.println(generatedText);
            System.out.println();

            long startTime = System.currentTimeMillis();

            String userInput = scanner.nextLine();

            long endTime = System.currentTimeMillis();

            double timeTakenInSeconds = (endTime - startTime) / 1000.0;
            double wordsTyped = userInput.split("\\s+").length;
            double wpm = (wordsTyped / timeTakenInSeconds) * 60;

            int correctCharacters = 0;
            int minLength = Math.min(userInput.length(), generatedText.length());
            int errors = Math.abs(userInput.length() - generatedText.length());

            for (int i = 0; i < minLength; i++) {
                if (userInput.charAt(i) == generatedText.charAt(i)) {
                    correctCharacters++;
                } else {
                    errors++;
                }
            }
            double accuracy = ((double) correctCharacters / generatedText.length()) * 100;

            System.out.println();
            System.out.println("Time taken: " + timeTakenInSeconds + " seconds");
            System.out.println("Words per minute (WPM): " + wpm);
            System.out.println("Accuracy: " + accuracy + "%");
            System.out.println("Number of errors: " + errors);

            System.out.println("\nDo you want to retry? (yes/no): ");
            String retry = scanner.nextLine().trim().toLowerCase();
            if (!retry.equals("yes")) {
                break;
            }
        }

        scanner.close();
    }

    private static String generateRandomText() {
        Random random = new Random();
        String subject = SUBJECTS[random.nextInt(SUBJECTS.length)];
        String verb = VERBS[random.nextInt(VERBS.length)];
        String object = OBJECTS[random.nextInt(OBJECTS.length)];
        String adverb = ADVERBS[random.nextInt(ADVERBS.length)];
        String adjective = ADJECTIVES[random.nextInt(ADJECTIVES.length)];
        
        return subject + " " + verb + " " + object + " " + adverb + " " + adjective + ".";
    }
}
