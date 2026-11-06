"""Bounded retry and mock external-action ledger; never sends email."""
def generate_with_limit(generate, validate, max_attempts=2):
    if max_attempts < 1:
        raise ValueError("max_attempts must include at least one attempt")
    for attempt in range(1, max_attempts + 1):
        try:
            result = generate()
        except TimeoutError:
            continue
        if validate(result):
            return {"status": "succeeded", "attempt": attempt, "result": result}
    return {"status": "failed", "attempt": max_attempts, "error": "attempt limit reached"}

def run_action_once(ledger, action_id, mock_action):
    previous = ledger.get(action_id)
    if previous:
        # pending/unknown requires reconciliation; succeeded must not repeat.
        return previous
    ledger[action_id] = {"status": "pending"}
    try:
        result_id = mock_action()
    except TimeoutError:
        ledger[action_id] = {"status": "unknown"}
    else:
        ledger[action_id] = {"status": "succeeded", "result_id": result_id}
    return ledger[action_id]
