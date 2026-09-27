public class Correct {
    static String label(String value) {
        return switch (value) {
            case null -> "missing";
            case "ok" -> "ok";
            default -> "other";
        };
    }

    public static void main(String[] args) {
        System.out.println(label(null));
    }
}
