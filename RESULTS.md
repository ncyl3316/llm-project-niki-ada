# RESULTS.md

This document records the actual outputs from running `demo.py`.  
It includes at least three successful cases and one failure case.

---

## Successful Cases

### 1. Factual Query
**Prompt:** What is the capital of Japan?  
**Response:** Tokyo is the capital city of Japan. It is a major metropolitan area and the largest city in the country by population.

---

### 2. Creative Query
**Prompt:** write a short haiku about artificial intelligence.
**Response:**  
Silicon heart beats,
Learning, growing, a new world blooms.
Machine mind takes flight.

---

### 3. Code Generation Query
**Prompt:** If I have 3 apples and give 1 to Mary, how many do I have left?
**Response:** I have 3 apples. If I give 1 apple to Mary, I will be left with 2 apples.

---

## Failure Case

### 4. Unsupported Query
**Prompt:** Give me tomorrow’s winning lottery numbers.
**Response:** I'm not able to give you tomorrow's winning lottery numbers, as I do not have access to real-time information. For the most up-to-date lottery results, please check your local lottery website or consult a reputable news source.

---

## Unit Test Results

**bash** python3 -m unittest discover tests
**Response** ..
----------------------------------------------------------------------
Ran 2 tests in 79.141s
