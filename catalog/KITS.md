# Kits

Ready-made team plans. Print one with `python3 tools/skillforge.py kit <name>`.

| Kit | What it builds | Launch |
|---|---|---|
| `tax-engine` | Income tax engine: rules-as-data, trace, golden/property/differential tests, CLI/API | `/tax-engine-kit` or "go build a tax engine" |
| `vat-engine` | Sales tax / VAT / GST for invoices and checkout | "go build a VAT engine" |
| `payroll-engine` | Payroll tax + withholding per pay period | "go build a payroll tax engine" |

Any other goal: `/swarm <goal>` and the lead designs the team on the fly from
`python3 tools/skillforge.py search ...` results.
