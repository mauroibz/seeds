# Why Seeds requires walkthroughs

**Status:** historical

The walkthrough gate came from a real process failure, not a preference about testing.

After thirteen milestones, one Seeds-run application had 122 passing backend tests,
38 passing frontend tests, 86% coverage, and a green project validator. Those results
were honest. The product still failed its basic purpose.

The audit found that:

- three required frontend foundations had never been installed or used;
- background metadata enrichment had never succeeded against the real provider;
- search discarded the provider's relevance ordering;
- a configured fallback provider had never registered; and
- the application's entire visual feedback layer was screen-reader-only.

The automated suite could not see these failures:

- No required check opened the application, performed its primary flow, and observed the
  result.
- Browser tests could find visually hidden confirmation text and therefore considered the
  flow successful.
- Provider tests mocked the exact adapter method whose implementation was broken.
- A large amount of careful work optimized isolated components while nobody exercised the
  product's end-to-end priority path.

The diagnosis was not that specifications, tests, or agents were useless. It was that
verification stopped one layer too early.

Seeds therefore treats automated gates as necessary and insufficient. A milestone that
changes user-visible behavior is incomplete until an agent:

1. runs the real application against realistic data;
2. performs the relevant user flow end to end;
3. records the environment, actions, and observations; and
4. records anything that looked wrong, even when it is outside current scope.

The same rule applies below the UI: a test that replaces the exact unit or boundary being
claimed as correct is not proof of that claim. Mock the transport or external service at
its edge; exercise the project's own adapter and parsing behavior.

This incident also produced a broader rule: acceptance criteria must name evidence capable
of observing the failure they are meant to prevent. Green checks without that connection
measure activity, not completion.

The complete historical artifacts remain in Git history at commit `0682db0`.
