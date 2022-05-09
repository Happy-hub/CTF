# ishihara-test - Misc
## Challenge description
> I don't think the person who made this knew what they were doing. Aren’t you supposed to see some kind of number or something in the middle?

## Solution
We are given a file ```flag.svg```:

![flag](https://user-images.githubusercontent.com/54234250/167450241-a7ebc5f8-431c-46dd-b836-a76a7dfae53e.svg)

I opened the file in Sublime Text and saw the following line:
```xml
<style>.c1{fill:#89a1d1;}.c2{fill:#89a1d2;}.c3{fill:#89a1d3;}.c4{fill:#89a1d4;}.c5{fill:#89a1d5;}.c6{fill:#89a1d6;}</style>
```

So I thought, let's change some of the colors and see if that gives us the flag.
After tampering with the values a bit, I came up with this line:
```xml
<style>.c1{fill:#00000;}.c2{fill:#89a1d2;}.c3{fill:#FF000;}.c4{fill:#89a1d4;}.c5{fill:#89a1d5;}.c6{fill:#FF000;}</style>
```

which resulted with this image containing the flag:

![flag_solved](https://user-images.githubusercontent.com/54234250/167450955-5140cb1d-6ad0-4ebf-b6c6-683b98520339.svg)

> sdctf{c0untle55_col0rfu1_c0lors_cov3ring_3veryth1ng}
