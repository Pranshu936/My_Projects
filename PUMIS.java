import java.io.*;
import java.util.InputMismatchException;
import java.util.Scanner;

/**
 * Student Management System (PUMIS: Personalized University Management
 * Information System)
 * This program manages student records using a CSV file and maintains a unique
 * ID counter.
 */
public class PUMIS {
    private static int idcounter; // Counter to generate unique student IDs
    private static final String FILENAME = "students.csv"; // File to store student data
    private static final String ID_FILE = "last_used_id.txt"; // File to store last used ID
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        // Initialize idcounter from file or start from 1001 if file doesn't exist
        initializeIDCounter();

        boolean exit = false;

        while (!exit) {
            // Display menu options
            System.out.println("\nStudent Management System Menu:");
            System.out.println("1. Add Student");
            System.out.println("2. Display All Students");
            System.out.println("3. Search Student by ID");
            System.out.println("4. Update Student Information");
            System.out.println("5. Delete Student by ID");
            System.out.println("6. Exit");
            System.out.print("Enter your choice: ");

            int choice = getIntInput(); // Read user choice

            switch (choice) {
                case 1:
                    addStudent();
                    break;
                case 2:
                    displayAllStudents();
                    break;
                case 3:
                    searchStudentByID();
                    break;
                case 4:
                    updateStudent();
                    break;
                case 5:
                    deleteStudentByID();
                    break;
                case 6:
                    exit = true;
                    System.out.println("Exiting... Thank you!");
                    break;
                default:
                    System.out.println("Invalid choice. Please enter a number between 1 and 6.");
            }
        }

        scanner.close(); // Close the scanner object
    }

    // Utility method to get integer input from user
    private static int getIntInput() {
        while (true) {
            try {
                return scanner.nextInt();
            } catch (InputMismatchException e) {
                System.out.print("Invalid input. Please enter a number: ");
                scanner.next(); // Consume invalid input
            } finally {
                scanner.nextLine(); // Consume newline character
            }
        }
    }

    // Initialize idcounter from file or start from 1001 if file doesn't exist
    private static void initializeIDCounter() {
        try (BufferedReader reader = new BufferedReader(new FileReader(ID_FILE))) {
            String lastID = reader.readLine();
            if (lastID != null && !lastID.isEmpty()) {
                idcounter = Integer.parseInt(lastID);
            } else {
                idcounter = 1001; // Default starting ID
            }
        } catch (IOException | NumberFormatException e) {
            System.err.println("Error initializing ID counter: " + e.getMessage());
            idcounter = 1001; // Default starting ID
        }
    }

    // Method to store the last used ID back to the file
    private static void storeLastUsedID() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(ID_FILE))) {
            writer.write(String.valueOf(idcounter));
        } catch (IOException e) {
            System.err.println("Error storing last used ID: " + e.getMessage());
        }
    }

    // Method to add a new student
    private static void addStudent() {
        int id = idcounter++;

        String name;
        boolean validInput = false;
        while (!validInput) {
            System.out.print("Enter student name: ");
            name = scanner.nextLine().trim(); // Read and trim input

            // Validate the input
            if (isValidName(name)) {
                try (BufferedWriter writer = new BufferedWriter(new FileWriter(FILENAME, true))) {
                    writer.write(id + "," + name + "\n");
                    System.out.println("Student added successfully.");
                    validInput = true;
                } catch (IOException e) {
                    System.err.println("Error writing to file: " + e.getMessage());
                }
            } else {
                System.out.println("Invalid name. Please enter a valid name (only alphabetic characters).");
            }
        }

        // Update the last used ID after adding a student
        storeLastUsedID();
    }

    // Method to validate if a name contains only alphabetic characters
    private static boolean isValidName(String name) {
        // Allow alphabetic characters and spaces
        return name.matches("[a-zA-Z ]+");
    }

    // Method to display all students
    private static void displayAllStudents() {
        try (BufferedReader reader = new BufferedReader(new FileReader(FILENAME))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 2) {
                    int id = Integer.parseInt(parts[0]);
                    String name = parts[1];
                    System.out.println("ID: " + id + ", Name: " + name);
                }
            }
        } catch (IOException | NumberFormatException e) {
            System.err.println("Error reading from file: " + e.getMessage());
        }
    }

    // Method to search for a student by ID
    private static void searchStudentByID() {
        System.out.print("Enter student ID to search: ");
        int id = getIntInput(); // Get student ID from user input

        boolean found = false;
        try (BufferedReader reader = new BufferedReader(new FileReader(FILENAME))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 2 && Integer.parseInt(parts[0]) == id) {
                    String name = parts[1];
                    System.out.println("Student found:");
                    System.out.println("ID: " + id + ", Name: " + name);
                    found = true;
                    break;
                }
            }
            if (!found) {
                System.out.println("Student not found with ID: " + id);
            }
        } catch (IOException | NumberFormatException e) {
            System.err.println("Error reading from file: " + e.getMessage());
        }
    }

    // Method to update student information
    private static void updateStudent() {
        System.out.print("Enter student ID to update: ");
        int id = getIntInput(); // Get student ID from user input

        boolean found = false;
        try (BufferedReader reader = new BufferedReader(new FileReader(FILENAME));
                BufferedWriter writer = new BufferedWriter(new FileWriter("students_temp.csv"))) {

            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 2 && Integer.parseInt(parts[0]) == id) {
                    System.out.print("Enter new name for student: ");
                    String newName = scanner.nextLine().trim(); // Get new name from user input

                    // Validate the input
                    if (isValidName(newName)) {
                        writer.write(id + "," + newName + "\n");
                        System.out.println("Student information updated successfully.");
                        found = true;
                    } else {
                        System.out.println("Invalid name. Please enter a valid name (only alphabetic characters).");
                        writer.write(line + "\n"); // Keep the original line in the temp file
                    }
                } else {
                    writer.write(line + "\n");
                }
            }
        } catch (IOException | NumberFormatException e) {
            System.err.println("Error updating student information: " + e.getMessage());
            return; // Exit method on error
        }

        if (!found) {
            System.out.println("Student not found with ID: " + id);
            return; // Exit method if student not found
        }

        // Replace original students.csv with students_temp.csv
        try {
            File originalFile = new File(FILENAME);
            File tempFile = new File("students_temp.csv");

            if (originalFile.delete()) { // Delete original students.csv
                if (tempFile.renameTo(originalFile)) {
                    System.out.println("File renamed successfully.");
                } else {
                    System.err.println("Failed to rename file.");
                }
            } else {
                System.err.println("Failed to delete original file.");
            }
        } catch (Exception e) {
            System.err.println("Error renaming file: " + e.getMessage());
        }

        // Update the last used ID after updating a student
        storeLastUsedID();
    }

    // Method to delete a student by ID
    private static void deleteStudentByID() {
        System.out.print("Enter student ID to delete: ");
        int id = getIntInput(); // Get student ID from user input

        boolean found = false;
        try (BufferedReader reader = new BufferedReader(new FileReader(FILENAME));
                BufferedWriter writer = new BufferedWriter(new FileWriter("students_temp.csv"))) {

            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 2 && Integer.parseInt(parts[0]) == id) {
                    System.out.println("Student deleted successfully.");
                    found = true;
                } else {
                    writer.write(line + "\n");
                }
            }
        } catch (IOException | NumberFormatException e) {
            System.err.println("Error deleting student: " + e.getMessage());
            return; // Exit method on error
        }

        if (!found) {
            System.out.println("Student not found with ID: " + id);
            return; // Exit method if student not found
        }

        // Replace original students.csv with students_temp.csv
        try {
            File originalFile = new File(FILENAME);
            File tempFile = new File("students_temp.csv");

            if (originalFile.delete()) { // Delete original students.csv
                if (tempFile.renameTo(originalFile)) {
                    System.out.println("File renamed successfully.");
                } else {
                    System.err.println("Failed to rename file.");
                }
            } else {
                System.err.println("Failed to delete original file.");
            }
        } catch (Exception e) {
            System.err.println("Error renaming file: " + e.getMessage());
        }
    }
}