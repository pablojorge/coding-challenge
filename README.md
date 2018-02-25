# Coding challenge

I chose to go with the RSA key pair option, as I have previous experience with this. This would save me the time needed to explore how to use Python's "wave" library, or PIL to produce images.

I took some basic functions from an old test I did some time ago, and started playing with the random generator function, initially with a simple generator
based on the standard 'random' library, that emulates the interface of the original function (as expected by RSA.generate)

Then I moved to implement the same custom generator but based on the data from random.org, instead of the "random" module. The initial approach was to fetch data from the server any time the generator function was invoked, but many times only a single byte was needed, which resulted in a full request to retrieve just one number. This triggered 503s from the server (and it was painfully slow).

I moved the calls to random.org inside a python generator to cache the random bytes obtained from the server, and only fetch more data when the random pool becomes empty.

TODO:
 * Proper error handling in the client (quota check, exponential backoff)
 * Follow guidelines from https://www.random.org/clients/
 * Of course, proper doc, tests, logging, dependencies, structure, etc. etc. (leaving those out as this is just an exercise)