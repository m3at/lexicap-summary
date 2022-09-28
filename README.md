# lexicap-summary
Summarize [transcribed Lex Fridman podcast](https://karpathy.ai/lexicap/index.html).

__Note__: This is just a hack, proper summarization would require to split the source transcript by speaker, and then aggregate properly instead of doing a summary of summary.

Dependencies:
```bash
python3 -m pip install -U transformers beautifulsoup4
```

Usage:
```bash
./summarize_page.sh "https://karpathy.ai/lexicap/0321-small.html"
```
