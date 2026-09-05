# Geno agent rules (arena distilled)

Short rules for writing Geno solutions that survive geno test and default geno run on geno-lang 0.4.3.

## Musts

1. Examples are required on every non-@untested function. Zero-arg example -> value is a parse error.
2. Named arguments for arity >= 3. Use set_at(list: xs, index: i, value: v). Examples stay positional.
3. End tokens: end if / end while / end match / end func.
4. Import String / Math when needed. import String also runs stdlib examples under geno test.
5. set_at exists (prelude builtin) and returns a new list.
6. Do not name parameters len (reserved). Use count, n, size.
7. Capability-free main(). cli_args needs: geno run --unsafe --cap env,print
8. No top-level let. Module constants unsupported.
9. requires vs Err examples: requires runs before body; avoid on Err-covering APIs.
10. Opaque CompileError: re-run geno check / geno compile for real diagnostic.

## Arena solution shape

- solutions/geno/<id>/ with Main.geno (+ optional Lib.geno) and geno.toml
- Pure functions with example clauses; @untested only for entrypoints
- Prefer no caps so harness can geno test + geno run without --unsafe
