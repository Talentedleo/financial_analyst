# 05-decisions.md — Ed Thorp's Key Decisions

> The defining moments where Thorp's probability mindset led to breakthroughs.

---

## Decision 1: Beat the Dealer — Card Counting (1961)

**Context:** Ph.D. in mathematics, teaching at MIT. Read a paper by army mathematicians on blackjack strategy.

**The Insight:** Blackjack has *memory* — unlike dice or roulette, the outcome of each hand depends on what cards have been played. This means the odds shift during play.

**The Pivot:** Instead of just improving basic strategy (what everyone else was trying), Thorp realized he needed to track the *composition of the remaining deck*.

**Method:**
- Used the IBM 704 supercomputer at MIT
- Learned Fortran to program probability calculations
- Discovered that removing fives gives the player the biggest edge
- Developed the "Ten-Count" system

**Test:** $10,000 stake from Manny Kimmel. Won $11,000 in a single weekend in Reno.

**Outcome:**
- Published in *Proceedings of the National Academy of Sciences* (1961)
- *Beat the Dealer* (1962) — NYT Bestseller, 700,000+ copies sold
- Casinos changed rules (more decks, earlier shuffling)
- Barred from casinos; used disguises

> "I found out that if the fives go out of the deck, the player gets a huge edge — bigger than any other card."

---

## Decision 2: The Wearable Computer with Claude Shannon (1960-1961)

**Context:** While at MIT, Thorp met Claude Shannon, the father of information theory.

**The Problem:** Can roulette be beaten using physics?

**The Insight:** If you can measure the speed of the roulette wheel and the ball, Newtonian physics can predict which half of the wheel the ball will land in.

**The Innovation:** First wearable computer — a toe-operated timing device with a hidden earpiece transmitting musical tones.

**Method:**
- Operator 1 watches wheel, uses toe to input cadence
- Operator 2 receives prediction through hidden earpiece (musical tones)
- Bet on groups of neighboring numbers for sufficient advantage

**Test:** Final version tested in Shannon's basement lab, June 1961.

**Legacy:** Now illegal in Nevada (Nevada devices law, May 30, 1985).

---

## Decision 3: Beat the Market — Warrant Hedging (1967)

**Context:** After blackjack, Thorp looked for "the biggest casino in the world" — Wall Street. His first stock picks failed badly.

**The Problem:** Stock options (warrants) were priced intuitively, not mathematically. Nobody knew how to value them.

**The Insight:** Warrants could be systematically mispriced relative to the underlying stock. A hedging strategy could lock in profits.

**Method:**
- Developed a mathematical formula for warrant pricing (independent of Black-Scholes)
- Buy underpriced warrants, short overpriced common stock
- Market-neutral position protected against price moves

**Result:**
- Co-authored *Beat the Market* with Sheen T. Kassouf (1967)
- "One of the most influential books of all time on Wall Street"
- Launched "the quant" revolution

> "I got a really neat formula. I said, I like this formula. It looks right to me. I'm going to try it out."

---

## Decision 4: Princeton Newport Partners — First Market-Neutral Hedge Fund (1969)

**Context:** After proving the warrant hedging strategy worked, Thorp decided to formalize it as an investment partnership.

**The Structure:** Convertible Hedge Associates (CHA, 1969) → renamed Princeton/Newport Partners (PNP, 1974).

**Key Features:**
- First market-neutral hedge fund in history
- Systematic, model-driven trading
- Derivatives hedging + statistical arbitrage

**Performance:**
- 20% annualized returns after fees
- 20+ years with zero down quarters
- 227 out of 230 months profitable
- All three down months less than 1%

> "In 230 months, we had three down months. All the others were up."

**The End (1989):** PNP became embroiled in the Drexel Burnham Lambert/Michael Milken junk bond scandal. Thorp was never charged, but the RICO investigation forced liquidation.

---

## Decision 5: Detecting Bernie Madoff's Fraud (1991)

**Context:** A friend asked Thorp to review Madoff's investment strategy.

**The Insight:** Madoff's reported returns were statistically impossible.

**The Method:**
- Analyzed the options strategy Madoff claimed to use (split-strike conversion)
- Realized the returns were too consistent to be real
- The mathematical impossibility was obvious to someone who understood options pricing

> "The returns were too consistent. The options strategy Madoff claimed to use couldn't produce those numbers. I told people. Nobody listened for 17 years."

**Outcome:** Thorp warned people; the fraud was exposed in 2008.

---

## Decision 6: Ridgeline Partners — Statistical Arbitrage (1994-2002)

**Context:** After PNP's closure, Thorp regrouped and launched a new fund.

**The Strategy:** Statistical arbitrage — trading large baskets of stocks based on short-term mean reversion and small statistical correlations.

**Performance:** Successful for 8 years, but returns declined as the strategy became more competitive.

**The Close:** Thorp voluntarily closed the fund in 2002 when returns no longer justified the effort.

> "We closed it largely because the return of the statistical arbitrage strategies had been low since 2002."

---

## Decision 7: The Oil Tanker Trade (1990s)

**Context:** After PNP's closure, Thorp found opportunity in an unlikely place.

**The Trade:** Bought an oil tanker when tanker prices had fallen to scrap value.

**The Insight:** Oil tankers were priced below their replacement cost and operating value. The market had overcorrected.

**Outcome:** Profitable — another demonstration of finding mispricing where others saw only distress.

---

## Decision 8: The Dot-Com Bubble (1999-2000)

**Context:** The tech bubble created extreme mispricing in options and securities.

**The Strategy:** Thorp systematically exploited pricing anomalies created by irrational exuberance.

**Method:** Applied the same warrant hedging/options pricing framework to overvalued tech stocks and their derivatives.

**Outcome:** Profited from the crash that followed, while many lost everything.

---

## Decision Patterns Across All Decisions

| Pattern | Frequency | Example |
|---------|-----------|---------|
| **Prove mathematically first** | Always | IBM 704 simulations before Vegas |
| **Start small, test in reality** | Always | $10,000 in Reno, $2,000 account for market |
| **Exploit what others don't understand** | Always | Options as "lottery tickets" |
| **Keep it market-neutral initially** | Often | Warrant hedging, convertible arbitrage |
| **Walk away when edge disappears** | Always | Closed PNP and Ridgeline |
| **Share knowledge via publication** | Often | Books, academic papers |
| **Use disguises / stealth** | When needed | Casinos: false beards, wraparound glasses |

---

## Sources

- [Wikipedia — Edward O. Thorp](https://en.wikipedia.org/wiki/Edward_O._Thorp)
- [Wikipedia — Princeton Newport Partners](https://en.wikipedia.org/wiki/Princeton_Newport_Partners)
- NPR Planet Money, Episode 749 (2017)
- The Investor's Podcast, TIP128 (2017/2026)
- Poundstone, *Fortune's Formula* (2005)
- Thorp, *A Man for All Markets* (2017)
- Thorp, "Option Theory: What I Knew and When I Knew It" (Wilmott Magazine)
