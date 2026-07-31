# Resolution registry

Information cutoff: 2026-07-30. All probabilities remain provisional until
the entrant's authorship review.

## General protocol

- Threshold equality resolves as stated in each sentence (`at least` includes
  equality; `more than` does not).
- Use the first qualifying official release published by 2031-06-30, unless a
  forecast-specific date below supersedes it.
- Use the latest vintage available on that publication date; later historical
  revisions do not reopen resolution.
- A renamed successor series is acceptable only if the publisher documents
  comparability. Otherwise apply the stated fallback; where none exists, the
  event resolves No.
- Dollars are nominal U.S. dollars. Calendar years and UTC dates apply.

## Forecast-specific contracts

**F01.** The evaluated system must be generally available to outside users by
2029-12-31, and METR must publish by 2030-06-30 a 50% time-horizon point
estimate of at least 168 hours on a software/research task suite that METR does
not designate saturated. If METR discontinues the series without a documented
successor, resolve No.

**F02.** Use the national, firm-count-weighted estimate for the core BTOS
question asking whether the business used AI in any business function during
the prior two weeks, for the collection period ending latest in 2028. Ignore
the employment-weighted supplement estimate. Resolve from the original release
even if Census later revises it.

**F03.** Calculate `(index_2030Q4 / index_2026Q4)^(1/4)-1` from the BLS
nonfarm-business labor-productivity index in the release available on
2031-06-30. The event resolves Yes only if the result is strictly above 2.25%.

**F04.** Sum company-disclosed capital expenditure excluding acquisitions for
calendar-quarter activity in 2028. Use restated comparable figures when
available. Alphabet and Meta use purchases of property and equipment; Amazon
includes equipment acquired under finance leases in its disclosed capex;
Microsoft is aligned from fiscal-quarter disclosures to calendar quarters.

**F05.** Use the first DOE/LBNL national study published by 2032-12-31 that
estimates actual 2030 data-center electricity consumption and total U.S.
electricity use. If none is published, use the corresponding EIA national
estimate available on that date. Resolve No if neither source reports both
quantities.

**F06.** Count distinct corporate foundry operators, not fabrication plants.
High-volume production must occur at a U.S. wafer fab and be described by the
operator in an audited filing or official release as commercial high-volume or
mass production. Node size follows the operator's marketed name, so Intel 18A
qualifies as smaller than 2 nm; research, risk production, qualification, and
packaging do not qualify.

**F07.** A facility must be physically located in an EU member state, formally
selected/co-funded under the Commission/EuroHPC AI Gigafactories program, and
have accepted at least one compute allocation from a legally separate external
user by 2029-12-31. AI Factories and antennas do not count.

**F08.** For each fixed mineral basket member (copper, lithium, nickel, cobalt,
graphite, manganese), take the largest country's share of global refined
production in 2030 and calculate the unweighted mean. Use the first IEA Global
Critical Minerals Outlook published by 2032-06-30 with 2030 actuals or
estimates. If one mineral is missing, calculate over the other five; if two or
more are missing, resolve No.

**F09.** Use the General Administration of Customs of China annual U.S.-dollar
goods exports less goods imports. Exactly two or three annual surpluses from
2027, 2028, and 2029 must each be strictly greater than $1 trillion.

**F10.** Use the WTO's estimate of the share of merchandise trade conducted on
MFN terms at 2029 year-end, as first published by 2030-06-30. If the WTO
publishes a range, use its midpoint. If it publishes no update or comparable
successor estimate, resolve No.

**F11.** Count the members shown on the WTO Appellate Body roster at
23:59 UTC on 2029-12-31. Fewer than three resolves Yes, irrespective of interim
arbitration arrangements.

**F12.** For each calendar year, divide duties collected by customs value for
total U.S. merchandise imports in USITC DataWeb, then take the unweighted mean
of the three annual rates. Use DataWeb data downloaded on 2030-06-30; the event
resolves Yes at 8.000% or above.
