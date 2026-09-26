# What a Text File Is

Before you can process a text file, you need a clear picture of what one is. This chapter gives you that picture: bytes on a disk, an encoding that turns them into characters, and the newline that turns characters into lines.

*The problem.* I open `notes.txt` in an editor and see three short lines. A [hex viewer]{.idx} shows the same file as a row of numbers.

*The question.* Which one is the file, and why does a program that counts lines sometimes disagree with my eyes?

## Bytes First

A **file** is a named sequence of **bytes** stored on a disk. A byte is a number from 0 to 255; nothing more. The file system remembers the name and the length, and it doesn't care what the numbers mean.

A **text file** is a file whose bytes are meant to be read as characters. The rule that maps bytes to characters is the file's **encoding**. Today that is almost always **UTF-8**, which uses one byte for plain English letters and two to four bytes for everything else.

> **Note:** "Plain text" is not a format of its own. It's an agreement between whoever wrote the bytes and whoever reads them: *use UTF-8*. When the two sides disagree, you see garbage such as `cafÃ©` instead of `café`.

Here is the whole idea in one picture. The same three lines, as the disk stores them and as an editor shows them:

```
┌──────────────────────── notes.txt (31 bytes on disk) ────────────────────────┐
│ 74 68 65 20 63 61 74 20 73 61 74 0a 6f 6e 20 74 68 65 20 6d 61 74 0a 74 68 … │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │  decode as UTF-8
                                       ▼
                      ┌─────────────────────────────────┐
                      │ the cat sat\n                   │
                      │ on the mat\n                    │
                      │ the end\n                       │
                      └─────────────────────────────────┘
```

## Lines Are a Convention Too

A **line** is the text between two **newline** characters.[]{idx="line ending"} The newline is an ordinary byte (`0a`, written `\n` in code). Editors hide it and start a new row instead; to a program it's just another character.

> **Tip:** When a line count looks one short, check whether the file ends with a newline. `wc -l` counts newline characters, not rows, so a last line without one isn't counted.

Different systems historically chose different line endings. You'll meet all three:

| System | Line ending | Bytes | Where you still see it |
|---|---|---|---|
| Unix, Linux, macOS | LF[]{idx="line ending!LF"} | `0a` | Almost every file on a server, every Git repository by default |
| Windows | CR LF[]{idx="line ending!CR LF"} | `0d 0a` | Files created by Notepad and older Windows tools; some CSV exports from spreadsheets |
| Classic Mac OS (before 2001) | CR | `0d` | Very old files only; treat it as a curiosity |

> **Warning:** Never "fix" line endings on a file you don't own by saving it in another editor. A shell script with `CR LF` endings fails on Linux with a confusing `bad interpreter` error, and a changed file can silently break a checksum or a signature.

## Lab: See the Bytes for Yourself

`xxd` prints any file's bytes in hexadecimal, next to their characters.

1. Run `xxd notes.txt`. **Expected:**

   ```text
   00000000: 7468 6520 6361 7420 7361 740a 6f6e 2074  the cat sat.on t
   00000010: 6865 206d 6174 0a74 6865 2065 6e64 0a    he mat.the end.
   ```

2. Count the `0a` bytes. **Expected:** three. Each `0a` is a newline, which `xxd` prints as a dot on the right, so the file has three lines.

## Summary, Key Terms, and Review Questions

### Summary

- A file is a named sequence of bytes; the disk stores numbers, not letters.
- An **encoding** maps bytes to characters. Use **UTF-8** unless you have a reason not to.
- A line ends at a **newline** byte. Line endings differ between systems.

### Key Terms

| Term | Meaning |
|---|---|
| File | A named sequence of bytes stored on a disk |
| Encoding | The rule that turns bytes into characters, such as UTF-8 |
| Newline | The character (`\n`, byte `0a`) that ends a line |

### Review Questions

1. Why can a text editor and a hex viewer show the "same" file so differently?
2. What does `wc -l` actually count?
3. What goes wrong when a writer and a reader disagree about the encoding?

> **You understand this when** you can explain why `café` takes 4 characters but 5 bytes in UTF-8.
