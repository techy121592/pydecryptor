# PyDecryptor

A simple Python decrypter; written using Python version 3. This program terminates simple substitution encryption; thereby decrypting it.

This took me a few attempts.
* At first I attempted to convert the whole sentence into numbers to reveal patterns and use these patterns to compare the sentences to the sentences in the corpus provided. I thought these quotes might be from the books provided, but there weren't, before abandoning this approach, I used regex and the location of the punctuation to prove that the sentences are not on there.
* My second attempt was to brute force the cypher using random guesses, I played around and got this running faster; but after some research and quick math, I realized that even if I got 5000 guesses a second, it would take me longer than the current age of the universe to go through all cyphers; so I knew I needed a better approach.
* My third attempt was take all of the encrypted words, match it with all of the words from the corpus that it could possibly match using the same numeric algorithm from my first attempt. This was taking too long at this point so I sorted the list by the number of matches(least number of matches first.) This dramatically sped the whole process up so that I can reasonably run it on my laptop in a matter of minutes.
* Since I worked on this so hard already, I honestly don't have any ideas to how else I would approach this.

  

You can find the cypher and decrypted text that I generated in *./cypher.txt* and *./decrypted.txt* respectively.

---

You can run the following command from *./py-decryptor/*

`./main.py ./test/challenge/corpus-en.txt ./test/challenge/encoded-en.txt -v -o ./test/challenge/`

You can always pass the -h flag to figure out what the options are, but the -v flag makes it run verbosely and the -o is for the output directory.
