# crossword-generator

Fills an empty crossword with words that fit.

Uses dynamic programming to fill a crossword template with words such that intersections of down and across words have the same letters.

For example the crossword template below, where # means no letter is placed in that cell


||||||||||||
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|   |   |   |   |   | # |   |   |   |   |   |
|   | # | # | # |   | # |   | # |   | # |   |
|   |   |   | # |   |   |   |   |   |   |   |
|   | # |   | # |   | # |   | # |   | # |   |
| # |   |   |   |   |   | # |   |   |   |   |
|   | # |   | # |   | # |   | # |   | # |   |
|   |   |   |   | # |   |   |   |   |   | # |
|   | # |   | # |   | # |   | # |   | # |   |
|   |   |   |   |   |   |   | # |   |   |   |
|   | # |   | # |   | # |   | # | # | # |   |
|   |   |   |   |   | # |   |   |   |   |   |

The result of the algorithm is the following crossword solution below:


||||||||||||
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| B | A | S | I | S |   | P | A | P | E | R |
| E |   |   |   | I |   | A |   | R |   | H |
| A | I | R |   | L | A | R | G | E | L | Y |
| T |   | E |   | E |   | T |   | C |   | T |
|   | S | C | E | N | E |   | R | I | C | H |
| A |   | O |   | T |   | S |   | S |   | M |
| C | A | M | P |   | S | T | E | E | L |   |
| C |   | M |   | D |   | A |   | L |   | S |
| E | L | E | M | E | N | T |   | Y | E | T |
| P |   | N |   | N |   | U |   |   |   | O |
| T | O | D | A | Y |   | S | H | A | R | P |

