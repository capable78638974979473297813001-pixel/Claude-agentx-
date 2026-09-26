---
id: java-21-switch-null-throws
area: languages
topic: java
task: match-null-in-switch
title: A Java 21 switch without case null throws NullPointerException
description: Use when a pattern switch on a nullable String prints npe, and adding case null prints missing.
triggers:
  - switch null NullPointerException
  - case null java 21
  - pattern switch NPE
  - JEP 441 null
aliases:
  - java
  - switch
  - null
related:
  - rust-temporary-dropped-while-borrowed
  - go-nil-pointer-stored-in-interface
sources:
  - https://openjdk.org/jeps/441
commands:
  - python3 library/examples/java-21-switch-null-throws/check.py
---

# A Java 21 switch without case null throws NullPointerException

JEP 441, which Java 21 ships as pattern matching for switch, says a switch throws `NullPointerException` when the selector is null and no `case null` is present. `switch (null)` with only `case "ok"` and `default` prints `npe` under `javac --release 21`.

`case null -> "missing"` is a separate label. It does not fall into `default`. With that label, the same call prints `missing`. The check compiles with `javac --release 21` and compares those two stdout lines.

## Incorrect

```java file=library/examples/java-21-switch-null-throws/Incorrect.java
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
```

## Correct

```java file=library/examples/java-21-switch-null-throws/Correct.java
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
```

## Verify

Run `python3 library/examples/java-21-switch-null-throws/check.py`.

## Sources

- https://openjdk.org/jeps/441
