In wordle, the target string is a word, and each of your guesses is also a word.
In a FoCdle the target string is a simple math equation of a known length
(measured in characters), and each of your guesses must also be math equations of
the same length. Each cell in the FoCdle contains a single digit, or one of four
possible operators "+-*%", or an "=" relationship; and the format of the FoCdle is
always value operator value operator value = result. That is, each FoCdle always
has exactly two operators, one equality, three values, and one result. Each
value is an integer between 1 and 99 inclusive, expressed in the minimum number
of digits (no leading zeros); and the result is a non-zero non-negative integer
also expressed without any leading zeros. The four possible operators are "+",
"-", "*", "%", all with exactly the same interpretation as in Python, and with the
same precedence as in Python ("*" and "%" are carried out before either of "+" or "-").

The difficulty of a FoCdle is measured by its length in total characters.
For example, here is a trace of a person solving a FoCdle of difficulty 10. In their
first guess they tried the 10-character equation "13+12-8=17" and learnt (from the
green cells) what the first operator was and where it was located, and got the location
of the "=" correct. They also learnt (from the yellow cells) that there were at least
one each of the digits 1, 2, 3, and 7 (plus for each of those digits, they learnt one
character position in which it did not appear); and they learnt (from the grey cells)
that there was only a single instance of 1, that the second operator wasn't subtraction,
and that there were no 8 digits anywhere.

From that information they formed their second guess "72+31%6=73" and submitted it.
The response from that told them that the computed value had to be 73; that second
operator wasn't "%" either; that there were no 6s, only one 7, and only one 3; plus also
told them some more positions in which the digits 1 and 2 (which must occur somewhere)
could not appear. This person's third guess wasn't even a valid equation! But it told
them that there was exactly one 5, one or more 4s and no 0s. It also told them that the
second operator was a "*" and was not in position 6. By pooling all of the available
information, the user was able to conclude that there were no 0s (guess 3), one 1 (guess 1),
two or more 2s (guess 3), one 3 (guess 2), one or more 4s (guess 3), one five (guess 3),
no 6s (guess 2), one 7 (guess 2), and no 8s (guess 1). They also know (because it is difficulty
10) that there are only seven digits in total required across the four numbers (three values
and one result; so they can conclude that they have found all of the digits, without needing to
test digit 9. The accumulation of all that information meant that their fourth guess was the
only option that both fitted all of the information clues and was a valid equation, and when
they submitted that guess they got the precious "all green" response.
