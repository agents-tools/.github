# Presentation fixture

`record.json` captures the successful stdout and exit code of
`printf 'Presentation fixture\n'` using the POSIX shell's `printf` builtin.
It has no product executable, dependencies or path normalization. The empty
recipe selects the renderer's neutral defaults; this fixture has no DESIGN
binding.

Both SVGs are generated with the renderer whose upstream revision and digests
are recorded in [Scripts/vendor/README.md](../../../Scripts/vendor/README.md).
The repository's CI calls the reusable presentation workflow against these
inputs and exports at the candidate revision. This fixture proves the shared
check runs; member adoption still requires the actual member's recording.
