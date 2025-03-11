# Lead targeting 🚀

## Introduction

How do you cut through the noise and find the perfect leads for your business? Traditional lead generation is slow, manual, and often misses the mark. What if you could leverage AI to instantly surface the most relevant prospects—without spending hours digging through profiles?  
Our solution transforms how you identify and engage with potential customers, candidates, or partners. By combining LinkedIn data, AI-driven embeddings, and vector search, we help business identify and prioritize high-value leads.

✅ **Automatic** – No more manual searches; our system gathers and structures LinkedIn profiles for you.  
✅ **Intelligent** – AI-powered embeddings capture deep insights into each profile.  
✅ **Precision-Driven** – A simple prompt retrieves the most relevant leads from a vector database.  

Imagine entering a search query defining your Ideal Customer Profile like:  
🔍
*“Senior IT security and infrastructure leaders in large industrial companies”*

…and instantly getting the most relevant profiles, ranked and ready for action.

Whether you're in sales, recruiting, or networking, this system ensures you spend time on the right people—not just anyone.

🚀 Stop searching. Start connecting.


## Get started

To simplify usage, `make` commands are available. If you don't want to use `make`, simply execute the corresponding commands in the `Makefile`.

### 1. Create right environment, with dependencies

```
make sync
```

### 2. Get data from [LinkedIn Dataset](https://github.com/navid-aub/LinkedIn-Dataset)

```
make download-data
```

### 3. Build & feed databases
```
make build-databases
```

### 4. Serve the User Interface
```
make serve-ui
```