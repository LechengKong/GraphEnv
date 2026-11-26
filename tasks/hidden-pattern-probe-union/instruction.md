You are investigating an unknown system through the `probe` command-line tool (run `probe --help`).

The system consists of items, each with an opaque ID, and links between items. You can only learn
about it through `probe`:

- `probe status` tells you the **start item** and your remaining budget.
- `probe neighbors ITEM` lists the items linked to ITEM. You may only ask about items you have
  already seen (the start item, or any item returned by an earlier `neighbors` call). This command
  is free and unlimited.
- `probe evaluate ITEM ...` scores a selection of 1 to 200 seen items and returns a number between
  0 and 1 that measures how closely your selection matches a hidden **target selection**. A score
  of 1.0 means your selection matches the target. You have a budget of **150** `evaluate` calls in
  total; once it is spent, `evaluate` stops working.
- `probe submit ITEM ...` submits your final selection. You can submit only once, and it ends the
  task.

The target selection contains the start item. It was not picked at random: it is defined by a
simple rule relative to the start item and the way items are linked.

Your goal is to submit a selection that matches the target. Your submission is graded by the same
matching criterion that makes `evaluate` return 1.0. Submissions that do not match score zero,
however close their score was.
