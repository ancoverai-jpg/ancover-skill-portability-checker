# Input contract
Node22+ standard library. One UTF8 regular JSON file, max1MiB, <=100 expected and observed rows. No install dependencies or network. Names are 1-100 ASCII characters from letters, digits, spaces, dot, underscore, parentheses, slash, colon and hyphen; start with letter/digit. App IDs must be positive safe integers. SHA fields require 40 lowercase hex characters. Unknown fields and duplicate expected identities are invalid. JSON duplicate object keys are not independently detected; review the input producer.
Fields:
- schemaVersion:1
- expectedSha, observedSha
- complete:boolean, supplied by operator after verifying pagination
- expected:[{name,appId,allowSkipped:boolean}], nonempty
- checks:[{name,appId,status,conclusion}]
Status queued/in_progress requires conclusion:null. Completed requires success, failure, neutral, cancelled, timed_out, action_required, skipped, stale or startup_failure. Unrecognized values fail input validation.
Duplicate observed identities are AMBIGUOUS. Additional contexts outside policy are counted as ignored; the policy does not claim those checks passed. A policy must reflect the reviewer's intended scope.
Exit0: explicit policy satisfied. Exit1: evidence gaps or revision/completeness problems. Exit2: invalid file, invocation or schema; fixed error without contents or paths.
The evaluator does not authenticate operator assertions, inspect test counts, parse job logs, read branch protection or authorize a merge. Input file selection is not a filesystem security boundary against concurrent replacement, hardlinks or a hostile runtime. Symlink input is rejected when inspected, but race-free resolution is not guaranteed.
