sundial
=======

A solver for the sundial word problem typically encountered in the Sun(UK) Newspaper

### Useage ###
python sundial [letters] [minlen] [dictionary file]

letters can be any combination of uppercase and lowercase characters, the first letter in the sequence is classed as the letter at the centre of the dial, the letter that must appear in all words.

minlen defaults to 4

dictionary file defaults to /usr/share/words which should be dictionary file for your system locale language on Linux systems.

## Caveats ##
 - Only ever run on Linux, you'll definately need to provide an alternative dictionary file on Windows systems
 - Nice and quick upto 9 character combinations, OK on 10, you'll have to wait on 11 and any more your on your own.

## sundial2.py ##
Golfed it down to 5 lines.... Not pretty!
