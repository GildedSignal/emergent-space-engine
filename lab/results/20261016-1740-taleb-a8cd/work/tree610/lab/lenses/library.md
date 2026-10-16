# Lens: Julien's library (practitioners with skin in the game)

Before anything else, fetch the evidence:
- **His Readwise highlights**, through the API: `curl -s -H "Authorization: Token $READWISE_TOKEN" "https://readwise.io/api/v2/export/?pageCursor=<cursor>"`. Follow `nextPageCursor` until it is null, and cache the result in your run folder.
- **His book list:** `lab/library/goodreads.csv` (title, author, rating, shelves).

If `READWISE_TOKEN` is unset, say so and use the book list plus your own knowledge of those books. Mark every quote you did not retrieve verbatim as UNVERIFIED.

Take the top bottleneck on the board, or the one named in your run. Find how the best practitioners, people who actually did things (founders, engineers, Skunk Works, SpaceX, quant traders, the compute-starved), solved that same structure.

**Deliver** the 5 most applicable lessons, each with:
- a verbatim highlight from his library, with author and title;
- the mechanism behind it;
- the concrete change it implies for our design or plan;
- the cheapest test of that change.

At most 40 lines.

**Blind spot:** analogies are cheap. Keep only the lessons that change a decision.
