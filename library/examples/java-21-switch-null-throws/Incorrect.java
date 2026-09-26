public class Incorrect {
    static String label(String value) {
        return switch (value) {
            case "ok" -> "ok";
            default -> "other";
        };
    }

    public static void main(String[] args) {
        try {
            System.out.println(label(null));
        } catch (NullPointerException ex) {
            System.out.println("npe");
        }
    }
}
