# Chained RSA

[![Build Status](https://travis-ci.com/o-o-overflow/dc2019q-chainedrsa.svg?token=6XM5nywRvLrMFwxAsXj3&branch=master)](https://travis-ci.com/o-o-overflow/dc2019q-chainedrsa)

## Solution:
      
  0. check out the paper
  
     [The straight one](https://github.com/o-o-overflow/dc2019q-chainedrsa/blob/master/util/rsa_upper_half.pdf)
      
  1. The public key header hints the key is PKCS#1.2. It is clearly written in the "standard" --- PKCS1v2, RFC 2437.
     
     [A great explanation](https://stackoverflow.com/questions/18039401/how-can-i-transform-between-the-two-styles-of-public-key-format-one-begin-rsa)

  2. ed = k * lambda(N) - 1, intead of ed = k * phi(N) - 1.
      lambda(N) is the lcm of (p-1), (q-1), not the multiplication of
      (p-1) and (q-1).
      
  3. The paper's solution need to be edited because of the use of lcm.
      
  4. And you need to add optimizations to improve the performance.
      
  5. Actually you don't need all optimizations. We loose the time in
      case of network latency. I ran it during the game and this can be
      done in 3 minutes in my laptop.

## Confession:
  1. key corpus is too small (it's kinda intentionally, I am okay if you brute force with parallization).
  
  2. same message all the time (I am also okay if you send the msgs you already know)

  ... which made the challenge easier than it should

